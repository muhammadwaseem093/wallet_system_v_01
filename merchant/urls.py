from django.urls import path 
from . import views

urlpatterns = [
    path('merchant-dashboard/', views.merchant_dashboard, name='dashboard'),
]