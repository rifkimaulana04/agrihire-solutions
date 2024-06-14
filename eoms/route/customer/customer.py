from eoms import app
from flask import render_template, redirect, request, flash, url_for,session,jsonify
from eoms.model import db
from datetime import datetime
from eoms.form.booking_form import BookingForm
from eoms.model.session_utils import allow_role
from eoms.model.booking import get_my_current_booking, get_bookingItemList, get_my_current_booking_notEarlyToday, cancel_booking_byuserIdAndBookingId, extend_booking_period
from eoms.model.message import add_new_message_BycustomerID,add_new_notification
import json


@app.route('/mybooking', methods=['GET', 'POST'])
def mybooking():
    allow_role(['customer'])

    user_id = session["user_id"]
    
    form = BookingForm(request.form)

    booking_list = get_my_current_booking_notEarlyToday(user_id)
    allBookingList = {}
    for booking in booking_list:
        booking_items = get_bookingItemList(booking['booking_id'])
        if not booking_items:
            booking_items = []
        allBookingList[booking['booking_id']] = {
            'create_date': booking['create_date'],
            'status': booking['status'],
            'booking_items': booking_items
        }
    return render_template('customer/mybooking.html', booking_list = booking_list, allBookingList = allBookingList, form = form)

@app.route('/allbooking', methods=['GET', 'POST'])
def allbooking():
    allow_role(['customer'])

    user_id = session["user_id"]


    booking_list = get_my_current_booking(user_id)
    allBookingList = {}
    for booking in booking_list:
        booking_items = get_bookingItemList(booking['booking_id'])
        if not booking_items:
            booking_items = []
        allBookingList[booking['booking_id']] = {
            'create_date': booking['create_date'],
            'status': booking['status'],
            'booking_items': booking_items
        }
    return render_template('customer/allbooking.html', booking_list = booking_list, allBookingList = allBookingList)


@app.route('/cancelBooking/<int:id>', methods=['GET', 'POST'])
def cancelbooking(id):
    allow_role(['customer'])
    user_id = session["user_id"]

    cancel_booking_byuserIdAndBookingId(user_id,id)
    return redirect(url_for('mybooking'))

@app.route('/extendperiod/<int:id>', methods=['GET', 'POST'])
def extendperiod(id):
    allow_role(['customer'])
    if request.method == 'POST' :
        hire_to = request.form.get('hire_to')
        extend_price = request.form.get('total')
        extend_booking_period(hire_to, id)
        booking_id = request.form.get('booking_id')
        update_payment(extend_price,booking_id)
        return redirect(url_for('mybooking'))
        
@app.route('/message', methods=['GET', 'POST'])
def message():
    allow_role(['customer'])

    user_id = session["user_id"]
    cursor = db.get_cursor()
    sql = 'SELECT * FROM customer WHERE user_id=%s;'
    cursor.execute(sql,(user_id,))
    profile = cursor.fetchone()
    sql3 = 'SELECT * FROM store;'
    cursor.execute(sql3)
    storeList = cursor.fetchall()
    sql4 = 'SELECT * FROM message WHERE customer_id = %s;'
    cursor.execute(sql4,(user_id,))
    message_list = cursor.fetchall()
            
    if request.method == 'POST' :
        customer_id = request.form.get('customer_id')
        subject = request.form.get('subject')
        content = request.form.get('content')
        store_id = request.form.get('store_id')
        # Get today's date without time part
        time = datetime.now()
        response = add_new_message_BycustomerID(customer_id,subject,content,time, store_id)
        if response.json['success']:
            message_id = response.json['message_id']
            add_new_notification(message_id, store_id, time)
        
        response_json = response.get_json()
        msg = response_json.get('message')
        
        return render_template('customer/message.html', profile=profile,  storeList=storeList, msg=msg)
    else:
        return render_template('customer/message.html', profile=profile,  storeList=storeList, message_list = message_list)

@app.route('/customer_read_message', methods=['GET', 'POST'])
def customer_read_message():
    allow_role(['customer'])
    msgId = request.form[ 'id' ]
    cursor = db.get_cursor()
    sql =  """SELECT * FROM message 
            JOIN customer ON customer.customer_id = message.customer_id
            WHERE message_id=%s;"""
    cursor.execute(sql,(msgId,))
    msgList = cursor.fetchone()
    sql = "UPDATE message SET status = 2 WHERE message_id = %(msgId)s"
    cursor.execute(sql,{
        'msgId':   msgId,
        })
    cursor.fetchone()
    return jsonify({'htmlresponse': render_template('messagedetail.html',msgList = msgList, msgId=msgId)})


def update_payment(extend_price,booking_id):
    cursor = db.get_cursor()
    sql = """UPDATE booking SET total = (total + %s) WHERE booking_id = %s"""
    cursor.execute(sql, (extend_price, booking_id))
    cursor.fetchone()
    return cursor.rowcount
  