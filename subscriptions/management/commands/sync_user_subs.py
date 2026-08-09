import helpers.billing
from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.models import UserSubscription

class Command(BaseCommand):

    def handle(self, *arg: Any, **options: Any):
        qs = UserSubscription.objects.filter(stripe_id__isnull=False)
        for user_sub_obj in qs:
            user = user_sub_obj.user
            customer_stripe_id = user.customer.stripe_id
            if not customer_stripe_id:
                print(f"Skipping {user} - no Stripe customer id")
                continue
            print(f"Sync {user} - {customer_stripe_id} subs and remove old ones")
            subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
            for sub in subs:
                existing_user_subs_qs = UserSubscription.objects.filter(stripe_id__iexact=f"{sub.id}".strip())
                if existing_user_subs_qs.exists():
                    continue
                helpers.billing.cancel_subscription(sub.id, reason="Dangling active subscription", cancel_at_period_end=False)
                print(sub.id, existing_user_subs_qs.exists())