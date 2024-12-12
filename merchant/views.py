from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from .models import User, ActivityLog
from .models import Merchant
from transactions.models import Transaction

@login_required
def merchant_dashboard(request):
    """Merchant-specific dashboard."""
    if request.user.role == 'merchant':
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        sales_total = transactions.filter(type='sending').aggregate(Sum('amount'))['amount__sum'] or 0
        context = {
            'transactions': transactions,
            'sales_total': sales_total,
        }
        return render(request, 'merchant/merchant_dashboard.html', context)
    return redirect('users:dashboard')

@login_required
def checkout_page(request):
    """Handles merchant checkout functionality."""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        if amount and payment_method:
            # Assuming PaymentGateway model is configured
            PaymentGateway.objects.create(
                user=request.user,
                amount=amount,
                payment_method=payment_method
            )
            messages.success(request, 'Checkout successful!')
            return redirect('merchant:merchant_dashboard')
        messages.error(request, 'Invalid input. Please check and try again.')
    return render(request, 'merchant/checkout_page.html')