from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils.timezone import now

User = get_user_model()

class PaymentGateway(models.Model):
    name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=255,default='API_KEY')
    api_secret = models.CharField(max_length=255,default='API_SECRET')
    enabled = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} ({'Enabled' if self.enabled else 'Disabled'})"

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_id = models.CharField(max_length=50, unique=True)
    merchant_id = models.CharField(max_length=100, default='MERCHANT')
    merchant_webhook_url = models.URLField(default='http://localhost:8000/api/webhook/')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    username = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_method_id = models.CharField(max_length=100, blank=True, null=True)
    status_choices = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    timestampt = models.DateTimeField(default=now)

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.status}"
class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, default='API_KEY')
    api_secret = models.CharField(max_length=255, default='API_SECRET')
    webhook_url = models.URLField(default='http://localhost:8000/api/webhook/')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
    
class ValidatePayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=Invoice.status_choices, default='PENDING')
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.invoice.invoice_id} - {self.status}"
    
    