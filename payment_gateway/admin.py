from django.contrib import admin
from .models import PaymentGateway, PaymentTransaction

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('name','api_key','enabled','created_at','updated_at')
    list_filter = ('enabled',)
    search_fields = ('name',)
    
    
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','user','amount','currency','status','created_at')
    list_filter = ('status','gateway','created_at')
    search_fields = ('transaction_id','user_username','gateway_name')    