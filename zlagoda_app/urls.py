from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.check_login, name='login'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('cashier/', views.cashier_dashboard, name='cashier_dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]