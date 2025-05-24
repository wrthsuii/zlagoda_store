from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date

#===========CUSTOMERS===========

def cashier_customer_cards(request):
    """
    3. Отримати інформацію про усіх постійних клієнтів, відсортованих за прізвищем;
    6. Здійснити пошук постійних клієнтів за прізвищем;
    """
    page_number = request.GET.get('page', 1)
    surname_filter = request.GET.get('surname', '').strip()

    query = """
        SELECT * 
        FROM Customer_Card
    """
    params = []

    if surname_filter:
        query += " WHERE LOWER(cust_surname) LIKE LOWER(%s)"
        params.append(f"%{surname_filter}%")

    query += " ORDER BY cust_surname"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    customer_cards = [
        {
            'card_number': row[0],
            'cust_surname': row[1],
            'cust_name': row[2],
            'cust_patronymic': row[3],
            'phone_number': row[4],
            'city': row[5],
            'street': row[6],
            'zip_code': row[7],
            'percent': row[8]
        }
        for row in rows
    ]

    paginator = Paginator(customer_cards, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'templates_cashier/cashier_customer_cards.html', context)


def cashier_add_customer_card(request):
    """
    8. Додавати інформацію про постійних клієнтів;
    """
    if request.method == "POST":
        data = request.POST
        query = """
        INSERT INTO Customer_Card (card_number, cust_surname, cust_name, 
                                   cust_patronymic, phone_number, city, 
                                   street, zip_code, percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['card_number'], data['cust_surname'], data['cust_name'],
                data.get('cust_patronymic'), data['phone_number'],
                data.get('city'), data.get('street'), data.get('zip_code'), data['percent']
            ])
        return redirect("cashier_customer_cards")


def cashier_edit_customer_card(request):
    """
    8. Редагувати інформацію про постійних клієнтів;
    """
    if request.method == "POST":
        data = request.POST
        query = """
         UPDATE Customer_Card
         SET cust_surname = %s, cust_name = %s, cust_patronymic = %s,
             phone_number = %s, city = %s, street = %s, zip_code = %s,
             percent = %s
         WHERE card_number = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['cust_surname'], data['cust_name'],
                data.get('empl_patronymic'), data['phone_number'],
                data.get('city'), data.get('street'), data.get('zip_code'),
                data['percent'], data['card_number']
            ])
    return redirect('cashier_customer_cards')


def cashier_products(request):
    return render(request, 'templates_cashier/cashier_products.html')

def cashier_db_products(request):
    """
    1. Отримати інформацію про усі товари, відсортовані за назвою;
    4. Здійснити пошук товарів за назвою;
    5. Здійснити пошук товарів, що належать певній категорії, відсортованих за назвою;
    """
    category_filter = request.GET.get('category_name', '')
    product_name_filter = request.GET.get('product_name', '').strip()
    page_number = request.GET.get('page', 1)

    # Отримати список категорій
    with connection.cursor() as c:
        c.execute("""
            SELECT category_name 
            FROM Category 
            ORDER BY category_name
        """)
        category_rows = c.fetchall()
    categories = [row[0] for row in category_rows]

    query = """
        SELECT P.id_product, P.category_number, P.product_name, P.characteristics
        FROM Product P
        JOIN Category C ON P.category_number = C.category_number
    """
    conditions = []
    params = []

    if category_filter:
        conditions.append("C.category_name = %s")
        params.append(category_filter)

    if product_name_filter:
        conditions.append("P.product_name ILIKE %s")
        params.append(f"%{product_name_filter}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY P.product_name"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    products = [
        {
            'id_product': row[0],
            'category_number': row[1],
            'product_name': row[2],
            'characteristics': row[3]
        }
        for row in rows
    ]

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'category_filter': category_filter,
        'product_name_filter': product_name_filter,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, "templates_cashier/cashier_db_products.html", context)

#================

