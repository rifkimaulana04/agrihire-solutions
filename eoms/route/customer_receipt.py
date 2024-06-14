from eoms import app
from flask import render_template
from eoms.model import db
from eoms.model.session_utils import allow_role

# view reciept
@app.route('/receipt/<int:booking_id>', methods=['GET', 'POST'])
def receipt(booking_id):
    allow_role(['customer'])
    booking_detail = get_booking_detail_by_id(booking_id)
    booking_item_list= get_booking_item_list(booking_id)
    total = get_booking_detail_by_id(booking_id)['total']
    gst = round(total * 3 / 23, 2)

    return render_template('customer/receipt.html',booking_detail= booking_detail,
                        booking_item_list = booking_item_list, gst = gst)
# 
def get_booking_detail_by_id(booking_id):
      try:
            sql = '''SELECT b.*, p.create_date AS pay_date, p.amount, c.*,
                  s.store_name, s.phone AS store_phone, s.email, s.address_line1 AS store_address_line1, 
                  s.address_line2 AS store_address_line2, 
                  s.suburb AS store_suburb, s.city AS store_city, s.post_code AS store_post_code
                  FROM booking b 
                  INNER JOIN payment p ON b.booking_id = p.booking_id
                  INNER JOIN customer c ON b.customer_id = c.customer_id
                  INNER JOIN store s ON b.store_id = s.store_id
                  WHERE b.booking_id = %s;'''    
            cursor = db.get_cursor()    
            cursor.execute(sql,(booking_id,))  
            return cursor.fetchone() 
      except Exception as err:
            return {'success': False, 'message': 'Somethings Wrong'}


def get_booking_item_list(booking_id):
      try:
            sql = '''SELECT bi.*,m.*,p.*
                  FROM booking_item bi
                  INNER JOIN machine m ON bi.machine_id = m.machine_id
                  INNER JOIN product p ON m.product_code = p.product_code
                  WHERE bi.booking_id = %s;'''    
            cursor = db.get_cursor()    
            cursor.execute(sql,(booking_id,))  
            return cursor.fetchall() 
      except Exception as err:
            return {'success': False, 'message': 'Somethings wrong'} 