from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator
import random

def manage_customer_cards(request):
    """
    7. Отримати інформацію про усіх постійних клієнтів, відсортованих за прізвищем;
    12. Отримати інформацію про усіх постійних клієнтів, що мають карту клієнта із
    певним відсотком, посортованих за прізвищем;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
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
        'customer_cards': customer_cards
    }
    return render(request, 'templates_manager/manage_customer_cards.html', context)


def add_customer_card(request):
    """
    1. Додавати нові дані про постійних клієнтів;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == "POST":
        data = request.POST
        card_number = str(random.randint(10 ** 12, 10 ** 13 - 1))
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
        return redirect("manage_customer_cards")


def edit_customer_card(request):
    """
    2. Редагувати дані про постійних клієнтів;
    """
    if request.session.get('user_role') != 'manager':
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
    return redirect('manage_customer_cards')


def delete_customer_card(request):
    """
    3. Видаляти дані про постійних клієнтів;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == 'POST':
        card_number = request.POST['card_number']

        query = """
        DELETE FROM Customer_Card
        WHERE card_number = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [card_number])

    return redirect('manage_customer_cards')