from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """Custom form for user registration."""
    
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address'}), required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Select Role'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone_number', 'address', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    """Custom form for user login."""
    
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
