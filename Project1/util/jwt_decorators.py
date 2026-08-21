from functools import wraps
from flask import request, jsonify, g, redirect, url_for
import jwt as pyjwt
from util.jwt_utils import decode_token
from models.user import User
from models.employee import Employee

def _extract_token():
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header.removeprefix("Bearer ").strip()
    return request.cookies.get("access_token")

def _unauthorized(message):
    if "text/html" in request.headers.get("Accept", ""):
        return redirect(url_for("auth.login_page"))
    return jsonify(error=message), 401

def jwt_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        token = _extract_token()
        if not token:
            return _unauthorized("Missing token.")
        try:
            payload = decode_token(token, expected_type="access")
        except pyjwt.ExpiredSignatureError:
            return _unauthorized("Token expired.")
        except pyjwt.InvalidTokenError:
            return _unauthorized("Invalid token.")
        
        user = User.query.get(int(payload["sub"]))
        if user is None or not user.is_active:
            return _unauthorized("Account is inactive.")
        
        g.user = user
        g.employee = Employee.query.filter_by(user_id=user.id).first()
        g.jwt_payload = payload
        return view(*args, **kwargs)
    return wrapper

def jwt_role_required(*roles):
    def decorator(view):
        @wraps(view)
        @jwt_required
        def wrapper(*args, **kwargs):
            if g.user.role not in roles:
                if "text/html" in request.headers.get("Accept", ""):
                    from flask import render_template
                    return render_template("error.html", code=403, message="You do not have permission to do that."), 403
                return jsonify(error="Forbidden for this role."), 403
            return view(*args, **kwargs)
        return wrapper
    return decorator
