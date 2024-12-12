from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal
from .models import Wallet, Transaction
from django.http import HttpResponseServerError
from django.utils import timezone
# define login_required decorator
from django.contrib.auth.decorators import login_required

@login_required
def wallet_dashboard(request):
    try:
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        if created:
            messages.success(request, "Wallet created successfully!")
            wallet.balance = 0
            wallet.save()
            
        now = timezone.now()
        
        #calculate toal sending this month
        total_sending = Transaction.objects.filter(
            user=request.user,
            transaction_type='sending',
            date__month = now.month,
            date__year =now.year
        ).aggregate(sum('amount')[amount__sum])or 0.00
        
        total_receiving = Transaction.objects.filter(
            user=request.user,
            transaction_type='receiving',
            date__month=now.month,
            date__year=now.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
            
        return render(request, 'wallet/wallet_dashboard.html', {
            'wallet': wallet,
            'total_sending': total_sending,
            'total_receiving':total_receiving
            })
    except Exception as e:
        return HttpResponseServerError(f"An error occured: {str(e)}", status=500)

@login_required
def deposit(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Invalid amount!")

            wallet, create = Wallet.objects.get_or_create(user=request.user)
            wallet.balance += amount
            wallet.save()
            
            messages.success(request, f"Successfully deposited ${amount:.2f} to your wallet!")
            return redirect('wallet:wallet_dashboard')
        except Wallet.DoesNotExist:
            messages.error(request, "Wallet does not exist!")
        except ValueError:
            messages.error(request, "Invalid Deposit amount!")
        except Exception as e:
            messages.error(request, f"An error occured: {str(e)}")
            
    return render(request, 'wallet/deposit.html')
@login_required
def withdraw(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        amount = request.POST['amount']
        wallet.balance -= amount
        wallet.save()
    return render(request, 'wallet/withdraw.html', {'wallet': wallet})

@login_required
def transfer(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        amount = request.POST['amount']
        wallet.balance -= amount
        wallet.save()
    return render(request, 'wallet/transfer.html', {'wallet': wallet})
@login_required
def wallet_balance(request):
    """API to get wallet balance."""
    try:
        wallet = Wallet.objects.get(user=request.user)
        data = {'balance': wallet.balance}
    except Wallet.DoesNotExist:
        data = {'balance': 0}
    return JsonResponse(data)

