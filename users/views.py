from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect(reverse('wallet:dashboard'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'user/signup.html', {'form': form})


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
                return redirect(reverse('wallet:dashboard'))  # Adjust as needed
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission. Please check your inputs.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'user/login.html', {'form': form})


def logout(request):
    """Handles user logout."""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('users:login'))


@login_required
def dashboard(request):
    """Redirect users to appropriate dashboards based on their roles."""
    if request.user.is_staff:
        return redirect(reverse('admin:index'))  # Admin dashboard
    elif request.user.groups.filter(name="Merchant").exists():
        return render(request, 'merchant/merchant-dashboard.html')  # Merchant dashboard
    else:
        return render(request, 'user/user_dashboard.html')  # Default user dashboard
