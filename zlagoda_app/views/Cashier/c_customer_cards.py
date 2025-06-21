from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator
import random

def cashier_customer_cards(request):
    """
    3. Отримати інформацію про усіх постійних клієнтів, відсортованих за прізвищем;
    6. Здійснити пошук постійних клієнтів за прізвищем;
    """
    user_role = request.session.get('user_role')
    if user_role not in ['cashier1', 'cashier2', 'cashier3', 'cashier4']:
        return redirect('login')
    page_number = request.GET.get('page', 1)
    surname_filter = request.GET.get('surname', '').strip()

    query = """
        SELECT * 
        FROM Customer_Card
    """
    params = []

    if surname_filter:
        query += " WHERE cust_surname ILIKE %s"
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
    user_role = request.session.get('user_role')
    if user_role not in ['cashier1', 'cashier2', 'cashier3', 'cashier4']:
        return redirect('login')
    if request.method == "POST":
        data = request.POST

        card_number = str(random.randint(10**12, 10**13 - 1))
        query = """
        INSERT INTO Customer_Card (card_number, cust_surname, cust_name, 
                                   cust_patronymic, phone_number, city, 
                                   street, zip_code, percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        with connection.cursor() as c:
            c.execute(query, [
                card_number, data['cust_surname'], data['cust_name'],
                data.get('cust_patronymic'), data['phone_number'],
                data.get('city'), data.get('street'), data.get('zip_code'), data['percent']
            ])
        return redirect("cashier_customer_cards")


def cashier_edit_customer_card(request):
    """
    8. Редагувати інформацію про постійних клієнтів;
    """
    user_role = request.session.get('user_role')
    if user_role not in ['cashier1', 'cashier2', 'cashier3', 'cashier4']:
        return redirect('login')
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