from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard/', views.merchant_dashboard, name='dashboard'),
    # path('transactions/', views.merchant_transactions, name='transactions'),
    # path('transaction/<int:id>/', views.merchant_transaction, name='transaction'),
    # path('transaction/<int:id>/approve/', views.merchant_approve_transaction, name='approve_transaction'),
    # path('transaction/<int:id>/reject/', views.merchant_reject_transaction, name='reject_transaction'),
    # path('transaction/<int:id>/refund/', views.merchant_refund_transaction, name='refund_transaction'),
    # path('activity-log/', views.merchant_activity_log, name='activity_log'),
]