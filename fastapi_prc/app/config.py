import secrets

ACCESS_TOKEN_EXPIRE_MINUTE = 60 * 24 * 8
SECRET_KEY = secrets.token_urlsafe(32)

SMTP_HOST = "localhost"
SMTP_PORT = "867"
SERVER_HOST = "localhost"

PROJECT_NAME="fastapi-prc"
EMAIL_TEMPLATES_DIR = "/app/email-templates"
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
