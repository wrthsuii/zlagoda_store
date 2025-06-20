from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator

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
        'store_products': store_products
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