from django.contrib import admin
from .models import Merchant, Invoice, PaymentGateway

admin.site.register(Merchant)
admin.site.register(Invoice)
admin.site.register(PaymentGateway)