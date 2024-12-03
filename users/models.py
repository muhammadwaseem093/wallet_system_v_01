from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional address

    # Override the default `groups` and `user_permissions` for custom relationships
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    # Define roles for the user
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('merchant', 'Merchant'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username  # Fix typo from `usernamess` to `username`
