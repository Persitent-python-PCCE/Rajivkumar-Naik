from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g, current_app
from dao.user_dao import UserDAO
from dao.employee_dao import EmployeeDAO
from service.auth_service import AuthService
from util.jwt_utils import issue_access_token, issue_refresh_token, decode_token
from util.jwt_decorators import jwt_required
import jwt as pyjwt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
user_dao = UserDAO()
employee_dao = EmployeeDAO()
auth_service = AuthService(user_dao, employee_dao)


# ---------------------------------------------------------------------------
# Phase 1 helper: redirect to a role dashboard.
# Other blueprints are added in later phases; for now everyone goes to /auth/home.
# ---------------------------------------------------------------------------
def _home_for(role):
    destinations = {
        "EMPLOYEE": "auth.home",
        "MANAGER":  "auth.home",
        "FINANCE":  "auth.home",
        "ADMIN":    "auth.home",
    }
    return url_for(destinations.get(role, "auth.home"))


@auth_bp.route("/home")
@jwt_required
def home():
    """Phase-1 landing page after login (all roles)."""
    return render_template("home.html")


@auth_bp.route("/login-page")
def login_page():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) if request.is_json else request.form
    try:
        user = auth_service.authenticate(data.get("username"), data.get("password"))
    except ValueError as e:
        if request.is_json:
            return jsonify(error=str(e)), 401
        flash(str(e), "danger")
        return redirect(url_for("auth.login_page"))

    access = issue_access_token(user)
    refresh = issue_refresh_token(user)

    if request.is_json:
        return jsonify(access_token=access, refresh_token=refresh,
                       token_type="Bearer", user=user.to_dict())

    resp = redirect(_home_for(user.role))
    resp.set_cookie("access_token", access, httponly=True, samesite="Lax",
                    max_age=current_app.config["JWT_ACCESS_MINUTES"] * 60)
    resp.set_cookie("refresh_token", refresh, httponly=True, samesite="Lax",
                    max_age=current_app.config["JWT_REFRESH_DAYS"] * 86400)
    flash(f"Welcome back, {user.username}!", "success")
    return resp


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json(silent=True) or {}
    token = data.get("refresh_token") or request.cookies.get("refresh_token", "")
    try:
        payload = decode_token(token, expected_type="refresh")
    except pyjwt.ExpiredSignatureError:
        return jsonify(error="Refresh token expired. Please log in again."), 401
    except pyjwt.InvalidTokenError:
        return jsonify(error="Invalid refresh token."), 401

    user = user_dao.get_by_id(int(payload["sub"]))
    if user is None or not user.is_active:
        return jsonify(error="Account is inactive."), 401
    return jsonify(access_token=issue_access_token(user), token_type="Bearer")


@auth_bp.route("/logout")
@jwt_required
def logout():
    resp = redirect(url_for("auth.login_page"))
    resp.delete_cookie("access_token")
    resp.delete_cookie("refresh_token")
    flash("You have been logged out.", "info")
    return resp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            auth_service.register(request.form)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login_page"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("register.html", managers=employee_dao.get_all())


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required
def change_password():
    try:
        auth_service.change_password(g.user,
                                     request.form.get("old_password"),
                                     request.form.get("new_password"))
        flash("Password updated.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("auth.home"))


@auth_bp.route("/me")
@jwt_required
def me():
    return jsonify(id=g.user.id, username=g.user.username, role=g.user.role,
                   employee=g.employee.to_dict() if g.employee else None)
