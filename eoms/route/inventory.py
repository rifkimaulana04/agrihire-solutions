from eoms import app
from flask import render_template, redirect, request, flash, url_for,session,jsonify
from eoms.model import db
from eoms.model.session_utils import allow_role
from datetime import datetime
from eoms.route import promotion


@app.route('/view_inventory', methods=['GET', 'POST'])
def view_inventory():
    inventory_list = []
    allow_role(['staff', 'lmgr', 'nmgr', 'admin'])
    product_code = request.form.get('product_code', '').strip()
    category_code = request.form.get('category_code', '').strip()
    product_name = request.form.get('product_name', '').strip()
    category_list = get_category()
    store_list = promotion.get_store_list()
    store_name = []
    role = session['role']

    if role == 'staff' or role == 'lmgr':
        store_id = session['store_id']
    else:
        store_id = request.form.get('store_id', '').strip()

    product_list = get_products(product_code, category_code, product_name, store_id)

    if store_id:
        for product in product_list:
            p_store_id = product['store_id']
            code = product['product_code']
            c_name = product['category_name']
            p_name = product['name']
            store_name = promotion.get_store_name(p_store_id)['store_name']
            total_machine_quantities = count_machine_quantities(code, store_id)
            inventory_number = total_machine_quantities['COUNT(product_code)']
            booked_item = get_today_inventory(code, store_id)['COUNT(product_code)']
            in_stock = inventory_number - booked_item
            v_list = {
                'product_code': code,
                'c_name': c_name,
                'p_name': p_name,
                'store_id': store_id,
                'store_name': store_name,
                'total_machine_quantities': inventory_number,
                'in_stock': in_stock
            }
            inventory_list.append(v_list)
    else:
        product_list = get_all_products()
        for product in product_list:
            code = product['product_code']
            c_name = product['category_name']
            p_name = product['name']
            booked_item = get_today_inventory(code, store_id)['COUNT(product_code)']
            print(booked_item)
            total_machine_quantities = count_national_machine_quantities(code)
            inventory_number = total_machine_quantities['COUNT(product_code)']
            in_stock = inventory_number - booked_item
            v_list = {
                'product_code': code,
                'c_name': c_name,
                'p_name': p_name,
                'total_machine_quantities': inventory_number,
                'in_stock': in_stock
            }
            inventory_list.append(v_list)
    return render_template('staff_product/inventory.html', inventory_list=inventory_list, product_list=product_list,
                           product_code=product_code, category_list=category_list, category_code=category_code,
                           product_name=product_name, store_list=store_list, store_name = store_name)


# def get_all_products():
#     sql = '''SELECT DISTINCT p.*,c.`name` AS category_name, m.store_id FROM product p
#             INNER JOIN category c ON p.category_code = c.category_code
#             INNER JOIN machine m ON p.product_code=  m.product_code; '''
#     cursor = db.get_cursor()
#     cursor.execute(sql)
#     return cursor.fetchall()
def get_all_products():
    sql = '''SELECT DISTINCT p.*,c.`name` AS category_name, m.product_code FROM product p 
            INNER JOIN category c ON p.category_code = c.category_code 
            INNER JOIN machine m ON p.product_code=  m.product_code; '''
    cursor = db.get_cursor()
    cursor.execute(sql)
    all_products = cursor.fetchall()
    return all_products


def get_products(product_code=None, category_code=None, product_name=None, store_id=None):
    params = []
    sql = '''SELECT DISTINCT p.*,c.`name` AS category_name, m.store_id FROM product p 
            INNER JOIN category c ON p.category_code = c.category_code 
            INNER JOIN machine m ON p.product_code=  m.product_code'''
    if product_code:
        sql += ' AND p.product_code LIKE %s'
        params.append(f'%{product_code}%')
    if category_code:
        sql += ' AND p.category_code = %s'
        params.append(category_code)
    if product_name:
        sql += ' AND p.name LIKE %s'
        params.append(f'%{product_name}%')
    if store_id:
        sql += ' AND m.store_id = %s'
        params.append(store_id)

    sql += ' ORDER BY category_name;'
    cursor = db.get_cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()

def get_today_inventory(product_code=None, store_id=None):
    params = []
    selected_date = request.form.get('selected_date')
    if selected_date is None:
        selected_date = datetime.now()
    sql = '''select COUNT(product_code) from booking b
            INNER JOIN booking_item bi ON b.booking_id = bi.booking_id
            INNER JOIN machine m ON bi.machine_id = m.machine_id'''
    if product_code:
        sql += ' AND product_code = %s'
        params.append(product_code)
    if store_id:
        sql += ' AND m.store_id = %s'
        params.append(store_id)
    sql += ' WHERE %s BETWEEN hire_from AND hire_to;'
    params.append(selected_date)
    cursor = db.get_cursor()
    cursor.execute(sql, params)
    number = cursor.fetchone()
    return number


def get_category():
    sql = 'SELECT * FROM category ORDER BY name;'
    cursor = db.get_cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def count_machine_quantities(product_code, store_id):
    sql = '''SELECT COUNT(product_code) FROM machine WHERE product_code = %s and store_id = %s;'''
    cursor = db.get_cursor()
    cursor.execute(sql, (product_code, store_id,))
    number = cursor.fetchone()
    print(number)
    return number


def count_national_machine_quantities(product_code):
    sql = '''SELECT COUNT(product_code) FROM machine WHERE product_code = %s;'''
    cursor = db.get_cursor()
    cursor.execute(sql, (product_code,))
    number = cursor.fetchone()
    return number


def count_booked_machine_quantities(product_code, store_id):
    sql = '''SELECT COUNT(product_code) FROM machine WHERE product_code = %s and store_id = %s;'''
    cursor = db.get_cursor()
    cursor.execute(sql, (product_code, store_id,))
    return cursor.fetchall()


def get_booked_item():
    sql = ''' SELECT b.*, bi.* FROM booking b
              INNER JOIN booking_item bi ON b.booking_id = bi.booking_id;'''
    cursor = db.get_cursor()
    cursor.execute(sql)
    return cursor.fetchall()

