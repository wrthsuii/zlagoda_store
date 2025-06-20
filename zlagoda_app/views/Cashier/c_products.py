from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator

def cashier_products(request):
    return render(request, 'templates_cashier/cashier_products.html')


def cashier_db_products(request):
    """
    1. Отримати інформацію про усі товари, відсортовані за назвою;
    4. Здійснити пошук товарів за назвою;
    5. Здійснити пошук товарів, що належать певній категорії, відсортованих за назвою;
    """
    category_filter = request.GET.get('category_name', '')
    product_name_filter = request.GET.get('product_name', '').strip()
    page_number = request.GET.get('page', 1)

    with connection.cursor() as c:
        c.execute("""
            SELECT category_name 
            FROM Category 
            ORDER BY category_name
        """)
        category_rows = c.fetchall()
    categories = [row[0] for row in category_rows]

    query = """
        SELECT C.category_name, P.product_name, P.characteristics
        FROM Product P
        JOIN Category C 
        ON P.category_number = C.category_number

    """
    conditions = []
    params = []

    if category_filter:
        conditions.append("C.category_name = %s")
        params.append(category_filter)

    if product_name_filter:
        conditions.append("P.product_name ILIKE %s")
        params.append(f"%{product_name_filter}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY P.product_name"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    products = [
        {
            'category_name': row[0],
            'product_name': row[1],
            'characteristics': row[2]
        }
        for row in rows
    ]

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'category_filter': category_filter,
        'product_name_filter': product_name_filter,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, "templates_cashier/cashier_db_products.html", context)