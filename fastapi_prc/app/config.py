import secrets

ACCESS_TOKEN_EXPIRE_MINUTE = 60 * 24 * 8
SECRET_KEY = secrets.token_urlsafe(32)