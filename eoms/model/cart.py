from eoms.model.db import get_cursor
from flask import jsonify, abort
from mysql.connector import Error

# Module to hanlde queries related to cart and cart_item table

# Return a shopping cart by cart_id
def get_cart_by_id(cart_id):
    cursor = get_cursor()
    query = """
            SELECT * FROM cart
            WHERE cart_id = %(cart_id)s;
            """
    cursor.execute(query, {'cart_id': cart_id})
    return cursor.fetchone()

# Return a shopping cart by customer_id
def get_cart_by_customer_id(customer_id):
    cursor = get_cursor()
    query = """
            SELECT * FROM cart
            WHERE customer_id = %(customer_id)s;
            """
    cursor.execute(query, {'customer_id': customer_id})
    return cursor.fetchone()

# Insert a shopping cart, optional parameter customer_id
def add_cart(customer_id=None):
    cursor = get_cursor()
    query = """
            INSERT INTO cart (customer_id)
            VALUES (%(customer_id)s);
            """
    cursor.execute(query, {'customer_id': customer_id})
    if cursor.rowcount == 1:
        return cursor.lastrowid
    else:
        return None


# Return a list of cart items by cart id
def get_cart_items_by_cart_id(cart_id):
    connection  = get_cursor()
    query = """
            SELECT c.*, 
            p.name, 
            p.image,
            (CEIL(DATEDIFF(c.hire_to, c.hire_from)) * c.hire_rate * c.qty) AS original_subtotal,
            ROUND((CEIL(DATEDIFF(c.hire_to, c.hire_from)) * c.hire_rate * c.qty * (c.disc_rate / 100)), 2) as discount,
            ROUND((CEIL(DATEDIFF(c.hire_to, c.hire_from)) * c.hire_rate * c.qty * (1 - c.disc_rate / 100)), 2) as subtotal
            FROM cart_item c
            INNER JOIN product p ON c.product_code = p.product_code
            WHERE cart_id = %(cart_id)s
            ORDER BY c.line_num;
            """
    connection.execute(query, {'cart_id': cart_id})
    return connection.fetchall()

# Return a cart item by cart item id
def get_cart_item_by_id(cart_item_id):
    connection  = get_cursor()
    query = """
            SELECT c.*, 
            p.name, 
            (CEIL(DATEDIFF(c.hire_to, c.hire_from)) * c.hire_rate * c.qty) AS original_subtotal,
            ROUND((CEIL(DATEDIFF(c.hire_to, c.hire_from)) * c.hire_rate * c.qty * (c.disc_rate / 100)), 2) as discount,
            ROUND((CEIL(DATEDIFF(c.hire_to, c.hire_from)) * c.hire_rate * c.qty * (1 - c.disc_rate / 100)), 2) as subtotal
            FROM cart_item c
            INNER JOIN product p ON c.product_code = p.product_code
            WHERE cart_item_id = %(cart_item_id)s;
            """
    connection.execute(query, {'cart_item_id': cart_item_id})
    return connection.fetchone()

# Add a product to shopping cart
def add_cart_items(cart_id, product_code, qty, hire_from, hire_to):
    try:
        cursor = get_cursor()
        query = """
                SET @line_num = (
                    SELECT IFNULL(MAX(line_num), 0) + 1
                    FROM cart_item
                    WHERE cart_id = %(cart_id)s
                );

                SET @hire_rate = (
                    SELECT price_a
                    FROM product
                    WHERE product_code = %(product_code)s
                );

                INSERT INTO cart_item (cart_id, product_code, qty, line_num, hire_rate, hire_from, hire_to)
                VALUES (%(cart_id)s, %(product_code)s, %(qty)s, @line_num, @hire_rate, %(hire_from)s, %(hire_to)s);
                """
        cursor.execute(
            query, 
            {
                'cart_id': cart_id,
                'product_code': product_code,
                'qty': qty,
                'hire_from' :hire_from,
                'hire_to': hire_to
            }
        )
        return {'status': 'success', 'message': 'Equipment has been added to cart'}
    except Error as e:
        return {'status': 'fail', 'message': str(e)}
    finally:
        if cursor:
            cursor.close()

