import logging
import helpers.billing
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from subscriptions.models import SubscriptionPrice, Subscription, UserSubscription

User = get_user_model()
logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL
# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    return redirect("stripe-checkout-start")

@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get("checkout_subscription_price_id")
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except SubscriptionPrice.DoesNotExist:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect("pricing")

    customer = getattr(request.user, "customer", None)
    if customer is None:
        logger.error(
            "User id=%s has no Customer record at checkout time.",
            request.user.id,
        )
        messages.error(request, "We couldn't find your billing profile. Please contact support.")
        return redirect("pricing")

    if not customer.stripe_id:
        logger.warning(
            "User id=%s attempted checkout before email confirmation / Stripe customer creation "
            "(init_email_confirmed=%s).",
            request.user.id,
            customer.init_email_confirmed,
        )
        messages.error(
            request,
            "Please confirm your email address before subscribing. "
            "Check your inbox for the confirmation link, or request a new one."
        )
        return redirect("pricing")

    customer_stripe_id = customer.stripe_id
    success_url_path = reverse("stripe-checkout-end")
    pricing_url_path = reverse("pricing")
    success_url = f"{BASE_URL}{success_url_path}"
    cancel_url = f"{BASE_URL}{pricing_url_path}"
    price_stripe_id = obj.stripe_id

    if not BASE_URL:
        logger.error("BASE_URL setting is empty/None — checkout success/cancel URLs will be invalid.")

    try:
        url = helpers.billing.start_checkout_session(
            customer_stripe_id,
            success_url=success_url,
            cancel_url=cancel_url,
            price_stripe_id=price_stripe_id,
            raw=False
        )
    except Exception:
        logger.exception(
            "Stripe checkout session creation failed for user_id=%s, price_id=%s, "
            "customer_stripe_id=%s, success_url=%s",
            request.user.id,
            checkout_subscription_price_id,
            customer_stripe_id,
            success_url,
        )
        messages.error(request, "Something went wrong starting checkout. Please try again shortly.")
        return redirect("pricing")

    return redirect(url)


def checkout_finalize_view(request): #here all things coming from stripe
    session_id = request.GET.get('session_id')
    if not session_id:
        logger.warning("checkout_finalize_view hit with no session_id in querystring.")
        messages.error(request, "We couldn't verify your checkout session. Please try again.")
        return redirect("pricing")

    try:
        checkout_data = helpers.billing.get_checkout_customer_plan(session_id)
    except Exception:
        logger.exception(
            "Failed to retrieve checkout/customer/plan from Stripe for session_id=%s "
            "(commonly caused by a test-mode session_id being looked up with a live-mode "
            "STRIPE_SECRET_KEY, or vice versa, or an expired/invalid session).",
            session_id,
        )
        messages.error(
            request,
            "We couldn't confirm your payment right now. If you were charged, "
            "please contact support with your confirmation email."
        )
        return redirect("pricing")

    plan_id = checkout_data.pop('plan_id')
    customer_id = checkout_data.pop('customer_id')
    sub_stripe_id = checkout_data.pop('sub_stripe_id')
    subscription_data = {**checkout_data}
    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id=plan_id)
    except (Subscription.DoesNotExist, Subscription.MultipleObjectsReturned):
        sub_obj = None

    try:
        user_obj = User.objects.get(customer__stripe_id=customer_id)
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        user_obj = None

    _user_sub_exists = False
    updated_sub_options = {
        "subscription": sub_obj,
        "stripe_id": sub_stripe_id,
        "user_cancelled": False,
        **subscription_data,
    }
    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(user=user_obj, **updated_sub_options)
    except Exception:
        logger.exception(
            "Unexpected error creating/loading UserSubscription for user_id=%s",
            getattr(user_obj, "id", None),
        )
        _user_sub_obj = None
    if None in [sub_obj, user_obj, _user_sub_obj]:
        return HttpResponse("There is a error with your account. please contact us.")
    if _user_sub_exists:
        # cancel old sub
        old_stripe_id = _user_sub_obj.stripe_id
        same_stripe_id = sub_stripe_id == old_stripe_id
        if old_stripe_id is not None and not same_stripe_id:
            try:
                helpers.billing.cancel_subscription(old_stripe_id, reason="Auto ended new membership", feedback="other")
            except Exception:
                logger.exception(
                    "Failed to cancel old Stripe subscription %s while upgrading user_id=%s",
                    old_stripe_id,
                    getattr(user_obj, "id", None),
                )
        # assign new sub
        for k, v in updated_sub_options.items():
            setattr(_user_sub_obj, k, v)
        _user_sub_obj.save()
        messages.success(request, "Success! Thank you for your joining.")
        return redirect(_user_sub_obj.get_absolute_url())
    context = {}
    return render(request, "checkout/success.html")