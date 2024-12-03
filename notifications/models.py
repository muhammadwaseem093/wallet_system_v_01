# wallet_system/notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # Recipient
    title = models.CharField(max_length=255, default='No Title')  # Title of the notification
    message = models.TextField()             # Notification body
    is_read = models.BooleanField(default=False)  # Status: read/unread
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