# Delete a cart item by cart_item_id
def delete_cart_item_by_id(cart_item_id):
    try:
        connection  = get_cursor()
        query = """
                DELETE FROM cart_item
                WHERE cart_item_id = %(cart_item_id)s;
                """
        connection.execute(query, {'cart_item_id': cart_item_id})
        if connection.rowcount == 0:
            return {'status': 'fail', 'message': 'Cart item not found'}
        else:
            return {'status': 'success', 'message': 'Cart item deleted sucessfully'}
    except Error as e:
        return {'status': 'fail', 'message': str(e)}
    finally:
        if connection:
            connection.close()

# Remove any cart items hire date of which is in the past
def delete_outdated_cart_items_by_cart_id(cart_id):
    try:
        cursor = get_cursor()
        query = """
                DELETE FROM cart_item
                WHERE cart_id = %(cart_id)s
                AND hire_from < NOW()
                ;
                """
        cursor.execute(query, {'cart_id': cart_id})
        return cursor.rowcount
    finally:
        if cursor:
            cursor.close()

# Update cart item qty, hire_from, hire_to  by cart item id
# update_cart_item_by_id(cart_item_id, qty=None, hire_from=None, hire_to=None)
def update_cart_item_by_id(cart_item_id, **kwargs):
    # Only allow updating qty, hire_from, hire_to fields
    allowed_params = ['qty', 'hire_from', 'hire_to']
    connection  = get_cursor()
    query = "UPDATE cart_item SET "
    # List to hold the parts of the update query
    update_parts = []
    for key, value in kwargs.items():
        # Check if keyword argument is allowed
        if key in allowed_params:
            update_parts.append(f"{key} = '{value}'")
    # Join the update parts into a single string
    update_string = ", ".join(update_parts)
    # Complete the query
    query += update_string
    query += " WHERE cart_item_id = %(cart_item_id)s;"
    connection.execute(query, {'cart_item_id': cart_item_id})

# Calculate original total, total dicount, and discounted total for given cart items
def get_cart_items_totals(cart_items: dict):
    original_total = round(sum(item['original_subtotal'] for item in cart_items), 2)
    total_discount = round(sum(item['discount'] for item in cart_items), 2)
    cart_total = round(sum(item['subtotal'] for item in cart_items), 2)
    total_gst =  round(cart_total * 3 / 23, 2)
    return original_total, total_discount, cart_total, total_gst

# Apply discount to eligible cart items and return the number of rows affected
def apply_promo_to_cart(cart_id, promo_code):
    cursor = get_cursor()
    try:
        query = """
            UPDATE cart_item ci
            JOIN (
                SELECT pp.product_code, p.disc_rate
                FROM promo_product pp
                JOIN promotion p ON pp.promo_code = p.promo_code
                WHERE p.promo_code = %(promo_code)s 
                AND p.start_date <= NOW() 
                AND p.end_date >= NOW()
                AND p.status = 1
            ) AS promo
            ON ci.product_code = promo.product_code
            SET ci.disc_rate = promo.disc_rate
            WHERE ci.cart_id = %(cart_id)s
            ;
            """
        cursor.execute(
        query, 
        {
            'cart_id': cart_id,
            'promo_code': promo_code,
            }
        )
        rowcount = cursor.rowcount
        if rowcount > 0:
            query = """
            UPDATE cart
            SET promo_code = %(promo_code)s
            WHERE cart_id = %(cart_id)s
            ;
            """
            cursor.execute(
            query, 
            {
                'cart_id': cart_id,
                'promo_code': promo_code,
                }
            )
    finally:
        cursor.close()
    return rowcount

# Delete promo from cart and cart items
def delete_promo_by_cart_id(cart_id):
    cursor = get_cursor()
    try:
        cursor.execute("START TRANSACTION;")
        # Remove promo from cart
        query = """
                UPDATE cart
                SET promo_code = Null
                WHERE cart_id = %(cart_id)s;
                
                """
        cursor.execute(
            query, 
            {
                'cart_id': cart_id,
            }
        )
        rowcount = cursor.rowcount
        # Remove discount from cart items
        query = """
                UPDATE cart_item
                SET disc_rate = 0
                WHERE cart_id = %(cart_id)s;
                """
        cursor.execute(
            query, 
            {
                'cart_id': cart_id,
            }
        )
        rowcount += cursor.rowcount
        cursor.execute("COMMIT;")
    except Error as e:
        cursor.execute("ROLLBACK;")
        raise e
    finally:
        cursor.close()
    return rowcount