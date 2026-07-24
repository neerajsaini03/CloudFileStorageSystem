from flask import current_app
from flask_mail import Mail, Message
import traceback

mail = Mail()


def send_email(subject, recipients, body):
    try:
        print("=" * 50)
        print("MAIL_SERVER:", current_app.config.get("MAIL_SERVER"))
        print("MAIL_PORT:", current_app.config.get("MAIL_PORT"))
        print("MAIL_USE_TLS:", current_app.config.get("MAIL_USE_TLS"))
        print("MAIL_USE_SSL:", current_app.config.get("MAIL_USE_SSL"))
        print("MAIL_USERNAME:", current_app.config.get("MAIL_USERNAME"))
        print("MAIL_DEFAULT_SENDER:", current_app.config.get("MAIL_DEFAULT_SENDER"))
        print("=" * 50)

        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body
        )

        mail.send(msg)

        print("✅ Email sent successfully")
        return True

    except Exception:
        traceback.print_exc()
        return False