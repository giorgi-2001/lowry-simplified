import os
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Template
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


template_path = Path(__file__).parent.joinpath("email_template.html")


BASE_FRONTEND_URL = os.environ.get("BASE_FRONTEND_URL")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


def format_email(username: str, token: str, template_path=template_path):
    current_year = datetime.now(timezone.utc).year
    url = f"{BASE_FRONTEND_URL}/password-reset-confirm?token={token}"
    with template_path.open() as file:
        tmpl = Template(file.read())
    return tmpl.render(username=username, reset_link=url, year=current_year)


async def send_email(email: str, username: str, token: str):
    email_template = format_email(username, token)

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=email_template,
        subtype="html"
    )

    fast_mail = FastMail(conf)
    await fast_mail.send_message(message)
