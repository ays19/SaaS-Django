import helpers.billing
from typing import Any
from django.core.management.base import BaseCommand
from customers.models import Customer
from subscriptions.models import UserSubscription

class Command(BaseCommand):

    def handle(self, *arg: Any, **options: Any):
        qs = UserSubscription.objects.filter(stripe_id__isnull=False)
        for user_sub_obj in qs:
            user = user_sub_obj.user
            try:
                customer_obj = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                continue
            customer_stripe_id = customer_obj.stripe_id
            if not customer_stripe_id:
                continue
            print(f"Sync {user} - {customer_stripe_id} subs and remove old ones")
            subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
            for sub in subs:
                print(sub.id)