import smtplib
import ssl
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    @staticmethod
    def send(receiver_email: str, title: str, message: str) -> None:
        port: int = 465
        sender_email: str = ""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = title
        msg["From"] = sender_email
        msg["To"] = receiver_email

        msg.attach(MIMEText(message, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, base64.decodebytes(b"").decode("utf-8") )
            server.sendmail(sender_email, receiver_email, msg.as_string())
