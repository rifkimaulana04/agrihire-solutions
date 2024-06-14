import bcrypt
from eoms import app
from flask import render_template, redirect, request, flash, url_for, session
from eoms.form.login_form import LoginForm
from eoms.form.registration_form import RegistrationForm
from eoms.form.reset_password_form import ResetPasswordForm, ResetPasswordConfirmForm
from eoms.model import auth, customer, staff, cart, cart_utils, mail, token_utils
from eoms.model.session_utils import allow_role, logged_in, check_user_role_staff, check_user_role_lmgr, check_user_role_nmgr, check_user_role_admin
from eoms.const import STAFF_ROLE_LIST

# Routes for user registration, login, and logout
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = auth.add_user(form.email.data, form.password.data, form.first_name.data, form.last_name.data)
        if user_id:
            # Fetach customer_id and insert shopping cart
            customer_id = customer.get_customer_by_user_id(user_id).get('customer_id')
            cart.add_cart(customer_id)
            flash('Thanks for registering', 'success')
            return redirect(url_for('login'))
        else:
            flash('Regitration failed. Please try again.', 'danger')
            return render_template('/auth/register.html', form=form, form_errors=form.errors)
    return render_template('/auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    form_error = None
    # If the request method is POST, validate the form and attempt to login
    if request.method == 'POST' and form.validate():
        role = auth.login_by_email(form.email.data, form.password.data)
        if role:
            if role in STAFF_ROLE_LIST:
                return redirect(url_for('dashboard'))
            elif session["role"] == 'customer':
                user = customer.get_customer_by_user_id(session["user_id"])
                session["customer_id"] = user['customer_id']
                previous_page = form.previous_url.data
                cart_utils.merge_customer_cart(session["customer_id"])
                # Get notification for booking hire and return when login
                hire_notification_list = auth.booking_hire_notification(session["customer_id"])
                if hire_notification_list:
                    for row in hire_notification_list:
                        flash(f"Notification: Machine SN: {row['sn']},  Hire Date: {row['hire_from'].strftime('%d/%m/%Y %H:%M:%S')}", 'danger')
                return_notification_list = auth.booking_return_notification(session["customer_id"])
                if return_notification_list:
                    for row in return_notification_list:
                        flash(f"Notification: Machine SN: {row['sn']},  Return Date: {row['hire_to'].strftime('%d/%m/%Y %H:%M:%S')}", 'danger')
     
                # Redirect customer back to page before login
                if previous_page:
                    return redirect(previous_page)
                else:
                    return redirect(url_for('home'))
        else:
            form_error = "Invalid email or password. Please try again."
            return render_template("/auth/login.html", form=form, form_error=form_error, form_errors=form.errors)
    # If the request method is GET, display the login form
    else:
        return render_template("/auth/login.html", form=form)

# Clear session and logout user, return to home page
@app.route('/logout')
def logout():
    if logged_in():
        # Clear all session data except my_store
        session.pop('loggedin', None)
        session.pop('user_id', None)
        session.pop('email', None)
        session.pop('role', None)
        session.pop('customer_id', None)
        session.pop('cart_id', None)
        session.pop('staff_id', None)
        session.pop('store_id', None)
    return redirect(url_for('home'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        if auth.email_exists(email):
            # Generate a token and send email
            token = token_utils.generate_token(email)
            body = f'Click the following link to reset your password: {url_for("reset_password_confirm", token=token, _external=True)}'
            mail.send_email(from_email='info@agrihire.nz', to_email=email, subject='Password Reset Request', body=body)
        flash('Password request email has been sent if account is found', 'success')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    # Check if token is valid
    if token_utils.is_token_valid(token):
        form = ResetPasswordConfirmForm(request.form)
        # token_info = token_utils.get_reset_token_by_token(token)
        email = token_utils.is_token_valid(token)
        if request.method == 'POST' and form.validate():
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            auth.update_password(email, hashed_password)
            token_utils.delete_reset_token_by_token(token)
            flash('Password has been updated.', 'success')
            return redirect(url_for('login'))
        return render_template('auth/reset_password_confirm.html', form=form, token=token)
    else:
        flash('Token is invalid or expired. Please request a new one.', 'danger')
        return redirect(url_for('reset_password'))