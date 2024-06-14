from flask import session, abort

# Module to check if user is logged in 
# and if user has right permission to access the page

# Check if user is logged in, return True or False
def logged_in():
    return 'loggedin' in session

# Check if user role is logged in and permitted to access the page
def allow_role(role_list: list):
    # Check if user is logged in
    # If not logged in, abort 403 and redirect to login
    if logged_in():
        # Check if user role is in the permitted role list
        # if not allowed, abort 401
        if session['role'] not in role_list:
            abort(403)
    else:
        abort(401)

# Check if user role is logged in and permitted to access the page
def check_user_role_customer():
    return {'loggedin': 'loggedin' in session,
            'role': session['role'] == 'customer',
            'user_id': session.get('user_id')} if 'loggedin' in session else {}

def check_user_role_staff():
    return {'loggedin': 'loggedin' in session,
            'role': session['role'] == 'staff',
            'user_id': session.get('user_id')} if 'loggedin' in session else {}

def check_user_role_lmgr():
    return {'loggedin': 'loggedin' in session,
            'role': session['role'] == 'lmgr',
            'user_id': session.get('user_id')} if 'loggedin' in session else {}

def check_user_role_nmgr():
    return {'loggedin': 'loggedin' in session,
            'role': session['role'] == 'nmgr',
            'user_id': session.get('user_id')} if 'loggedin' in session else {}

def check_user_role_admin():
    return {'loggedin': 'loggedin' in session,
            'role': session['role'] == 'admin',
            'user_id': session.get('user_id')} if 'loggedin' in session else {}