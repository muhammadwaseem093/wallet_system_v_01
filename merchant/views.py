from django.shortcuts import render
from .models import Merchant

def merchant_dashboard(request):
    try:
        merchant = Merchant.objects.get(user=request.user)
    except Merchant.DoesNotExist:
        merchant = None
    return render(request, 'merchant/merchant_dashboard.html', {'merchant': merchant})

