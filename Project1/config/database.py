import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    user = os.getenv("DB_USER", "root")
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "travel")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "pool_recycle": 280}

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-only-change-me")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", app.config["JWT_SECRET_KEY"])
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_ACCESS_MINUTES"] = int(os.getenv("JWT_ACCESS_MINUTES", 15))
    app.config["JWT_REFRESH_DAYS"] = int(os.getenv("JWT_REFRESH_DAYS", 7))

    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads/receipts")
    app.config["ALLOWED_EXTENSIONS"] = {"pdf", "png", "jpg", "jpeg"}
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH_MB", 5)) * 1024 * 1024

    db.init_app(app)
