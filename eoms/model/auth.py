from eoms.model.db import get_cursor
import bcrypt
from flask import session

# This module handles user authentication, i.e. login
# and any function in realation to password hashinng, i.e. register, change password

# Authenciate username ans passwor, attempt to log user in
# Return True if both username and password pass authentication
# Otherwise return False

# Check if email exists in db
def email_exists(email):
    query = """SELECT *
            FROM user
            WHERE email = %(email)s;
            """
    connection = get_cursor()
    connection.execute(
        query,
        {
            "email": email
        },
        )
    user = connection.fetchone()
    if user:
        return True
    else:
        return False

def login_by_email(email, password):
    # Query username in db user table
    query = """SELECT * 
            FROM user 
            WHERE email = %(email)s;
            """
    connection = get_cursor()
    connection.execute(
        query, 
        {
            "email": email
        },
        )
    user = connection.fetchone()
    # If user exists and is active
    if user and user.get('is_active'):
        # Check if password matches
        user_bytes = password.encode('utf-8')
        user_password = user['password'].encode('utf-8')
        if bcrypt.checkpw(user_bytes, user_password):
            session['loggedin'] = True
            session["user_id"] = user["user_id"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            # return True
            return user["role"]
    else:
        # return False
        return None

# Add a user to db, default role is customer
def add_user(email, password, first_name, last_name, role='customer'):
    # converting password to array of bytes
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    query = """INSERT INTO user (`email`, `password`, `role`) 
            VALUES  (%(email)s, %(password)s, %(role)s);
            """
    connection = get_cursor()
    connection.execute(
        query,
        {
            'email': email,
            'password': hash,
            'role': role
        }
    )
    # Check if insert is successful
    # Return new user_id if successful
    # Otherwise return False
    if connection.rowcount == 1:
        user_id = connection.lastrowid
        query = """INSERT INTO customer (`user_id`, `first_name`, `last_name`) 
                VALUES  (%(user_id)s, %(first_name)s, %(last_name)s);
                """
        connection.execute(
            query,
            {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        return user_id if connection.rowcount == 1 else False
    else:
        return False


# For the reset password feature
def update_password(email, hashed_password):
    query = """UPDATE user SET password = %(password)s WHERE email = %(email)s"""
    connection = get_cursor()
    connection.execute(
        query,
        {
            'email': email,
            'password': hashed_password
        }
    )



#Notification for booking hire
def booking_hire_notification(customer_id):
    sql = '''SELECT m.sn, bi.hire_from
            FROM `booking` b
            INNER JOIN booking_item bi ON b.booking_id = bi.booking_id
            INNER JOIN machine m ON m.machine_id = bi.machine_id
            WHERE b.customer_id = %s
            AND bi.hire_from BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 DAY)
            ORDER BY bi.hire_from;'''    
    cursor = get_cursor()   
    cursor.execute(sql, (customer_id,))
    return cursor.fetchall()

#Notification for booking return    
def booking_return_notification(customer_id):
    sql = '''SELECT m.sn,bi.hire_to
                FROM `booking` b
                INNER JOIN booking_item bi ON b.booking_id = bi.booking_id
                INNER JOIN machine m ON m.machine_id = bi.machine_id
                WHERE b.customer_id = %s
                AND bi.hire_to BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 DAY)
                ORDER BY bi.hire_to; '''
    
    cursor = get_cursor()   
    cursor.execute(sql, (customer_id,)) 
    return cursor.fetchall()
    