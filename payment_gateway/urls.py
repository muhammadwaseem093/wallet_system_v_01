from django.urls import path
from . import views

urlpatterns = [
    path('process-payment/', views.process_payment, name='process_payment'),
    path('history/',views.payment_history,name='payment_historys'),
]