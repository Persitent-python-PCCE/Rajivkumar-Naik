import uuid
from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app

def _now():
    return datetime.now(timezone.utc)

def issue_access_token(user):
    payload = {
        "sub": str(user.id), "role": user.role, "type": "access",
        "jti": uuid.uuid4().hex, "iat": _now(),
        "exp": _now() + timedelta(minutes=current_app.config["JWT_ACCESS_MINUTES"]),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])

def issue_refresh_token(user):
    payload = {
        "sub": str(user.id), "type": "refresh",
        "jti": uuid.uuid4().hex, "iat": _now(),
        "exp": _now() + timedelta(days=current_app.config["JWT_REFRESH_DAYS"]),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])

def decode_token(token, expected_type="access"):
    payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=[current_app.config["JWT_ALGORITHM"]])
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"Expected a {expected_type} token.")
    return payload
