from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PaymentGateway(models.Model):
    """
    Represents a payment gateway configuration.
    """
    name = models.CharField(max_length=255, unique=True)  # Gateway name (e.g., Stripe, PayPal)
    api_key = models.CharField(max_length=255)            # API key for gateway integration
    api_secret = models.CharField(max_length=255)         # API secret for gateway integration
    enabled = models.BooleanField(default=True)           # Whether the gateway is enabled for transactions
    description = models.TextField(blank=True, null=True) # Description or notes about the gateway
    created_at = models.DateTimeField(default=timezone.now)  # Record creation time
    updated_at = models.DateTimeField(auto_now=True)      # Record last updated time

    def __str__(self):
        return f"{self.name} ({'Enabled' if self.enabled else 'Disabled'})"

class PaymentTransaction(models.Model):
    """
    Represents a payment transaction record.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User initiating the transaction
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount involved in the transaction
    currency = models.CharField(max_length=10, default='USD')      # Currency (e.g., USD, PKR)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE)  # Gateway used for the transaction
    transaction_id = models.CharField(max_length=255, unique=True)         # Unique transaction ID
    status_choices = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')  # Transaction status
    description = models.TextField(blank=True, null=True)  # Optional description for the transaction
    created_at = models.DateTimeField(auto_now_add=True)   # Transaction creation time
    updated_at = models.DateTimeField(auto_now=True)       # Transaction last updated time

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
