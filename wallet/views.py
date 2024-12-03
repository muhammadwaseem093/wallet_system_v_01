from django.shortcuts import render
from .models import Wallet
# define login_required decorator
from django.contrib.auth.decorators import login_required

@login_required
def wallet_dashboard(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)
    return render(request, 'wallet/wallet_dashboard.html', {'wallet': wallet})

# @login_required
# def deposit(request):
#     wallet = Wallet.objects.get(user=request.user)
#     if request.method == 'POST':
#         amount = request.POST['amount']
#         wallet.balance += amount
#         wallet.save()
#     return render(request, 'wallet/deposit.html', {'wallet': wallet})

# @login_required
# def withdraw(request):
#     wallet = Wallet.objects.get(user=request.user)
#     if request.method == 'POST':
#         amount = request.POST['amount']
#         wallet.balance -= amount
#         wallet.save()
#     return render(request, 'wallet/withdraw.html', {'wallet': wallet})

# @login_required
# def transfer(request):
#     wallet = Wallet.objects.get(user=request.user)
#     if request.method == 'POST':
#         amount = request.POST['amount']
#         wallet.balance -= amount
#         wallet.save()
#     return render(request, 'wallet/transfer.html', {'wallet': wallet})


