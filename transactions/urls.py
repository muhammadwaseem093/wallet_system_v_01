from django.urls import path
from . import views

urlpatterns = [
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('<int:transaction_id>/detail/', views.transaction_detail, name='transaction_detail'),
]