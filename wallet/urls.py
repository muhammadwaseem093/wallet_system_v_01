from django.urls import path
from . import views

urlpatterns = [
    path('wallet-dashboard/', views.wallet_dashboard, name='wallet_dashboard'),
]