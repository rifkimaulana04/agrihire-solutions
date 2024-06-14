from eoms import app
from flask import render_template, redirect, request, flash, url_for,session
from eoms.model import db
from eoms.model.session_utils import allow_role
import bcrypt

# View and update profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    allow_role(['customer', 'staff', 'lmgr', 'nmgr', 'admin'])
    # Retreive current user id and role from session
    user_id = session['user_id']
    role = session['role']
    # When user submites the form, update user profile
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        # email = request.form.get('email')
        phone = request.form.get('phone')
        address_line1 = request.form.get('address1')
        address_line2 = request.form.get('address2')
        suburb = request.form.get('suburb')
        city = request.form.get('city')
        post_code = request.form.get('post_code')
        position = request.form.get('position')

        if role == 'customer':
            cursor = db.get_cursor() 
            customer_id = session['customer_id']
            sql='''UPDATE customer 
            SET first_name=%s, last_name=%s, phone=%s, address_line1=%s, address_line2=%s, suburb=%s, city=%s, post_code=%s 
            WHERE customer_id=%s;'''
            cursor.execute(sql,(first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, customer_id))
            flash('Update successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            staff_id = session['staff_id']
            cursor = db.get_cursor() 
            sql='UPDATE staff SET first_name=%s, last_name=%s, position=%s, phone=%s WHERE staff_id=%s;'
            cursor.execute(sql,(first_name, last_name, position, phone, staff_id))
            flash('Update successfully!', 'success')
            return redirect(url_for('profile'))

    else:
        if role == 'customer':
            cursor = db.get_cursor()
            sql = 'SELECT * FROM customer WHERE user_id=%s;'
            cursor.execute(sql,(user_id,))
            profile = cursor.fetchone()
            return render_template('profile/profile.html', profile = profile) 
        else:
            cursor = db.get_cursor()
            sql = 'SELECT * FROM staff WHERE user_id=%s;'
            cursor.execute(sql,(user_id,))
            profile = cursor.fetchone()
            return render_template('profile/profile.html', profile = profile)
        

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    msg = ''  
    allow_role(['customer', 'staff', 'lmgr', 'nmgr', 'admin'])
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if the current password is correct
        cursor = db.get_cursor()
        cursor.execute('SELECT password FROM user WHERE user_id = %s', (session.get('user_id'),))
        row = cursor.fetchone()
        if row:
            user_bytes = current_password.encode('utf-8')
            user_password = row['password'].encode('utf-8')
            if bcrypt.checkpw(user_bytes, user_password):
                # Check if the new password and confirm password match
                if new_password == confirm_password:
                    # Check if the new password is different from the current password
                    if new_password != current_password:
                        # Update the password
                        bytes = new_password.encode('utf-8') 
                        # generating the salt 
                        salt = bcrypt.gensalt() 
                        # Hashing the password 
                        hashed_password = bcrypt.hashpw(bytes, salt) 
                        cursor.execute('UPDATE user SET password=%s WHERE user_id = %s', (hashed_password, session.get('user_id')))
                        # Commit the transaction
                        db.connection.commit()
                        flash('Password updated successfully!', 'success')
                        # return redirect(url_for('dashboard'))
                    else:
                        msg = 'New password must be different from the current password.'
                else:
                    msg = 'New password and confirmation password do not match.'
            else:
                msg = 'Incorrect current password.'
    return render_template('profile/change_password.html', msg = msg)