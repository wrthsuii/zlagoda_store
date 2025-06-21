from django.shortcuts import render, redirect
from django.db import connection

def cashier_profile(request):
    """
    15. Можливість отримати усю інформацію про себе.
    """
    user_role = request.session.get('user_role')
    if user_role not in ['cashier1', 'cashier2', 'cashier3', 'cashier4']:
        return redirect('login')
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