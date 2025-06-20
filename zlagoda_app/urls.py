from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import auth
from .views.Manager import (m_employee, m_customer_cards, m_categories,
                            m_products, m_store_products, m_receipts)
from .views.Cashier import (c_customer_cards, c_products, c_store_products,
                            c_receipts, c_profile)

urlpatterns = [
    path('', auth.check_login, name='login'),
    path('manager/', auth.manager_dashboard, name='manager_dashboard'),
    path('cashier/', auth.cashier_dashboard, name='create_receipt'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('employees/', m_employee.manage_employees, name='manage_employees'),
    path("add_employee/", m_employee.add_employee, name="add_employee"),
    path("edit_employee/", m_employee.edit_employee, name="edit_employee"),
    path("delete_employee/", m_employee.delete_employee, name="delete_employee"),
    path("customer_cards/", m_customer_cards.manage_customer_cards, name="manage_customer_cards"),
    path("add_customer_card/", m_customer_cards.add_customer_card, name="add_customer_card"),
    path("edit_customer_card/", m_customer_cards.edit_customer_card, name="edit_customer_card"),
    path("delete_customer_card/", m_customer_cards.delete_customer_card, name="delete_customer_card"),
    path("categories/", m_categories.manage_categories, name="manage_categories"),
    path("add_category/", m_categories.add_category, name="add_category"),
    path("edit_category/", m_categories.edit_category, name="edit_category"),
    path("delete_category/", m_categories.delete_category, name="delete_category"),
    path("products/", m_products.manage_products, name="manage_products"),
    path("db_products/", m_products.manage_product_database, name="manage_product_database"),
    path("add_product/", m_products.add_product, name="add_product"),
    path("edit_product/", m_products.edit_product, name="edit_product"),
    path("delete_product/", m_products.delete_product, name="delete_product"),
    path("store_products/", m_store_products.manage_store_products, name="manage_store_products"),
    path("add_store_product/", m_store_products.add_store_product, name="add_store_product"),
    path("edit_store_product/", m_store_products.edit_store_product, name="edit_store_product"),
    path("delete_store_product/", m_store_products.delete_store_product, name="delete_store_product"),
    path("receipts/", m_receipts.manage_receipts, name="manage_receipts"),
    path("delete_check/", m_receipts.delete_check, name="delete_check"),
    path("receipts/<str:check_number>/", m_receipts.receipt_details, name="receipt_details"),
    #for report ---------------------------------------------------
    path("advanced_analytics/", m_receipts.advanced_analytics, name="advanced_analytics"),
    path("query-1/", m_receipts.query_1, name="query_1"),
    path("query-2/", m_receipts.query_2, name="query_2"),
    #--------------------------------------------------------------
    path("cashier_customer_cards/", c_customer_cards.cashier_customer_cards, name="cashier_customer_cards"),
    path("cashier_add_customer_card/", c_customer_cards.cashier_add_customer_card, name="cashier_add_customer_card"),
    path("cashier_edit_customer_card/", c_customer_cards.cashier_edit_customer_card, name="cashier_edit_customer_card"),
    path("cashier_products/", c_products.cashier_products, name="cashier_products"),
    path("cashier_db_products/", c_products.cashier_db_products, name="cashier_db_products"),
    path("cashier_store_products/", c_store_products.cashier_store_products, name="cashier_store_products"),
    path("cashier_profile/", c_profile.cashier_profile, name="cashier_profile"),
    path("cashier_receipts/", c_receipts.cashier_receipts, name="cashier_receipts"),
    path("create_receipt/", c_receipts.create_receipt, name="create_receipt"),
]