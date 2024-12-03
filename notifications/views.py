# wallet_system/notifications/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    """
    Display a list of notifications for the logged-in user.
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')  # Latest first
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})
