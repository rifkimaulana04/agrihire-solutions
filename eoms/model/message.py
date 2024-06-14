from flask import jsonify, abort
from datetime import datetime
import eoms.model.db as db
from eoms.model.db import get_cursor


def add_new_message_BycustomerID(customer_id,subject,content,time,store_id):
    cursor = db.get_cursor()
    query = """INSERT INTO message (`customer_id`, `store_id`, `subject`, `content`, `create_date`) 
            VALUES  (%(customer_id)s, %(store_id)s, %(subject)s, %(content)s, %(create_date)s);
            """
    cursor.execute(
        query, 
        {
            "customer_id": customer_id,
            "store_id": store_id,
            "subject": subject,
            "content": content,
            "create_date": time,
        }
    )
    if cursor.rowcount == 1:
        message_id = cursor.lastrowid
        return jsonify({'success': True, 'message': 'Success!', 'message_id': message_id})
    else:
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500
    
def reply_message(message_id,content,time):
    cursor = db.get_cursor()
    query = """UPDATE message 
                SET reply = %(content)s, reply_date = %(create_date)s, status = 0
                WHERE message_id = %(message_id)s;
            """
    cursor.execute(
        query, 
        {
            "message_id": message_id,
            "content": content,
            "create_date": time,
        }
    )
    if cursor.rowcount == 1:
        return jsonify({'success': True, 'message': 'Success!'})
    else:
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500
    
def add_new_notification(message_id, store_id, time):
    cursor = db.get_cursor()
    query = """INSERT INTO notifications (`message_id`, `store_id`, `create_date`, `is_read`)
                VALUE (%(message_id)s,%(store_id)s,%(create_date)s,%(is_read)s);
            """
    cursor.execute(
        query, 
        {
            "message_id": message_id,
            "store_id": store_id,
            "create_date": time,
            "is_read": False,
        }
    )
    if cursor.rowcount == 1:
        return jsonify({'success': True, 'message': 'Success!'})
    else:
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500
    
# Return a list of cart items by cart id
def get_notification_by_user_id(user_id):
    connection  = get_cursor()
    query = """
            SELECT * FROM message
            WHERE customer_id = %(user_id)s AND status = 0;
            """
    connection.execute(query, {'user_id': user_id})
    return connection.fetchall()