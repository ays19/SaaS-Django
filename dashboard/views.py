from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from subscriptions.models import UserSubscription
from visits.models import PageVisit

# Create your views here.
@login_required
def dashboard_view(request):
    user_sub_obj = UserSubscription.objects.filter(user=request.user).first()
    context = {
        "user_sub": user_sub_obj,
        "total_site_visits": PageVisit.objects.count(),
    }
    return render(request, 'dashboard/main.html', context)