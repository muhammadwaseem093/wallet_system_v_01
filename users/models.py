from django.db import models
# impoet abstract user
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=False, verbose_name="Phone Number")
    address = models.TextField(blank=True, null=False, verbose_name="Address")

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('merchant', 'Merchant'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="Role")

    def __str__(self):
        return self.username

    def get_full_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, 'Unknown')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity}"