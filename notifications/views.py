from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from .models import User, ActivityLog
from .models import Notification

@login_required
def notification_list(request):
    """
    Display a list of notifications for the logged-in user.
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')  # Latest first
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})
@login_required
def get_notifications(request):
    """API to fetch unread notifications."""
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    data = [{'id': n.id, 'message': n.message, 'timestamp': n.timestamp} for n in notifications]
    return JsonResponse({'notifications': data})

@login_required
def mark_notification_as_read(request, notification_id):
    """Marks a notification as read."""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found.'})
