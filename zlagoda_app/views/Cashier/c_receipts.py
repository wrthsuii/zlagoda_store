from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator
from datetime import date, datetime
from django.db import transaction
from django.http import JsonResponse
import json
import random

def create_receipt(request):
    """
    7. Здійснювати продаж товарів (додавання чеків);
    """
    if request.method == 'GET':
        card_filter = request.GET.get('card', '')
        product_search = request.GET.get('product_search', '')

        with connection.cursor() as c:
            c.execute("""
                        SELECT card_number, cust_surname, cust_name
                        FROM Customer_Card
                        ORDER BY cust_surname, cust_name
                    """)
            cards = [
                {'card_number': row[0], 'cust_surname': row[1], 'cust_name': row[2]}
                for row in c.fetchall()
            ]

        with connection.cursor() as c:
            if product_search:
                c.execute("""
                            SELECT SP.UPC, P.product_name, SP.selling_price
                            FROM Store_Product SP
                            JOIN Product P 
                            ON SP.id_product = P.id_product
                            WHERE P.product_name ILIKE %s
                            ORDER BY P.product_name
                        """, ['%' + product_search + '%'])
            else:
                c.execute("""
                            SELECT SP.UPC, P.product_name, SP.selling_price
                            FROM Store_Product SP
                            JOIN Product P 
                            ON SP.id_product = P.id_product
                            ORDER BY P.product_name
                        """)

            products = [
                {
                    'UPC': row[0],
                    'product_name': row[1],
                    'price': float(row[2])
                }
                for row in c.fetchall()
            ]

        context = {
            'cards': cards,
            'selected_card': card_filter,
            'products': products,
            'searched_product': product_search,
            'cashier_id': request.session.get('user_id'),
            'user_name': request.session.get('user_name')
        }
        return render(request, 'templates_cashier/cashier_dashboard.html', context)

    elif request.method == 'POST':
        try:
            with transaction.atomic():
                cashier_id = request.session.get('user_id')

                card_number = request.POST.get('card_number') or None
                products_json = request.POST.get('products_json')

                if not products_json:
                    return JsonResponse({'status': 'error', 'message': 'Немає товарів у чеку'}, status=400)

                try:
                    products = json.loads(products_json)
                except json.JSONDecodeError:
                    return JsonResponse({'status': 'error', 'message': 'Невірний формат даних товарів'}, status=400)

                with connection.cursor() as c:
                    for product in products:
                        c.execute("""
                            SELECT products_number 
                            FROM Store_Product 
                            WHERE UPC = %s
                        """, [product['upc']])
                        result = c.fetchone()
                        if not result or result[0] < int(product['quantity']):
                            return JsonResponse({
                                'status': 'error',
                                'message': f'Недостатньо товару {product.get("product_name", product["upc"])} на складі'
                            }, status=400)

                discount_percent = 0
                if card_number:
                    with connection.cursor() as c:
                        c.execute("""
                            SELECT percent 
                            FROM Customer_Card 
                            WHERE card_number = %s
                        """, [card_number])
                        result = c.fetchone()
                        if result:
                            discount_percent = result[0] or 0

                sum_wo_discount = sum(float(item['price']) * int(item['quantity']) for item in products)

                discount_amount = sum_wo_discount * (discount_percent / 100)
                sum_total = sum_wo_discount - discount_amount
                vat = sum_total * 0.2

                check_number = f"{cashier_id[5:]}{datetime.now().strftime('%d%H%M%S')}{str(random.randint(0, 9))}"
                print_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                with connection.cursor() as c:
                    c.execute("""
                        INSERT INTO "Check" (
                            check_number, 
                            id_employee, 
                            card_number, 
                            print_date, 
                            sum_total, 
                            vat
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, [
                        check_number,
                        cashier_id,
                        card_number,
                        print_date,
                        sum_total,
                        vat
                    ])

                    for product in products:
                        c.execute("""
                                        INSERT INTO Sale (
                                        UPC, 
                                        check_number, 
                                        product_number, 
                                        selling_price_total
                                        ) VALUES (%s, %s, %s, %s)
                                        """, [
                            product['upc'],
                            check_number,
                            product['quantity'],
                            product['price']
                        ])

                        c.execute("""
                                        UPDATE Store_Product 
                                        SET products_number = products_number - %s 
                                        WHERE UPC = %s
                                        """, [
                            product['quantity'],
                            product['upc']
                        ])

                return JsonResponse({
                    'status': 'success',
                    'check_number': check_number,
                    'sum_total': sum_total,
                    'vat': vat,
                    'print_date': print_date
                })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Помилка при створенні чеку: {str(e)}',
                "generated_check_number": check_number,
                "length": len(check_number),
            }, status=500)


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
    JOIN Employee E 
    ON C.id_employee = E.id_employee
    WHERE C.id_employee = %s
    AND C.print_date::date BETWEEN %s AND %s
    ORDER BY C.print_date DESC
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