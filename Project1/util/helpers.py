import hashlib
from datetime import datetime
from decimal import Decimal
from config.database import db

def generate_sequence(prefix, model, column):
    year = datetime.now().year
    like = f"{prefix}-{year}-%"
    count = db.session.query(db.func.count(getattr(model, column))) \
        .filter(getattr(model, column).like(like)).scalar() or 0
    return f"{prefix}-{year}-{count + 1:06d}"

def file_checksum(stream):
    sha = hashlib.sha256()
    stream.seek(0)
    for chunk in iter(lambda: stream.read(8192), b""):
        sha.update(chunk)
    stream.seek(0)
    return sha.hexdigest()

def money(value):
    return Decimal(str(value or 0)).quantize(Decimal("0.01"))
