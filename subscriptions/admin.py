from django.contrib import admin
from .models import Subscription, UserSubscription

# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']

admin.site.register(Subscription, SubscriptionAdmin)

admin.site.register(UserSubscription)