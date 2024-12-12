from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init_invoice, name='init_invoice'),
    path('pay/<str:invoice_id>/', views.invoice_checkout, name='invoice_checkout'),
    
]
