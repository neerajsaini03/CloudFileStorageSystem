from flask_mail import Mail, Message

mail = Mail()


def send_email(subject, recipients, body):
    """
    Send an email safely.
    If email sending fails, the application will continue running.
    """

    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body
        )

        mail.send(msg)

        print("=" * 50)
        print("✅ Email sent successfully.")
        print("Recipients:", recipients)
        print("=" * 50)

        return True

    except Exception as e:
        print("=" * 50)
        print("❌ Email sending failed!")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)

        # Do NOT stop the application
        return False