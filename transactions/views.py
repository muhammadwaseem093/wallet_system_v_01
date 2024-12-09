from django.shortcuts import render, redirect
from .models import Transaction
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm

# Create your views here.
@login_required
class transaction_list(request):
    transactions = Transaction.objects.filter(user = request.user)
    return render(request,'transactions/transaction_list.html',{'transactions':transactions})

@login_required
class create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form':form})