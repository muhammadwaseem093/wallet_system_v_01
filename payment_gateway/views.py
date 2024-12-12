from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Invoice, PaymentGateway
import random


def init_invoice(request):
    if request.method == "POST":
        merchant_id = request.POST.get('merchant_id')
        merchant_webhook_url = request.POST.get('merchant_webhook_url')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency', 'USD')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Validate input
        if not all([merchant_id, merchant_webhook_url, amount, username, email]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if float(amount) <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        # Generate invoice ID
        invoice_id = f"INV_{random.randint(100000, 999999)}"

        # Save invoice
        invoice = Invoice.objects.create(
            invoice_id=invoice_id,
            merchant_id=merchant_id,
            merchant_webhook_url=merchant_webhook_url,
            amount=amount,
            currency=currency,
            username=username,
            email=email,
            address=address,
        )
        # Return invoice data
        
        return JsonResponse({'message': 'Invoice created','invoice_url': f"/api/invoice/{invoice.id}/"})

        # return JsonResponse({'message': 'Invoice created','invoice data is:': invoice,'invoice_url': f"/api/invoice/{invoice.id}/"})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def invoice_checkout(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == "POST":
        payment_method_id = request.POST.get('payment_method_id')

        try:
            gateway = PaymentGateway.objects.get(id=payment_method_id, enabled=True)
        except PaymentGateway.DoesNotExist:
            return JsonResponse({'error': 'Invalid or disabled payment method'}, status=400)

        invoice.payment_method = gateway.name
        invoice.payment_method_id = gateway.id
        invoice.status = 'PAID'
        invoice.save()

        # Simulate webhook notification
        # Here, an async task like Celery could be used
        #return url like localhost/pay/inv_02345
        
        return JsonResponse({'message': 'Payment successful'})

    gateways = PaymentGateway.objects.filter(enabled=True)
    return render(request, 'payment_gateway/checkout.html', {'invoice': invoice, 'gateways': gateways})

