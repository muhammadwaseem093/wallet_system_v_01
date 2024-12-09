from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    
    path('signup/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]