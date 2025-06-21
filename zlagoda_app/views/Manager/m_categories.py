from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator

def manage_categories(request):
    """
    8. Отримати інформацію про усі категорії, відсортовані за назвою;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
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
        'categories': categories
    }
    return render(request, 'templates_manager/manage_categories.html', context)


def add_category(request):
    """
    1. Додавати нові дані про категорії;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == "POST":
        data = request.POST

        query = """
        INSERT INTO Category (category_number, category_name)
        VALUES (%s, %s);
        """
        with connection.cursor() as c:
            c.execute("""
                        SELECT COALESCE(MAX(category_number), 0) + 1
                        FROM Category
            """)
            category_number = c.fetchone()[0]

            c.execute(query, [
                category_number, data['category_name']
            ])
        return redirect("manage_categories")


def edit_category(request):
    """
    2. Редагувати дані про категорії;
    """
    if request.session.get('user_role') != 'manager':
        return redirect('login')
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
    if request.session.get('user_role') != 'manager':
        return redirect('login')
    if request.method == 'POST':
        category_number = request.POST['category_number']

        query = """
        DELETE FROM Category
        WHERE category_number = %s;
        """
        with connection.cursor() as c:
            c.execute(query, [category_number])

    return redirect('manage_categories')