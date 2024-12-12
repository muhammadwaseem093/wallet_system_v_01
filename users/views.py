from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
#import transactions 
from transactions.models import Transaction
from .models import User, ActivityLog




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
    return render(request, 'users/user_dashboard.html')
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
            return render(request, 'users/user_dashboard.html', context)   
        elif request.user.role == 'admin':
            
            return render(request, 'users/user_dashboard.html')
        elif request.user.role == 'merchant':
            return render(request, 'merchant/merchant_dashboard.html')
        else:
            return render(request, 'users/user_dashboard.html')
    else:
        return redirect('users:login')
    
@login_required
def activity_log(request):
    logs = ActivityLog.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, 'users/activity_log.html', {'activity_logs':logs})
    
@login_required
def change_password_view(request):
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not request.user.check_password(old_password):
                messages.error(request, 'Old password is incorrect!')
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('users/user_dashboard')
        return render(request, 'users/change_password.html')
@login_required
def my_wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    return render(request, 'users/my_wallet.html', {'wallet':wallet})

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user,is_read=False)
    return render(request, 'users/notifications.html', {'notifications':user_notifications})

@login_required
def profile_setting(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('firs_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request,'Profile Updated Successfully!')
        return redirect('users/profile_setting')
    return render(request, 'users/profile_setting.html', {'user':request.user})

@login_required
def user_details(request):
    """API to get user details."""
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'address': user.address,
        'role': user.get_full_role_display(),
    }
    return JsonResponse({'user': data})