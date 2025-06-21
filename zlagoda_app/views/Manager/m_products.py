from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator

def manage_products(request):
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    return render(request, 'templates_manager/manage_products.html')

def manage_product_database(request):
    """
    9. Отримати інформацію про усі товари, відсортовані за назвою;
    13. Здійснити пошук усіх товарів, що належать певній категорії,
    відсортованих за назвою;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
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

    query = """
        SELECT P.id_product, C.category_name, P.category_number, 
               P.product_name, P.characteristics
        FROM Product P
        JOIN Category C 
        ON P.category_number = C.category_number
    """
    params = []
    if category_filter:
        query += " WHERE C.category_name = %s"
        params.append(category_filter)
    query += " ORDER BY P.product_name"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    products = [
        {
            'id_product': row[0],
            'category_name': row[1],
            'category_number': row[2],
            'product_name': row[3],
            'characteristics': row[4]
        }
        for row in rows
    ]

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'category_filter': category_filter,
        'categories': categories,
        'page_obj': page_obj,
        'products': products
    }
    return render(request, "templates_manager/manage_db_products.html", context)

def add_product(request):
    """
    1. Додавати нові дані про товари;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == "POST":
        data = request.POST
        with connection.cursor() as c:
                c.execute("""
                            SELECT COALESCE(MAX(id_product), 0) + 1
                            FROM Product
                """)
                id_product = c.fetchone()[0]

                query = """
                INSERT INTO Product (id_product, category_number, product_name, characteristics)
                VALUES (%s, %s, %s, %s);
                """
                c.execute(query, [
                    id_product,
                    data['category_number'],
                    data['product_name'],
                    data['characteristics']
                ])
        return redirect("manage_product_database")

def edit_product(request):
    """
    2. Редагувати дані про товари;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
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
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == 'POST':
        id_product = request.POST['id_product']

        query = """
        DELETE FROM Product
        WHERE id_product = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [id_product])

    return redirect('manage_product_database')