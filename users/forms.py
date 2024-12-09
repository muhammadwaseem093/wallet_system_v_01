from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom form for user registration."""



    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2',]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        }



class CustomAuthenticationForm(AuthenticationForm):
    """Custom form for user login."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )
