from eoms import app
from flask import render_template, redirect, request, flash, url_for, session
from eoms.model import category, cart, message
# This module handles global variables can be used in the base templates

# Define a context processor for categories used in navbar menu
@app.context_processor
def inject_category_options():
    category_options = category.get_all_active_categories()
    return dict(category_options=category_options)

# Define a context processor for cart item count used in navbar menu
@app.context_processor
def inject_cart_item_count():
    cart_item_count = 0
    if session.get('cart_id'):
        cart_item_count = len(cart.get_cart_items_by_cart_id(session['cart_id']))
    return dict(cart_item_count=cart_item_count)

@app.context_processor
def inject_cart_notifications_count():
    notifications_count = 0
    if session.get('customer_id'):
        notifications_count = len(message.get_notification_by_user_id(session['customer_id']))
    return dict(notifications_count = notifications_count)
