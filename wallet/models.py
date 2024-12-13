from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    
    
    def __str__(self):
        return f"Wallet of {self.user.username}"
    
# control debit and credit transactions
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    transaction_type = models.CharField(max_length=50, choices=[('credit', 'credit'), ('debit', 'debit')])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_type} of {self.amount} on {self.timestamp}"