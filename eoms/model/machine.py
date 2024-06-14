from eoms.model.db import get_cursor
from flask import jsonify, abort

# Module to handle requey related to machine table

# Function to check stock availablitiy
# Return the number of avaliable machines for a given product and date range
def get_available_machines_by_code_store_date_range(product_code, store_id, date_from, date_to):
    connection  = get_cursor()
    query = """
            SELECT * FROM machine
            WHERE product_code = %(product_code)s
            AND store_id = %(store_id)s
            AND status = 1
            AND machine_id NOT IN (
                SELECT machine_id 
                FROM booking_item
                WHERE hire_from < %(date_from)s
                AND hire_to > %(date_to)s
            )
            AND machine_id NOT IN (
                SELECT machine_id
                FROM service
                WHERE service_date BETWEEN %(date_from)s AND %(date_to)s
            );
            """
    connection.execute(
        query, 
        {
            'product_code': product_code,
            'store_id': store_id,
            'date_from': date_from,
            'date_to': date_to
        }
    )
    available_machines = connection.fetchall()
    return available_machines


def get_machine_by_booking_item_ID(booking_item_id):
    connection  = get_cursor()
    query = """
            SELECT * FROM booking_item
            WHERE booking_item_id = %(booking_item_id)s;
            """
    connection.execute(
        query, 
        {
            'booking_item_id': booking_item_id,
        }
    )
    return connection.fetchone()
