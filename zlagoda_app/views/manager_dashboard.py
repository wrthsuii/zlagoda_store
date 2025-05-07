from django.shortcuts import render, redirect
from django.db import connection

def manage_employees(request):
    """
    5. Отримати інформацію про усіх працівників, відсортованих за прізвищем;
    6. Отримати інформацію про усіх працівників, що займають посаду касира,
    відсортованих за прізвищем;
    """
    role_filter = request.GET.get('empl_role', '')

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
    context = {
        'employees': employees,
        'role_filter': role_filter,
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
    return redirect("manage_employees")