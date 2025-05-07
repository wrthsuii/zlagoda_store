from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import auth, manager_dashboard

urlpatterns = [
    path('', auth.check_login, name='login'),
    path('manager/', auth.manager_dashboard, name='manager_dashboard'),
    path('cashier/', auth.cashier_dashboard, name='cashier_dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('employees/', manager_dashboard.manage_employees, name='manage_employees'),
    path("add_employee/", manager_dashboard.add_employee, name="add_employee"),
    path("edit_employee/", manager_dashboard.edit_employee, name="edit_employee"),
    path("delete_employee/", manager_dashboard.delete_employee, name="delete_employee"),
    path("customer_cards/", manager_dashboard.manage_customer_cards, name="manage_customer_cards"),
    path("add_customer_card/", manager_dashboard.add_customer_card, name="add_customer_card"),
    path("edit_customer_card/", manager_dashboard.edit_customer_card, name="edit_customer_card"),
    path("delete_customer_card/", manager_dashboard.delete_customer_card, name="delete_customer_card"),
]