import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, redirect, url_for, g
from config.database import db, init_db
import models  # noqa: F401 - registers all ORM models with SQLAlchemy
from controller.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)

    # 1. Wire up DB config + secret keys from .env
    init_db(app)

    # 2. Register blueprints (Phase 1: auth only)
    app.register_blueprint(auth_bp)

    # 3. Logging
    os.makedirs("logs", exist_ok=True)
    handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s [%(module)s:%(lineno)d] %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    # 4. Inject current_user into every template
    @app.context_processor
    def inject_user():
        return {"current_user": g.get("user"), "current_employee": g.get("employee")}

    # 5. Error handlers
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template("error.html", code=401, message="Please log in."), 401

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403, message="You do not have permission to do that."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        app.logger.exception("Unhandled error")
        return render_template("error.html", code=500, message="Something went wrong. It has been logged."), 500

    # 6. Root redirect to login
    @app.route("/")
    def root():
        return redirect(url_for("auth.login_page"))

    # 7. Create DB tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
