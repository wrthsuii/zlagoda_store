from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.core.paginator import Paginator
from django.contrib import messages

#===========EMPLOYEES===========
def manage_employees(request):
    """
    5. Отримати інформацію про усіх працівників, відсортованих за прізвищем;
    6. Отримати інформацію про усіх працівників, що займають посаду касира,
    відсортованих за прізвищем;
    """
    role_filter = request.GET.get('empl_role', '')
    page_number = request.GET.get('page', 1)

    query = """
    SELECT * 
    FROM Employee
    """
    params = []
    if role_filter:
        query += " WHERE empl_role = %s"
        params.append(role_filter)
    query += " ORDER BY empl_surname"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    employees = [
        {
            'id_employee': row[0],
            'empl_surname': row[1],
            'empl_name': row[2],
            'empl_patronymic': row[3],
            'empl_role': row[4],
            'salary': row[5],
            'date_of_birth': row[6],
            'date_of_start': row[7],
            'phone_number': row[8],
            'city': row[9],
            'street': row[10],
            'zip_code': row[11]
        }
        for row in rows
    ]

    paginator = Paginator(employees, 10)  # по 10 працівників на сторінку
    page_obj = paginator.get_page(page_number)

    context = {
        'role_filter': role_filter,
        'page_obj': page_obj,
    }
    return render(request, "manage_employee", context)


def add_employee(request):
    """
    1. Додавати нові дані про працівників;
    """
    if request.method == "POST":
        data = request.POST
        query = """
        INSERT INTO Employee (id_employee, empl_surname, empl_name, empl_patronymic, empl_role,
                             salary, date_of_birth, date_of_start, phone_number, city,
                             street, zip_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['id_employee'], data['empl_surname'], data['empl_name'],
                data.get('empl_patronymic'), data['empl_role'], data['salary'],
                data['date_of_birth'], data['date_of_start'], data['phone_number'],
                data['city'], data['street'], data['zip_code']
            ])
        return redirect("manage_employees")


def edit_employee(request):
    """
    2. Редагувати дані про працівників;
    """
    if request.method == "POST":
        data = request.POST
        query = """
         UPDATE Employee
         SET empl_surname = %s, empl_name = %s, empl_patronymic = %s,
             empl_role = %s, salary = %s, date_of_birth = %s,
             date_of_start = %s, phone_number = %s, city = %s,
             street = %s, zip_code = %s
         WHERE id_employee = %s
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['empl_surname'], data['empl_name'],
                data.get('empl_patronymic'), data['empl_role'], data['salary'],
                data['date_of_birth'], data['date_of_start'], data['phone_number'],
                data['city'], data['street'], data['zip_code'],
                data['id_employee']
            ])
    return redirect('manage_employees')


def delete_employee(request):
    """
    3. Видаляти дані про працівників;
    """
    if request.method == 'POST':
        id_employee = request.POST['id_employee']

        query = """
        DELETE FROM Employee
        WHERE id_employee = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [id_employee])

    return redirect('manage_employees')

#===========CUSTOMERS===========

def manage_customer_cards(request):
    """
    7. Отримати інформацію про усіх постійних клієнтів, відсортованих за прізвищем;
    12. Отримати інформацію про усіх постійних клієнтів, що мають карту клієнта із
    певним відсотком, посортованих за прізвищем;
    """
    percent_filter = request.GET.get('percent', '')
    page_number = request.GET.get('page', 1)

    query = """
    SELECT * 
    FROM Customer_Card
    """
    params = []
    if percent_filter:
        query += " WHERE percent = %s"
        params.append(percent_filter)
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
        'percent_filter': percent_filter,
        'page_obj': page_obj,
    }
    return render(request, 'templates_manager/manage_customer_cards.html', context)


def add_customer_card(request):
    """
    1. Додавати нові дані про постійних клієнтів;
    """
    if request.method == "POST":
        data = request.POST
        query = """
        INSERT INTO Customer_Card (card_number, cust_surname, cust_name, 
        cust_patronymic, phone_number, city, street, zip_code, percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['card_number'], data['cust_surname'], data['cust_name'],
                data.get('cust_patronymic'), data['phone_number'],
                data.get('city'), data.get('street'), data.get('zip_code'), data['percent']
            ])
        return redirect("manage_customer_cards")


