from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.core.paginator import Paginator
from datetime import datetime

def manage_receipts(request):
    """
    17. Отримати інформацію про усі чеки, створені певним касиром за певний період
    часу;
    18. Отримати інформацію про усі чеки, створені усіма касирами за певний період
    часу;
    19. Визначити загальну суму проданих товарів з чеків, створених певним касиром за
    певний період часу;
    20. Визначити загальну суму проданих товарів з чеків, створених усіма касиром за
    певний період часу;
    21. Визначити загальну кількість одиниць певного товару, проданого за певний
    період часу.
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    page_number = request.GET.get('page', 1)
    cashier_filter = request.GET.get('cashier', '')
    date_from = request.GET.get('start_date')
    date_to = request.GET.get('end_date')
    product_filter = request.GET.get('product')

    with connection.cursor() as c:
        c.execute("""
        SELECT id_employee, empl_surname 
        FROM Employee 
        WHERE empl_role = 'cashier' 
        ORDER BY empl_surname;
        """)
        cashiers = [{'id': row[0], 'surname': row[1]} for row in c.fetchall()]

        c.execute("""
        SELECT id_product, product_name
        FROM Product
        ORDER BY id_product;
        """)
        products = [{'id': row[0], 'name': row[1]} for row in c.fetchall()]

        selected_product_name = None
        if product_filter:
            c.execute("""
            SELECT product_name 
            FROM Product 
            WHERE id_product = %s;
            """, [product_filter])
            result = c.fetchone()
            if result:
                selected_product_name = result[0]

        stats = {'total_receipts': 0, 'total_sales': 0, 'product_quantity': None}

        count_query = """
            SELECT COUNT(*) 
            FROM "Check" C
            WHERE 1=1
        """
        count_params = []

        if cashier_filter:
            count_query += " AND C.id_employee = %s"
            count_params.append(cashier_filter)
        if date_from:
            count_query += " AND C.print_date >= %s"
            count_params.append(date_from)
        if date_to:
            count_query += " AND C.print_date <= %s"
            count_params.append(date_to)

        c.execute(count_query, count_params)
        stats['total_receipts'] = c.fetchone()[0]

        sum_query = """
            SELECT COALESCE(SUM(C.sum_total), 0)
            FROM "Check" C
            WHERE 1=1
        """
        sum_params = []

        if cashier_filter:
            sum_query += " AND C.id_employee = %s"
            sum_params.append(cashier_filter)
        if date_from:
            sum_query += " AND C.print_date >= %s"
            sum_params.append(date_from)
        if date_to:
            sum_query += " AND C.print_date <= %s"
            sum_params.append(date_to)

        c.execute(sum_query, sum_params)
        stats['total_sales'] = c.fetchone()[0]

        if product_filter:
            product_quantity_query = """
                SELECT COALESCE(SUM(S.product_number), 0)
                FROM (Sale S
                JOIN Store_Product SP 
                ON S.UPC = SP.UPC)
                JOIN "Check" C 
                ON S.check_number = C.check_number
                WHERE SP.id_product = %s
            """
            product_params = [product_filter]

            if cashier_filter:
                product_quantity_query += " AND C.id_employee = %s"
                product_params.append(cashier_filter)
            if date_from:
                product_quantity_query += " AND C.print_date >= %s"
                product_params.append(date_from)
            if date_to:
                product_quantity_query += " AND C.print_date <= %s"
                product_params.append(date_to)

            c.execute(product_quantity_query, product_params)
            stats['product_quantity'] = c.fetchone()[0]

    query = """
        SELECT DISTINCT C.check_number, E.empl_surname, C.print_date, C.sum_total
        FROM "Check" C
        JOIN Employee E 
        ON C.id_employee = E.id_employee
        WHERE 1=1
    """
    params = []

    if cashier_filter:
        query += " AND C.id_employee = %s"
        params.append(cashier_filter)
    if date_from:
        query += " AND C.print_date >= %s"
        params.append(date_from)
    if date_to:
        query += " AND C.print_date <= %s"
        params.append(date_to)
    if product_filter:
        query += """
            AND EXISTS (
                SELECT 1 
                FROM Sale S
                JOIN Store_Product SP 
                ON S.UPC = SP.UPC
                WHERE S.check_number = C.check_number
                AND SP.id_product = %s
            )
        """
        params.append(product_filter)

    query += " ORDER BY C.print_date DESC"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    receipts = [
        {
            'check_number': row[0],
            'empl_surname': row[1],
            'print_date': row[2],
            'sum_total': row[3]
        }
        for row in rows
    ]

    paginator = Paginator(receipts, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'cashiers': cashiers,
        'products': products,
        'page_obj': page_obj,
        'stats': stats,
        'request': request,
        'selected_product_name': selected_product_name,
        'selected_product_id': product_filter,
        'receipts': receipts
    }
    return render(request, "templates_manager/manage_receipts.html", context)

def delete_check(request):
    """
    3. Видаляти дані про чеки;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == 'POST':
        check_number = request.POST['check_number']

        with transaction.atomic():
            with connection.cursor() as c:
                # Отримати всі продукти з цього чека
                c.execute("""
                        SELECT UPC, product_number
                        FROM Sale
                        WHERE check_number = %s;
                    """, [check_number])
                products = c.fetchall()

                # Повернути продукти на склад
                for upc, product_number in products:
                    c.execute("""
                            UPDATE Store_Product
                            SET products_number = products_number + %s
                            WHERE UPC = %s;
                        """, [product_number, upc])

                # Видалити записи про продажі
                c.execute("""
                        DELETE FROM Sale
                        WHERE check_number = %s;
                    """, [check_number])

                # Видалити сам чек
                c.execute("""
                        DELETE FROM "Check"
                        WHERE check_number = %s;
                    """, [check_number])

    return redirect('manage_receipts')

