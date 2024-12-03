# wallet_system/payment_gateway/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PaymentGateway, PaymentTransaction
import uuid

def process_payment(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        currency = request.POST.get('currency', 'USD')
        gateway_id = request.POST.get('gateway_id')

        # Validate form data
        if not amount or float(amount) <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        # Fetch payment gateway
        try:
            gateway = PaymentGateway.objects.get(id=gateway_id, enabled=True)
        except PaymentGateway.DoesNotExist:
            return JsonResponse({'error': 'Payment gateway not found or disabled'}, status=404)

        # Simulate payment transaction
        transaction_id = str(uuid.uuid4())
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            amount=amount,
            currency=currency,
            gateway=gateway,
            transaction_id=transaction_id,
            status='PENDING'
        )

        # Simulate successful payment (Replace this with actual API call in production)
        transaction.status = 'SUCCESS'
        transaction.save()

        return JsonResponse({'message': 'Payment processed successfully', 'transaction_id': transaction_id})

    # Display available gateways for selection
    gateways = PaymentGateway.objects.filter(enabled=True)
    return render(request, 'payment_gateway/process_payment.html', {'gateways': gateways})
def payment_history(request):
    transactions = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payment_gateway/payment_history.html', {'transactions': transactions})