from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator

def cashier_store_products(request):
    """
    2. Отримати інформацію про усі товари у магазині, відсортовані за назвою;
    12. Отримати інформацію про усі акційні товари, відсортовані за кількістю одиниць
    товару/ за назвою;
    13. Отримати інформацію про усі не акційні товарів, відсортовані за кількістю
    одиниць товару/ за назвою;
    14. За UPC-товару знайти ціну продажу товару, кількість наявних одиниць товару.
    """
    page_number = request.GET.get('page', 1)
    prom_filter = request.GET.get('promotional_product', '')
    upc_search = request.GET.get('UPC', '').strip()

    query = """
    SELECT SP.UPC, SP.UPC_prom, P.product_name, SP.selling_price,
           SP.products_number, SP.promotional_product
    FROM Store_Product SP
    JOIN Product P
    ON SP.id_product = P.id_product
    """
    conditions = []
    params = []

    if prom_filter != '':
        conditions.append("SP.promotional_product = %s")
        params.append(prom_filter)

    if upc_search:
        conditions.append("SP.UPC LIKE %s")
        params.append(f"%{upc_search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY P.product_name, SP.products_number"

    with connection.cursor() as c:
        c.execute(query, params)
        rows = c.fetchall()

    store_products = [
        {
            'upc': row[0],
            'upc_prom': row[1],
            'product_name': row[2],
            'selling_price': row[3],
            'products_number': row[4],
            'promotional_product': row[5]
        }
        for row in rows
    ]

    paginator = Paginator(store_products, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'prom_filter': prom_filter,
        'page_obj': page_obj,
        'UPC': upc_search,
    }
    return render(request, "templates_cashier/cashier_store_products.html", context)