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
    path("categories/", manager_dashboard.manage_categories, name="manage_categories"),
    path("add_category/", manager_dashboard.add_category, name="add_category"),
    path("edit_category/", manager_dashboard.edit_category, name="edit_category"),
    path("delete_category/", manager_dashboard.delete_category, name="delete_category"),
    path("products/", manager_dashboard.manage_products, name="manage_products"),
    path("db_products/", manager_dashboard.manage_product_database, name="manage_product_database"),
    path("add_product/", manager_dashboard.add_product, name="add_product"),
    path("edit_product/", manager_dashboard.edit_product, name="edit_product"),
    path("delete_product/", manager_dashboard.delete_product, name="delete_product"),

]