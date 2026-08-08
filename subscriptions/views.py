import helpers.billing
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from subscriptions.models import SubscriptionPrice, UserSubscription

@login_required
def user_subscription_view(request,):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == "POST":
        print("refresh subscription")
    sub_data = {}
    if user_sub_obj.stripe_id:
        sub_data = helpers.billing.get_subscription(user_sub_obj.stripe_id)
    return render(request, 'subscriptions/user_detail_view.html', {'subscription': sub_data})

# Create your views here.
def subscription_price_view(request, interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoices.YEARLY
    object_lists = qs.filter(interval=inv_mo)
    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name, kwargs={'interval': inv_mo})
    yr_url = reverse(url_path_name, kwargs={'interval': inv_yr})
    active = inv_mo
    if interval == inv_yr:
        active = inv_yr
        object_lists = qs.filter(interval=inv_yr)
    return render(request, 'subscriptions/pricing.html', {'object_lists': object_lists,
        'mo_url': mo_url,
        'yr_url': yr_url,
        'active': active
    })