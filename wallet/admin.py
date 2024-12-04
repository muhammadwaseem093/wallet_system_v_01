from django.contrib import admin
#write code for admin dashboard access
from .models import Wallet, Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)

