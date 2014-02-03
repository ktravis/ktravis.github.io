"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort, render_template

def stubbable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ctx = f(*args, **kwargs)
        if ctx is None:
            ctx = {}
        elif isinstance(ctx, dict):
            ctx['stub'] = request.args.get('stub', False)
        return ctx
    return decorated_function

def templated(template):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            print `users.is_current_user_admin()` + " admin status"
            if users.is_current_user_admin():
                ctx['logged_in'] = True
                ctx['logout_url'] = users.create_logout_url("/")
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                abort(401)  # Unauthorized
            return func(*args, **kwargs)
        return redirect(users.create_login_url(request.url))
    return decorated_view
