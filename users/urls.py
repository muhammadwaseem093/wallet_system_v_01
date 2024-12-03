from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('login/', views.login, name='login'),
]