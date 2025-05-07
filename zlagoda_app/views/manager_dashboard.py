from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator

#===========EMPLOYEES===========
def manage_employees(request):
    """
    5. Отримати інформацію про усіх працівників, відсортованих за прізвищем;
    6. Отримати інформацію про усіх працівників, що займають посаду касира,
    відсортованих за прізвищем;
    """
    role_filter = request.GET.get('empl_role', '')
    page_number = request.GET.get('page', 1)

    query = "SELECT * FROM Employee"
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
    return render(request, 'templates_manager/manage_employees.html', context)


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

    query = "SELECT * FROM Customer_Card"
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
