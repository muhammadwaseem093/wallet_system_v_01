from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    address = models.TextField(blank=True, null=True, verbose_name="Address")

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('merchant', 'Merchant'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="Role")

    def __str__(self):
        return self.username

    def get_full_role_display(self):
        """Returns a user-friendly representation of the role."""
        return dict(self.ROLE_CHOICES).get(self.role, 'Unknown')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
