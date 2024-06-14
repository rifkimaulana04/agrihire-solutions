from eoms import app
from flask import render_template, redirect, request, flash, url_for, session, jsonify
from eoms.form.login_form import LoginForm
from eoms.form.registration_form import RegistrationForm
from eoms.model import auth
from eoms.model.session_utils import allow_role, logged_in
from eoms.model import db
from eoms.model.booking import get_bookingList_by_date, get_bookingItemList_by_id, confirm_check_out, record_check_out
from eoms.model.product import select_all_from_product, add_new_equipment
from eoms.model.store import select_all_from_store, get_store_by_code
from eoms.model.upload import upload_image_by_product_code
from eoms.model.message import reply_message
from eoms.model.machine import get_machine_by_booking_item_ID
from datetime import datetime

@app.route('/dashboard')
def dashboard():
    allow_role(['staff', 'lmgr', 'nmgr', 'admin'])
    user_id = session['user_id']
    cursor = db.get_cursor()
    sql = 'SELECT * FROM staff left JOIN store ON store.store_id = staff.store_id WHERE user_id=%s;'
    cursor.execute(sql,(user_id,))
    user = cursor.fetchone()
    session['staff_id'] = user['staff_id']
    session['store_id'] = user['store_id']
    session['store_name'] = user['store_name']
    
    return render_template('dashboard/dashboard.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    allow_role(['staff', 'lmgr', 'nmgr', 'admin'])
    date = datetime.now().strftime('%Y-%m-%d')
    user_id = session['user_id']
    bookingList = get_bookingList_by_date(date)
    booking_id_list = [booking['booking_id'] for booking in bookingList]
    bookingItemList = get_bookingItemList_by_id(booking_id_list,date)
    if request.method == 'POST':
        booking_item_id = request.form.get('id')
        machine = get_machine_by_booking_item_ID(booking_item_id)
        confirm_check_out(machine['machine_id'])
        record_check_out(booking_item_id,user_id)
        return jsonify({'status': 'success', 'message': 'Checkout confirmed'})
    return render_template('dashboard/equipments_list.html' , bookingList=bookingList, bookingItemList=bookingItemList, date=date)

@app.route('/addnew', methods=['GET', 'POST'])
def addNewEquipment():
    allow_role(['staff', 'lmgr', 'nmgr', 'admin'])
    productList = select_all_from_product()
    storeList = select_all_from_store()
    if session['store_id']:
        store_id = session['store_id']
        store = get_store_by_code(store_id)
    if request.method == 'POST':
        product_code = request.form.get('product_code')
        sn = request.form.get('sn')
        store_id = request.form.get('store_id')
        purchase_date = request.form.get('purchase_date')
        cost = request.form.get('cost')
        image = request.files.get('upload_image')
        machine_id  = add_new_equipment(
            product_code,
            sn,
            store_id,
            purchase_date,
            cost
        )
        if image:
            upload_image_by_product_code(machine_id,product_code, image)
        msg = "Your have added new equipment successfully!"
        return render_template('dashboard/addnew_equipment.html', msg = msg , productList = productList, storeList=storeList, store = store)
    return render_template('dashboard/addnew_equipment.html', productList = productList, storeList=storeList, store = store)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    allow_role(['staff'])
    user_id = session["user_id"]
    cursor = db.get_cursor()
    sql = 'SELECT * FROM staff WHERE user_id=%s;'
    cursor.execute(sql,(user_id,))
    profile = cursor.fetchone()
    sql2 =  """SELECT * FROM message 
            JOIN customer ON customer.customer_id = message.customer_id
            WHERE message.store_id=%s;"""
    cursor.execute(sql2,(profile['store_id'],))
    messageList = cursor.fetchall()
    if request.method == 'POST' :
        msgId = request.form[ 'id' ]
        cursor = db.get_cursor()
        sql3 =  """SELECT * FROM message 
                JOIN customer ON customer.customer_id = message.customer_id
                WHERE message_id=%s;"""
        cursor.execute(sql3,(msgId,))
        msgList = cursor.fetchone()
        return jsonify({'htmlresponse': render_template('messagedetail.html',msgList = msgList, msgId=msgId)})
    return render_template('dashboard/messages.html' , messageList=messageList)

@app.route('/submitMsg', methods=['GET', 'POST'])
def submitMsg():
    allow_role(['staff'])
    message_id = request.form[ 'id' ]
    content = request.form[ 'content' ]
    # Get today's date without time part
    time = datetime.now()
    reply_message(message_id,content,time)
    # update the notification
    update_notification(message_id)
    return redirect(url_for('messages'))

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    user_id = session['user_id']
    cursor = db.get_cursor()
    sql = 'SELECT * FROM staff WHERE user_id=%s;'
    cursor.execute(sql,(user_id,))
    user = cursor.fetchone()
    sql = 'SELECT * FROM notifications WHERE store_id=%s AND is_read = 0;'
    cursor.execute(sql,(user['store_id'],))
    notifications = cursor.fetchall()
    unread_count = len(notifications)
    return jsonify({'response': unread_count})


@app.route('/equipment_checkout_day', methods=['GET', 'POST'])
def equipment_checkout_day():
    allow_role(['staff', 'lmgr', 'nmgr', 'admin'])
    bookingItemList = []
    if request.method == 'POST':
        date = request.form.get('date')
        bookingList = get_bookingList_by_date(date)
        booking_id_list = [booking['booking_id'] for booking in bookingList]
        bookingItemList = get_bookingItemList_by_id(booking_id_list,date)
    return render_template('dashboard/equipments_list.html' , bookingList=bookingList, bookingItemList=bookingItemList, date=date)
    

def update_notification(message_id):
    cursor = db.get_cursor()
    sql = 'UPDATE notifications SET is_read = 1 WHERE message_id = %(message_id)s;'
    cursor.execute(sql,{
        'message_id':   message_id,
        })
    cursor.fetchone()
    if cursor.rowcount == 1:
        return jsonify({'success': True, 'message': 'Success!'})
    else:
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500