import hashlib
import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages
from decouple import config


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        if not login or not password:
            messages.error(request, 'Please fill in both fields.')
            return render(request, 'login.html', {'login': login, 'password': password})

        hashed_password = hash_password(password)

        conn = psycopg2.connect(
            dbname=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            host=config("DB_HOST", default="localhost"),
            port=config("DB_PORT", default="5432")
        )
        cur = conn.cursor()

        query = """
                SELECT id_employee, role_login, empl_name, empl_surname
                FROM Employee
                WHERE role_login = %s AND password_hash = %s
                """
        cur.execute(query, (login, hashed_password))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            # зберігаються дані користувача сесії
            request.session['user_id'] = result[0]
            request.session['user_role'] = result[1]
            request.session['user_name'] = f"{result[2]} {result[3]}"

            if result[1] == 'manager':
                return redirect('manager_dashboard')
            else:
                # інакше відправляє на дашборд касира (всього можливі дві ролі для входу у систему)
                return redirect('create_receipt')
        else:
            messages.error(request, 'Invalid login or password or you are not authorized to access the system.')

    return render(request, 'login.html')


def manager_dashboard(request):
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    return render(request, 'templates_manager/manager_dashboard.html', {
        'user_name': request.session.get('user_name')
    })


def cashier_dashboard(request):
    user_role = request.session.get('user_role')
    if user_role not in ['cashier1', 'cashier2', 'cashier3', 'cashier4']:
        return redirect('login')

    cashier_id = request.session.get('user_id')

    return render(request, 'templates_cashier/cashier_dashboard.html', {
        'user_name': request.session.get('user_name'),
        'cashier_id': cashier_id
    })