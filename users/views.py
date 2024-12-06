from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout,  authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successfully!')
            return redirect('wallet:dashboard')
        else:
            messages.error(request, 'Please Correct the Error Below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'User successfully logged in!')
                return redirect('dashboard')  # Replace 'wallet:dashboard' with your dashboard URL name
            else:
                messages.error(request, 'Invalid login credentials.')
                return render(request, 'users/login.html', {'form': form})
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'user/login.html', {'form': form})
    
def logout(request):
    logout(request)
    messages.success(request, 'You have been loggedout successfully')
    return redirect('user:login') 

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin:index')
    elif request.user.groups.filter(name="Merchant").exists():
        return redirect(request, 'merchant-dashboard.html')
    else:
        return render(request, 'user/dashboard.html')