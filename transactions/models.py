from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('sending','Sending'),
        ('receiving','Receiving'),
    )
    
    STATUS_CHOICES = (
        ("success","Success"),
        ("failed","Failed"),
        ("pending","Pending"),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(Self):
        return f"{self.user.username} - {self.amount} - {self.transaction_type} - {self.status}"
    