from eoms import app
from flask import render_template, redirect, request, flash, url_for,session,jsonify
from eoms.model import db
from eoms.model.session_utils import allow_role
import json
import bcrypt

# store list view  
@app.route('/admin/stores', methods=['GET', 'POST'])
def stores():
    allow_role(['nmgr', 'admin'])
    store_name = request.form.get('store_name', '').strip()
    store_list = get_stores(store_name)
    return render_template('administration/stores.html', store_list = store_list, store_name = store_name)

# store add and edit   
@app.route('/manage_store', methods=['POST'])
def manage_store():
    allow_role(['nmgr', 'admin'])
    store_id = request.form['store_id']
    store_name = request.form['store_name'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()
    address_line1 = request.form['address_line1'].strip()
    address_line2 = request.form['address_line2'].strip()
    suburb = request.form['suburb'].strip()
    city = request.form['city'].strip()
    post_code = request.form['post_code'].strip()
    response = None


    # Check if the store already exists to decide between add or edit
    if store_id:
        if not check_exist_store(store_name, store_id):
            response = update_store(store_id, store_name, phone, email, address_line1, address_line2, suburb, city, post_code)
        else:
            response = {'success': False, 'message': 'Store Name Exists'}
            return jsonify(response)
            
    else:
        if not check_exist_store(store_name):
            response = add_store(store_name, phone, email, address_line1, address_line2, suburb, city, post_code)
        else:
            response = {'success': False, 'message': 'Store Name Exists'}
            return jsonify(response)

    if response['success']:
        flash(response['message'], 'success')
    else:
        flash(response['message'], 'danger')
        
    return jsonify(response)

# store delete
@app.route('/delete_store', methods=['POST'])
def delete_store():
    store_id = request.form['store_id']
    response = delete_store_by_id(store_id)
    if response['success']:
        flash(response['message'], 'success')
    else:
        flash(response['message'], 'danger')
    return redirect(url_for('stores'))




# staff management 
@app.route('/staff', methods=['GET', 'POST'])
def staff():
    allow_role(['lmgr','nmgr', 'admin'])
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    role = session['role'] 
    if role == 'lmgr':
          store_id = session['store_id'] 
    else:
         store_id = request.form.get('store_id', '').strip()
    staff_list = get_staff(first_name, last_name, store_id)
    store_list = get_stores()
    return render_template('administration/staff.html', staff_list = staff_list, 
                            store_list =store_list, first_name = first_name,
                            last_name = last_name, store_id = store_id)

@app.route('/manage_staff', methods=['POST'])
def manage_staff():
    allow_role(['lmgr', 'nmgr', 'admin'])
    staff_id = request.form['staff_id'].strip()
    first_name = request.form['first_name'].strip()
    last_name = request.form['last_name'].strip()
    phone = request.form['phone'].strip()
    position = request.form['position'].strip()
    status = request.form['status'].strip()
    role = request.form['role'].strip()
    email = request.form['email'].strip()
    is_active = int(status)
    login_role = session['role']
    if login_role == 'lmgr':
            store_id = session['store_id']
    else:
        store_id = request.form['store_id'].strip()
    user_id = request.form['user_id'].strip()
    email = request.form['email'].strip()
    response = None
    # Check if the staff already exists to decide between add or edit
    if staff_id:
        response = update_staff(staff_id, store_id, first_name, last_name, position, phone, role, is_active, user_id) 
    else:
        user_id = get_max_user_id()
        default_pwd = 'Test1234!'
        hashed_password = bcrypt.hashpw(default_pwd.encode('utf-8'), bcrypt.gensalt())
        response = add_staff(user_id, email, hashed_password, role, is_active, store_id, first_name, last_name, position, phone)


    if response['success']:
        flash(response['message'], 'success')
    else:
        flash(response['message'], 'danger')
        
    return jsonify(response)




# customer management 
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    allow_role(['staff','lmgr','nmgr', 'admin'])
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    role = session['role'] 
    if role == 'staff' or role == 'lmgr':
          store_id = session['store_id'] 
    else:
         store_id = request.form.get('store_id', '').strip()
    customer_list = get_customers(first_name, last_name, store_id)
    store_list = get_stores()
    return render_template('administration/customers.html', customer_list = customer_list, 
                            store_list =store_list, first_name = first_name,
                            last_name = last_name, store_id = store_id)


@app.route('/manage_customer', methods=['POST'])
def manage_customer():
    allow_role(['lmgr', 'nmgr', 'admin'])
    customer_id = request.form['customer_id'].strip()
    first_name = request.form['first_name'].strip()
    last_name = request.form['last_name'].strip()
    phone = request.form['phone'].strip()
    address_line1 = request.form['address_line1'].strip()
    address_line2 = request.form['address_line2'].strip()
    suburb = request.form['suburb'].strip()
    city = request.form['city'].strip()
    post_code = request.form['post_code'].strip()
    status = request.form['status'].strip()
    is_active = int(status)
    user_id = request.form['user_id'].strip()
    response = update_customer(customer_id, first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, is_active, user_id)

    if response['success']:
        flash(response['message'], 'success')
    else:
        flash(response['message'], 'danger')
        
    return jsonify(response)







# business method
def get_stores(store_name = None):
      params = []
      sql = 'SELECT * FROM store WHERE 1=1'    
      if store_name:
            sql += ' AND store_name LIKE %s'
            params.append(f'%{store_name}%')     
      sql += ' ORDER BY store_name;'     
      cursor = db.get_cursor()   
      cursor.execute(sql, params)  
      return cursor.fetchall() 

def add_store(store_name, phone, email, address_line1, address_line2, suburb, city, post_code):
    try:
        sql = 'INSERT INTO store (store_name, phone, email, address_line1, address_line2, suburb, city, post_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s );'    
        cursor = db.get_cursor()    
        cursor.execute(sql,(store_name, phone, email, address_line1, address_line2, suburb, city, post_code))  
        return {'success': True, 'message': 'Store added successfully'}
    except Exception as err:
        return {'success': False, 'message': 'Something went wrong'}  
         
def update_store(store_id, store_name, phone, email, address_line1, address_line2, suburb, city, post_code):
    try:
        sql = 'UPDATE store SET store_name = %s, phone = %s, email = %s, address_line1 = %s, address_line2 = %s, suburb = %s, city = %s, post_code = %s WHERE store_id = %s;'
        cursor = db.get_cursor()
        cursor.execute(sql, (store_name, phone, email, address_line1, address_line2, suburb, city, post_code, store_id))
        return {'success': True, 'message': 'Store Updated Successfully'}
    except Exception as err:
        return {'success': False, 'message': 'Somethings Wrong'}

def delete_store_by_id(store_id):
    try:
        sql = 'DELETE from store WHERE store_id=%s;'     
        cursor = db.get_cursor()   
        cursor.execute(sql, (store_id,))  
        return {'success': True, 'message': 'Store Deleted Successfully'}
    except Exception as err:
         if 'FOREIGN KEY' in str(err):
            return {'success': False, 'message': 'This store is in use. It can not be deleted!'}    
         else:
            return {'success': False, 'message': 'Somethings Wrong'}   

def check_exist_store(store_name, store_id = None):
    params = []
    sql = 'SELECT COUNT(*) AS NUM FROM store WHERE store_name = %s'   
    params.append(store_name)  
    if store_id:
        sql +='AND store_id != %s' 
        params.append(store_id)   
    cursor = db.get_cursor()   
    cursor.execute(sql, params)  
    count = cursor.fetchone()['NUM']
    if count > 0:
        return True
    else:
        return False


def get_staff(first_name = None, last_name = None, store_id  = None):
     params = []
     sql = '''SELECT staff.*,store.store_name,user.email,user.is_active,user.role FROM staff 
                INNER JOIN store ON staff.store_id=store.store_id 
                INNER JOIN user ON user.user_id=staff.user_id
                WHERE 1=1'''    
     if first_name:
        sql += ' AND staff.first_name LIKE %s'
        params.append(f'%{first_name}%')
     if last_name:
        sql += ' AND staff.last_name LIKE %s'
        params.append(f'%{last_name}%')   
     if store_id:
        sql += ' AND staff.store_id = %s'
        params.append(store_id)    
     sql += ' ORDER BY staff.store_id,staff.first_name,staff.last_name;'     
     cursor = db.get_cursor()   
     cursor.execute(sql, params)  
     return cursor.fetchall() 

def get_max_user_id():
      sql = 'SELECT MAX(user_id) AS max_id FROM user;'        
      cursor = db.get_cursor()   
      cursor.execute(sql)  
      return int(cursor.fetchone()['max_id'])+1

def add_staff(user_id, email, password, role, is_active, store_id, first_name, last_name, position, phone): 
    try: 
        sql = "INSERT INTO user (user_id, email, password, role, is_active) VALUES (%s, %s, %s, %s, %s);"
        cursor = db.get_cursor()    
        cursor.execute(sql,(user_id, email, password, role ,is_active))
        sql = 'INSERT INTO staff (user_id, store_id, first_name, last_name, position, phone) VALUES (%s, %s, %s, %s, %s, %s);'    
        cursor = db.get_cursor()    
        cursor.execute(sql,(user_id, store_id, first_name, last_name, position, phone))  

        return {'success': True, 'message': 'Staff Added Successfully'}
    except Exception as err:
        return {'success': False, 'message': 'Something went wrong'}  

def update_staff(staff_id, store_id, first_name, last_name, position, phone, role, is_active, user_id): 
    try:
        sql = 'UPDATE user SET role=%s, is_active=%s WHERE user_id=%s;'
        cursor = db.get_cursor()    
        cursor.execute(sql,(role, is_active, user_id))
        sql = 'UPDATE staff SET store_id=%s,first_name = %s, last_name = %s, position = %s, phone = %s Where staff_id = %s;'    
        cursor = db.get_cursor()    
        cursor.execute(sql,(store_id, first_name, last_name, position, phone, staff_id))  
      
        return {'success': True, 'message': 'Staff Edited Successfully'}
    except Exception as err:
        return {'success': False, 'message': 'Something went wrong'}  

  
 
def get_customers(first_name = None, last_name = None, store_id  = None):
     params = []
     sql = '''SELECT c.*,s.store_name,u.email,u.is_active,u.role FROM customer c 
                INNER JOIN store s ON c.my_store=s.store_id
                INNER JOIN user u ON u.user_id=c.user_id WHERE 1=1''' 
     if first_name:
        sql += ' AND c.first_name LIKE %s'
        params.append(f'%{first_name}%')
     if last_name:
        sql += ' AND c.last_name LIKE %s'
        params.append(f'%{last_name}%')   
     if store_id:
        sql += ' AND c.my_store = %s'
        params.append(store_id)    
     sql += ' ORDER BY c.my_store,c.first_name,c.last_name;'     
     cursor = db.get_cursor()   
     cursor.execute(sql, params)  
     return cursor.fetchall() 

def add_customer(user_id, email, password, first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, store_id): 
      sql = 'INSERT INTO user (user_id, email, password, role, is_active) VALUES (%s, %s, %s, customer, 1);'
      cursor = db.get_cursor()    
      cursor.execute(sql,(user_id, email, password))
      sql = 'INSERT INTO customer (user_id, first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, my_store) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'    
      cursor = db.get_cursor()    
      cursor.execute(sql,(user_id, first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, store_id))  
      return cursor.fetchone()

def update_customer(customer_id, first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, is_active, user_id): 
    try:
      sql = 'UPDATE customer SET first_name = %s, last_name = %s, phone = %s, address_line1 = %s, address_line2 = %s, suburb = %s, city = %s, post_code = %s Where customer_id = %s;'    
      cursor = db.get_cursor()    
      cursor.execute(sql,(first_name, last_name, phone, address_line1, address_line2, suburb, city, post_code, customer_id))  
      sql = 'UPDATE user SET is_active = %s Where user_id = %s;'    
      cursor = db.get_cursor()    
      cursor.execute(sql,(is_active, user_id))  
      
      return {'success': True, 'message': 'Customer Edited Successfully'}
    except Exception as err:
        return {'success': False, 'message': 'Something went wrong'}    
 
 


   
 