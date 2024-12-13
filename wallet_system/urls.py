"""
URL configuration for wallet_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),  # Users app
    # path('admin_dashboard', include('admin_dashboard.urls')),  # Admin Dashboard app
    path('wallet/', include('wallet.urls')),  # Wallet app
    path('/', include('merchant.urls')),  # Merchant app
    path('api/invoices/', include('payment_gateway.urls')),
    path('pay/',include('payment_gateway.urls')),
    path('notifications/', include('notifications.urls')),  # Notifications app
    path('transactions/', include('transactions.urls')),  # Transactions app
    
]
