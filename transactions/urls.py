from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, Name='transaction_list'),
    path('create/', views.create_transaction, Name='create_transaction'),
]