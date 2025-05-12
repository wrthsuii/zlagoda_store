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
    return render(request, "templates_manager/manage_employees.html", context)


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
         WHERE id_employee = %s;
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
    FROM Customer_Card;
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
         WHERE category_number = %s;
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
    13. Здійснити пошук усіх товарів, що належать певній категорії,
    відсортованих за назвою;
    """
    category_filter = request.GET.get('category_name', '')
    page_number = request.GET.get('page', 1)

    with connection.cursor() as c:
        c.execute("""
        SELECT category_name 
        FROM Category 
        ORDER BY category_name
        """)
        category_rows = c.fetchall()
    categories = [row[0] for row in category_rows]

    query1 = """
        SELECT P.id_product, P.category_number, P.product_name, P.characteristics
        FROM Product P
        JOIN Category C 
        ON P.category_number = C.category_number
    """
    params = []
    if category_filter:
        query1 += " WHERE C.category_name = %s"
        params.append(category_filter)
    query1 += " ORDER BY P.product_name"

    with connection.cursor() as c:
        c.execute(query1, params)
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
        'categories': categories,
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
                c.execute("""
                SELECT 1 
                FROM category 
                WHERE category_number = %s;
                """, [data['category_number']])
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
         WHERE id_product = %s;
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

#===========STORE PRODUCTS===========

def manage_store_products(request):
    """
    10. Отримати інформацію про усі товари у магазині, відсортовані за кількістю;
    15. Отримати інформацію про усі акційні товари, відсортовані за кількістю одиниць
    товару/ за назвою;
    16. Отримати інформацію про усі не акційні товари, відсортовані за кількістю
    одиниць товару/ за назвою;
    """
    page_number = request.GET.get('page', 1)
    prom_filter = request.GET.get('promotional_product', '')

    query = """
    SELECT SP.UPC, SP.UPC_prom, SP.id_product, P.product_name, SP.selling_price,
           SP.products_number, SP.promotional_product
    FROM Store_Product SP
    JOIN Product P
    ON SP.id_product = P.id_product
    """
    params = []

    if prom_filter:
        query += " WHERE SP.promotional_product = %s"
        params.append(prom_filter)
    query += " ORDER BY SP.products_number, P.product_name"

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
    }
    return render(request, "templates_manager/manage_store_products.html", context)


def add_store_product(request):
    """
    1. Додавати нові дані про товари в магазині;
    """
    if request.method == "POST":
        data = request.POST
        query = """
        INSERT INTO Store_Product (UPC, UPC_prom, id_product, 
                                   selling_price, products_number, 
                                   promotional_product)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        with connection.cursor() as c:
            c.execute(query, [
                data['UPC'], data.get('UPC_prom') or None,
                data['id_product'], data['selling_price'],
                data['products_number'], data['promotional_product']

            ])
        return redirect("manage_store_products")

def edit_store_product(request):
    """
    2. Редагувати дані про товари в магазині;
    """
    if request.method == "POST":
        data = request.POST
        query = """
         UPDATE Store_Product
         SET UPC_prom = %s, id_product = %s, selling_price = %s, 
             products_number = %s, promotional_product = %s
         WHERE UPC = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [
                data.get('UPC_prom'), data['id_product'], data['selling_price'],
                data['products_number'], data['promotional_product'], data['UPC']
            ])
    return redirect('manage_store_products')


def delete_store_product(request):
    """
    3. Видаляти дані про товари в магазині;
    """
    if request.method == 'POST':
        UPC = request.POST['UPC']

        query = """
        DELETE FROM Store_Product
        WHERE UPC = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [UPC])

    return redirect('manage_store_products')

#===========CHECKS===========

def manage_reports(request):
    return render(request, 'templates_manager/manage_reports.html')


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
                SELECT 1 FROM Sale S
                JOIN Store_Product SP ON S.UPC = SP.UPC
                WHERE S.check_number = C.check_number
                AND SP.id_product = %s
            )
        """
        params.append(product_filter)

    query += " ORDER BY C.check_number DESC"

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
        'selected_product_id': product_filter
    }
    return render(request, "templates_manager/manage_receipts.html", context)

def delete_check(request):
    """
    3. Видаляти дані про чеки;
    """
    if request.method == 'POST':
        check_number = request.POST['check_number']

        query = """
        DELETE FROM "Check"
        WHERE check_number = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [check_number])

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
            SELECT C.check_number, E.empl_surname, C.card_number, CC.cust_surname,
                   CC.cust_name, C.print_date, C.sum_total, C.vat, SUM(S.selling_price_total) AS SPT,
                   CC.percent
            FROM (("Check" C
            JOIN Employee E 
            ON C.id_employee = E.id_employee)
            LEFT JOIN Customer_Card CC 
            ON C.card_number = CC.card_number)
            JOIN Sale S ON C.check_number = S.check_number
            WHERE C.check_number = %s
            GROUP BY C.check_number, E.empl_surname, C.card_number, CC.cust_surname,
                     CC.cust_name, C.print_date, C.sum_total, C.vat, CC.percent;
        """, [check_number])
        receipt_row = c.fetchone()

        receipt = {
            'check_number': receipt_row[0],
            'empl_surname': receipt_row[1],
            'card_number': receipt_row[2],
            'cust_surname': receipt_row[3],
            'cust_name': receipt_row[4],
            'print_date': receipt_row[5],
            'sum_total': receipt_row[6],
            'vat': receipt_row[7],
            'SPT': receipt_row[8],
            'percent': receipt_row[9]
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