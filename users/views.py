from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,  authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

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
                login(request, user)
                messages.success(request, 'User Successfully Login!')
                return redirect('wallet:dashboard')
            else:
                return HttpResponse('Invalid Login Credentials', status=401)
        else:
            return HttpResponse('Invalid Form ', status=401)
    else:
        form = AuthenticationForm()
        messages.success(request, 'User Successfully login!')
    return render(request, 'user/login.html', {'form':form}) 
    
    
def logout(request):
    logout(request)
    messages.success(request, 'You have been loggedout successfully')
    return redirect('user:login') 