def edit_customer_card(request):
    """
    2. Редагувати дані про постійних клієнтів;
    """
    if request.method == "POST":
        data = request.POST
        query = """
         UPDATE Customer_Card
         SET cust_surname = %s, cust_name = %s, cust_patronymic = %s,
             phone_number = %s, city = %s, street = %s, zip_code = %s,
             percent = %s
         WHERE card_number = %s
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['cust_surname'], data['cust_name'],
                data.get('empl_patronymic'), data['phone_number'],
                data.get('city'), data.get('street'), data.get('zip_code'),
                data['percent'], data['card_number']
            ])
    return redirect('manage_customer_cards')


def delete_customer_card(request):
    """
    3. Видаляти дані про постійних клієнтів;
    """
    if request.method == 'POST':
        card_number = request.POST['card_number']

        query = """
        DELETE FROM Customer_Card
        WHERE card_number = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [card_number])

    return redirect('manage_customer_cards')

#===========CATEGORIES===========

def manage_categories(request):
    """
    8. Отримати інформацію про усі категорії, відсортовані за назвою;
    """
    page_number = request.GET.get('page', 1)

    query = """
    SELECT * 
    FROM Category
    ORDER BY category_name;
    """
    params = []

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    categories = [
        {
            'category_number': row[0],
            'category_name': row[1]
        }
        for row in rows
    ]

    paginator = Paginator(categories, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'templates_manager/manage_categories.html', context)


def add_category(request):
    """
    1. Додавати нові дані про категорії;
    """
    if request.method == "POST":
        data = request.POST
        query = """
        INSERT INTO Category (category_number, category_name)
        VALUES (%s, %s);
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['category_number'], data['category_name']
            ])
        return redirect("manage_categories")


def edit_category(request):
    """
    2. Редагувати дані про категорії;
    """
    if request.method == "POST":
        data = request.POST
        query = """
         UPDATE Category
         SET category_name = %s
         WHERE category_number = %s
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['category_name'], data['category_number']
            ])
    return redirect('manage_categories')


def delete_category(request):
    """
    3. Видаляти дані про категорії;
    """
    if request.method == 'POST':
        category_number = request.POST['category_number']

        query = """
        DELETE FROM Category
        WHERE category_number = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [category_number])

    return redirect('manage_categories')

#===========PRODUCTS===========

def manage_products(request):
    return render(request, 'templates_manager/manage_products.html')

def manage_product_database(request):
    """
    9. Отримати інформацію про усі товари, відсортовані за назвою;
    """
    page_number = request.GET.get('page', 1)

    query = """
    SELECT * 
    FROM Product
    ORDER BY product_name;
    """
    params = []

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
        'page_obj': page_obj,
    }
    return render(request, "templates_manager/manage_db_products.html", context)

def add_product(request):
    """
    1. Додавати нові дані про товари;
    """
    if request.method == "POST":
        data = request.POST
        try:
            with connection.cursor() as c:
                c.execute("SELECT 1 FROM category WHERE category_number = %s", [data['category_number']])
                if not c.fetchone():
                    messages.error(request, "Error: The selected category does not exist")
                    return redirect("manage_product_database")

                query = """
                INSERT INTO Product (id_product, category_number, product_name, characteristics)
                VALUES (%s, %s, %s, %s);
                """
                c.execute(query, [
                    data['id_product'],
                    data['category_number'],
                    data['product_name'],
                    data['characteristics']
                ])
            return redirect("manage_product_database")

        except IntegrityError as e:
            if 'foreign key' in str(e).lower():
                messages.error(request, "Error: The selected category does not exist")
            return redirect("manage_product_database")

def edit_product(request):
    """
    2. Редагувати дані про товари;
    """
    if request.method == "POST":
        data = request.POST
        query = """
         UPDATE Product
         SET category_number = %s, product_name = %s, characteristics = %s
         WHERE id_product = %s
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['category_number'], data['product_name'],
                data['characteristics'], data['id_product']
            ])
    return redirect('manage_product_database')


def delete_product(request):
    """
    3. Видаляти дані про товари;
    """
    if request.method == 'POST':
        id_product = request.POST['id_product']

        query = """
        DELETE FROM Product
        WHERE id_product = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [id_product])

    return redirect('manage_product_database')
