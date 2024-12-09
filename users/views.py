from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
#import transactions 
from .models import Transaction

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect(reverse('users:login'))
        else:
            print("Forms errors: ",form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/signup.html', {'form': form})


def login(request):
    """Handles user login."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect(reverse('users:dashboard'))  # Adjust as needed
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission. Please check your inputs.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout(request):
    """Handles user logout."""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('users:login'))


@login_required
def dashboard(request):
    #show user dashboard with handling recursion error
    return render(request, 'dashboard.html')
def dashboard_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = request.user
            context = {
                'user':user,
                'total_transactions':Transaction.objects.filter(user=user).count(),
                'total_users':User.objects.count() if user.role == 'admin' else None,
                'total_sales': Transaction.objects.filter(user=user, type='sending')
.aggregate(Sum('amount'))['amount__sum'] if user.role == 'merchant' else None,
    'total_purchases': Transaction.objects.filter(user=user, type='receiving')
    .aggregate(Sum('amount'))['amount__sum'] if user.role == 'merchant' else None,
}
            return render(request, 'admin/admin_dashboard.html', context)   
        elif request.user.role == 'admin':
            
            return render(request, 'admin/admin_dashboard.html')
        elif request.user.role == 'merchant':
            return render(request, 'merchant/merchant_dashboard.html')
        else:
            return render(request, 'users/user_dashboard.html')
    else:
        return redirect('users:login')