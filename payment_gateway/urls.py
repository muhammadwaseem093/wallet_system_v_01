from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init_invoice, name='init_invoice'),
   path('<str:invoice_id>/', views.step1_payment_methods, name='step1_payment_methods'),
    path('<str:invoice_id>/fields/', views.step2_payment_fields, name='step2_payment_fields'),
    path('<str:invoice_id>/review/', views.step3_review, name='step3_review'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
]
