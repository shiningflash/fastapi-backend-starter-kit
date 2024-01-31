import uuid
from datetime import datetime, timedelta


def generate_unique_token():
    return str(uuid.uuid4())


def calculate_expiration(hours):
    return datetime.now() + timedelta(hours=hours)
