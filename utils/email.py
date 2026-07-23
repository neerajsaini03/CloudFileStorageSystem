from flask_mail import Mail, Message

mail = Mail()

def send_email(subject, recipients, body):

    print("=" * 50)
    print("send_email() function called")
    print("Recipients:", recipients)

    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body
        )

        mail.send(msg)

        print("✅ Email sent successfully.")
        print("=" * 50)

    except Exception as e:
        print("❌ Email sending failed!")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)