from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List
from models import User
import jwt
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from dotenv import dotenv_values

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,  # Use False for STARTTLS as we're using SSL
    MAIL_SSL_TLS=True,    # Use True for SSL/TLS as we are using port 465
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True   # This ensures certificates are validated
)

async def send_email(email: List[str], instance: User):
    token_data = {
        "id": instance.id,
        "username": instance.username
    }
    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")
    
    template = f"""
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        <body>
            <div style="display: flex; align-items: center; justify-content: center; flex-direction: column">
                <h3>Account Verification</h3>
                <p>Thanks for choosing us, please click the button below to verify your account.</p>
                <a href="http://localhost:8000/verification/?token={token}">Verify your email</a>
                <p>Please ignore this email if you did not register with us and nothing will happen.</p>
            </div>
        </body>
    </html>
    """
    
    message = MessageSchema(
        subject="Account Verification",
        recipients=email,
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)
