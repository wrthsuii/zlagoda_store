from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_login, name='login'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('cashier/', views.cashier_dashboard, name='cashier_dashboard'),
]