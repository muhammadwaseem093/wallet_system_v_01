from django.urls import path
from . import views

app_name ='wallet'

urlpatterns = [
    
    path('wallet_dashboard/', views.wallet_dashboard, name='wallet_dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
]