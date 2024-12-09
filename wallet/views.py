from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Wallet
from django.http import HttpResponseServerError
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
            
        return render(request, 'wallet/wallet_dashboard.html', {'wallet': wallet})
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
#count total transactions made by user 
def total_transactions(request):
    wallet = Wallet.objects.get(user=request.user)
    transactions = wallet.transaction_set.all()
    total_transactions = transactions.count()
    print(total_transactions)
    
    return render(request, 'users/dashboard.html', {
        'total_transactions': total_transactions,
    })

