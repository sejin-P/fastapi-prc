import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

import emails
from emails.template import JinjaTemplate
from jose import jwt

from fastapi_prc.app import config


def send_email(email_to: str, subject_template: str = "", html_template: str = "", environment: Dict[str, Any] = {}) -> None:
    message = emails.Message(subject=JinjaTemplate(subject_template), html=JinjaTemplate(html_template), mail_from=(None, None))
    smtp_options = {"host": config.SMTP_HOST, "port": config.SMTP_PORT}
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = config.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(config.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = config.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": config.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": config.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def generate_password_token(email: str) -> str:
    delta = timedelta(hours=48)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode({
        "exp": exp,
        "now": now,
        "sub": email,
    }, config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