def cashier_store_products(request):
    """
    2. Отримати інформацію про усі товари у магазині, відсортовані за назвою;
    12. Отримати інформацію про усі акційні товари, відсортовані за кількістю одиниць
    товару/ за назвою;
    13. Отримати інформацію про усі не акційні товарів, відсортовані за кількістю
    одиниць товару/ за назвою;
    14. За UPC-товару знайти ціну продажу товару, кількість наявних одиниць товару.
    """
    page_number = request.GET.get('page', 1)
    prom_filter = request.GET.get('promotional_product', '')
    upc_search = request.GET.get('UPC', '').strip()

    query = """
    SELECT SP.UPC, SP.UPC_prom, SP.id_product, P.product_name, SP.selling_price,
           SP.products_number, SP.promotional_product
    FROM Store_Product SP
    JOIN Product P
      ON SP.id_product = P.id_product
    """
    conditions = []
    params = []

    if prom_filter != '':
        conditions.append("SP.promotional_product = %s")
        params.append(prom_filter)

    if upc_search:
        conditions.append("SP.UPC LIKE %s")
        params.append(f"%{upc_search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY P.product_name, SP.products_number"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    store_products = [
        {
            'upc': row[0],
            'upc_prom': row[1],
            'id_product': row[2],
            'product_name': row[3],
            'selling_price': row[4],
            'products_number': row[5],
            'promotional_product': row[6]
        }
        for row in rows
    ]

    paginator = Paginator(store_products, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'prom_filter': prom_filter,
        'page_obj': page_obj,
        'UPC': upc_search,
    }
    return render(request, "templates_cashier/cashier_store_products.html", context)


def cashier_receipts(request):
    """
    9. Переглянути список усіх чеків, що створив касир за цей день;
    10. Переглянути список усіх чеків, що створив касир за певний період часу;
    11. За номером чеку вивести усю інформацію про даний чек, в тому числі
    інформацію про назву, к-сть та ціну товарів, придбаних в даному чеку.
    """
    cashier_id = request.session.get('user_id')

    page_number = request.GET.get('page', 1)
    date_from = request.GET.get('start_date')
    date_to = request.GET.get('end_date')

    if not date_from or not date_to:
        today = date.today().isoformat()
        date_from = today
        date_to = today

    query = """
    SELECT C.check_number, C.print_date, C.sum_total
    FROM "Check" C
    JOIN Employee E ON C.id_employee = E.id_employee
    WHERE C.id_employee = %s
      AND C.print_date::date BETWEEN %s AND %s
    ORDER BY C.print_date DESC, C.check_number DESC
    """
    params = [cashier_id, date_from, date_to]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()

    receipts = [
        {
            'check_number': row[0],
            'print_date': row[1],
            'sum_total': row[2],
        }
        for row in rows
    ]

    paginator = Paginator(receipts, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'start_date': date_from,
        'end_date': date_to,
        'user_name': request.session.get('user_name'),
    }

    return render(request, "templates_cashier/cashier_receipts.html", context)


def cashier_profile(request):
    """
    15. Можливість отримати усю інформацію про себе.
    """
    cashier_id = request.session.get('user_id')
    query = """
       SELECT empl_surname, empl_name, empl_patronymic,
              date_of_birth, phone_number, city, street, 
              zip_code, photo, date_of_start, salary
       FROM Employee
       WHERE id_employee = %s 
       """
    params = [cashier_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()

    if not row:
        # Handle case where employee not found
        return redirect('cashier_dashboard')

    photo_path = row[8] if row[8] else '/static/img/cashier_pic.png'

    context = {
        'user_name': request.session.get('user_name'),
        'empl_surname': row[0],
        'empl_name': row[1],
        'empl_patronymic': row[2],
        'date_of_birth': row[3],
        'phone_number': row[4],
        'city': row[5],
        'street': row[6],
        'zip_code': row[7],
        'photo_path': photo_path,
        'date_of_start': row[9],
        'salary': row[10]
    }

    return render(request, "templates_cashier/cashier_profile.html", context)