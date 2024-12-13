from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Invoice, Merchant, PaymentGateway
import random
import requests


@csrf_exempt
def init_invoice(request):
    if request.method == "POST":
        api_key = request.headers.get("API-Key")
        merchant_id = request.headers.get("Merchant-ID")
        amount = request.POST.get("amount")
        currency = request.POST.get("currency", "USD")

        # Validate Merchant
        merchant = Merchant.objects.filter(api_key=api_key, merchant_id=merchant_id).first()
        # if not merchant and api key then create 
        
        if not merchant:
            return JsonResponse({"error": "Invalid merchant credentials"}, status=400)

        # Validate Amount
        if not amount or float(amount) <= 0:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        # Generate Invoice
        invoice_id = f"INV_{random.randint(100000, 999999)}"
        invoice = Invoice.objects.create(
            invoice_id=invoice_id,
            merchant=merchant,
            amount=amount,
            currency=currency
        )

        return JsonResponse({"status": "success", "invoice_url": f"http://localhost:8000/pay/{invoice_id}/"})

    return JsonResponse({"error": "Invalid request method"}, status=405)

def step1_payment_methods(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    if request.method == "GET":
        gateways = PaymentGateway.objects.filter(enabled=True)
        return render(request, "payment_gateway/step1_payment_method.html", {"invoice": invoice, "gateways": gateways})

    elif request.method == "POST":
        payment_method_id = request.POST.get("payment_method_id")
        if not payment_method_id:
            return render(request, "payment_gateway/error.html", {"message": "Please select a payment method."})

        request.session["selected_gateway"] = payment_method_id
        
        return redirect("step2_payment_fields", invoice_id=invoice.invoice_id)

# Step 2: Payment Fields Input
def step2_payment_fields(request, invoice_id):
    
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    
    selected_gateway_id = request.session.get("selected_gateway")
    
    if not selected_gateway_id:
            return redirect("step1_payment_methods", invoice_id=invoice_id)
    payment_gateway = get_object_or_404(PaymentGateway, id=selected_gateway_id)
    
    if request.method == "POST":
        payment_data = {key: value for key, value in request.POST.items() if key != "csrfmiddlewaretoken"}
        invoice.payment_method = payment_gateway.name
        invoice.payment_method_id = selected_gateway_id
        try:
            invoice.save()
        except Exception as e:
            return render(request, 'payment_gateway/error.html',{"message": "Error saving invoice", "error": str(e)})
            
        return redirect("step3_review", invoice_id=invoice_id)

        # Render the fields dynamically
    return render(request, "payment_gateway/step2_payment_fields.html", {
        'payment_gateway': payment_gateway,
        'invoice_id': invoice_id,
        
        })
        
# Step 3: Review & Submit
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import requests

def step3_review(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    
    # Set the payment method ID
    payment_method_id = invoice.payment_method.id if invoice.payment_method else None

    if request.method == "POST":
        # Prepare the payment payload
        payment_payload = {
            "amount": invoice.amount,
            "currency": "USD",
            "payment_method_id": payment_method_id,
            "payment_data": invoice.payment_data,
            "invoice_id": invoice.invoice_id,
            "callback_url": request.build_absolute_uri('/pay/callback/'),
        }

        # If a webhook URL exists for the payment method
        if invoice.payment_method and invoice.payment_method.webhook_url:
            try:
                # Send the request to the webhook
                response = requests.post(invoice.payment_method.webhook_url, json=payment_payload)
                response_data = response.json()

                if response.status_code == 200 and "payment_url" in response_data:
                    # Redirect to the payment URL
                    return redirect(response_data["payment_url"])
                
                if response_data.get("status") == "success":
                    # Render success template
                    return render(request, "payment_gateway/success.html", {
                        'invoice': invoice, 
                        "message": "Payment successfully initialized."
                    })
                
                # Handle error response
                return render(request, "payment_gateway/error.html", {
                    "message": "Error initializing payment",
                    "error": response_data.get("error")
                })
            except Exception as e:
                # Handle exceptions during webhook communication
                return render(request, "payment_gateway/error.html", {
                    "message": "Error initializing payment",
                    "error": str(e)
                })

        # No valid webhook URL for the payment method
        return render(request, "payment_gateway/error.html", {
            "message": "No valid webhook URL for the payment method."
        })
    
    # Handle GET requests or other cases
    return render(request, "payment_gateway/step3_review.html", {'invoice': invoice})
    



@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        data = request.json()
        payment_id = data.get("payment_id")
        invoice_id = data.get("invoice_id")
        status = data.get("status")

        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            if status == "success":
                invoice.status = "paid"
                invoice.payment_gateway_transaction_id = payment_id
            else:
                invoice.status = "failed"
            invoice.save()
            return JsonResponse({"message": "Payment updated."})
        except Invoice.DoesNotExist:
            return JsonResponse({"error": "Invalid invoice ID."}, status=404)

    return JsonResponse({"error": "Invalid request."}, status=400)