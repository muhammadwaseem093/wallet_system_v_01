from django.db import models

class Merchant(models.Model):
    merchant_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField(default="sdfakljdglld a fdasjlk adgjlkd")
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    api_key = models.CharField(max_length=100, default="anasdlkaejrjdfl")

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, default=1)
    webhook_url = models.URLField(default= "www.example.url")
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True, default="abc coudkldjl djlfjdls")
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_data = models.JSONField(default=dict, null=True)
    payment_method_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')
    
    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.status}"

class PaymentGateway(models.Model):
    name = models.CharField(max_length=50)
    webhook_url = models.URLField(default= "www.example.url")
    enabled = models.BooleanField(default=True)
    input_fields = models.JSONField(null=True,default=dict)  # Store dynamic fields
    
    def __str__(self):
        return self.name