def receipt_details(request, check_number):
    """
    17. Отримати інформацію про усі чеки, створені певним касиром за певний період
    часу (з можливістю перегляду куплених товарів у цьому чеку, їх назви, к-сті та ціни);
    18. Отримати інформацію про усі чеки, створені усіма касирами за певний період
    часу (з можливістю перегляду куплених товарів у цьому чеку, їх назва, к-сті та ціни);
    """
    with connection.cursor() as c:
        c.execute("""
            SELECT C.check_number, E.empl_surname, C.card_number, 
                   C.print_date, C.sum_total, C.vat, SUM(S.selling_price_total) AS SPT
            FROM (("Check" C
            JOIN Employee E 
            ON C.id_employee = E.id_employee)
            LEFT JOIN Customer_Card CC 
            ON C.card_number = CC.card_number)
            JOIN Sale S ON C.check_number = S.check_number
            WHERE C.check_number = %s
            GROUP BY C.check_number, E.empl_surname, C.card_number, C.print_date, 
                     C.sum_total, C.vat;
        """, [check_number])
        receipt_row = c.fetchone()

        receipt = {
            'check_number': receipt_row[0],
            'empl_surname': receipt_row[1],
            'card_number': receipt_row[2],
            'print_date': receipt_row[3],
            'sum_total': receipt_row[4],
            'vat': receipt_row[5],
            'SPT': receipt_row[6],
        }

        c.execute("""
            SELECT P.product_name, SP.selling_price, S.product_number,
                   (SP.selling_price * S.product_number) AS total
            FROM (Sale S
            JOIN Store_Product SP 
            ON S.UPC = SP.UPC)
            JOIN Product P 
            ON SP.id_product = P.id_product
            WHERE S.check_number = %s;
        """, [check_number])

        items = [
            {
                'product_name': row[0],
                'selling_price': row[1],
                'product_number': row[2],
                'total': row[3],
            }
            for row in c.fetchall()
        ]

    context = {
        'receipt': receipt,
        'items': items,
    }

    return render(request, 'templates_manager/receipt_details.html', context)

def advanced_analytics(request):
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    return render(request, "templates_manager/dashb_adv_analytics.html")

def query_1(request):
    """
    *22. Визначити топ-5 товарів місяця, що продаються поміж клієнтів без картки лояльності.
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    selected_date = request.GET.get('month')
    if selected_date:
        try:
            parsed_date = datetime.strptime(selected_date, '%Y-%m')
        except ValueError:
            parsed_date = datetime.today()
    else:
        parsed_date = datetime.today()
    current_month = parsed_date.strftime('%Y-%m')

    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT P.product_name AS product_name, 
                       COUNT(P.id_product) AS products_count, 
                       C.category_name AS category_name
                FROM Product P
                INNER JOIN Store_Product SP 
                ON P.id_product = SP.id_product
                INNER JOIN Sale S 
                ON SP.UPC = S.UPC
                INNER JOIN "Check" Ch 
                ON S.check_number = Ch.check_number
                INNER JOIN Category C 
                ON P.category_number = C.category_number
                WHERE TO_CHAR(Ch.print_date, 'YYYY-MM') = %s
                AND Ch.card_number IS NULL
                GROUP BY P.product_name, C.category_name
                ORDER BY COUNT(P.id_product) DESC
                LIMIT 5;
            """, [current_month])
        top_products = [
            {'product_name': row[0], 'products_count': row[1], 'category_name': row[2]}
            for row in cursor.fetchall()
        ]

    context = {
        'current_month': current_month,
        'top_products': top_products,
    }
    return render(request, 'templates_manager/query_1.html', context)


def query_2(request):
    """
    *23. Визначити касирів, які продали усі продукти, які в базі є поточними акційними товарами.
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT P.product_name, C.category_name, SP.products_number
                FROM Product P 
                INNER JOIN Store_Product SP
                ON P.id_product = SP.id_product
                INNER JOIN Category C
                ON P.category_number = C.category_number
                WHERE SP.promotional_product IS TRUE
                ORDER BY SP.products_number DESC
        """)
        prom_products = [{'product_name': row[0], 'category_name': row[1], 'products_number': row[2]}
                         for row in cursor.fetchall()]

        cursor.execute("""
                SELECT E.id_employee, E.empl_surname, E.empl_name, E.empl_patronymic
                FROM Employee E
                WHERE E.empl_role = 'cashier'
                AND NOT EXISTS (
                                SELECT 1
                                FROM Store_Product SP
                                WHERE SP.promotional_product IS TRUE
                                AND NOT EXISTS (
                                                SELECT 1
                                                FROM "Check" C
                                                INNER JOIN Sale S 
                                                ON C.check_number = S.check_number
                                                WHERE C.id_employee = E.id_employee
                                                AND S.UPC = SP.UPC
                                                )
                                )
        """)
        qualifying_cashiers = [{'id_employee': row[0], 'empl_surname': row[1], 'empl_name': row[2], 'empl_patronymic': row[3]}
                    for row in cursor.fetchall()]
    context = {
        'prom_products': prom_products,
        'qualifying_cashiers': qualifying_cashiers
    }
    return render(request, "templates_manager/query_2.html", context)