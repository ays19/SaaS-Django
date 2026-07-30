from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription

class Command(BaseCommand):

    def handle(self, *arg: Any, **options: Any):
        print("Hello, World!")
        qs = Subscription.objects.all()