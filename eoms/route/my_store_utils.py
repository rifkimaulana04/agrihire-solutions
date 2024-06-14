from eoms import app
from flask import jsonify, request, session, redirect, url_for
from eoms.model import customer

# Module to check and update my store on customer facing pages

@app.before_request
def load_my_store():
    if 'my_store' not in session:
        if session.get('customer_id'):
            session['my_store'] = customer.get_my_store_by_customer_id(session['customer_id']).get('my_store')
        # else:
        #     session['my_store'] = None

# @app.route('/update_my_store', methods=['POST'])
# Update my store in session and customer profile
def update_my_store(store_id):
    if 'customer_id' in session:
        customer.update_my_store_by_customer_id(session["customer_id"], store_id)
    session['my_store'] = store_id

        