from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Transaction
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm

@login_required
def transaction_list(request):
    if request.user.role not in ['admin', 'merchant', 'user']:
        return HttpResponseForbidden("You do not have access to this page.")
    
    #admin can see all transactions
    if request.user.role == "admin":
        transactions = Transaction.objects.all()
        
    # merchant can see own transactions
    elif request.user.role == "merchant":
        transactions =Transaction.object.filter(merchant=request.user)
        
    #user can see only transaciton they are involved in
    else:
        transactions = Transaction.objects.filter(user=request.user)
        
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.user.role not in ['admin','merchant']:
        return HttpResponseForbidden("You do not have permission to crate a transaction")
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if request.user.role == 'merchant':
                transaction.merchant = request.user
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})

@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    # Role-based access
    if request.user.role == 'admin' or \
       (request.user.role == 'merchant' and transaction.merchant == request.user) or \
       (request.user.role == 'user' and transaction.user == request.user):
        return render(request, 'transactions/transaction_detail.html', {'transaction': transaction})
    
    return HttpResponseForbidden("You do not have permission to view this transaction.")

def transaction_history(request):
    """Returns transaction history for the user."""
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    data = [{
        'id': t.id,
        'amount': t.amount,
        'type': t.type,
        'date': t.date
    } for t in transactions]
    return JsonResponse({'transactions': data})