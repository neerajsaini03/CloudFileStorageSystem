import resend
from flask import current_app


def send_email(subject, recipients, body):
    """
    Send email using Resend API.
    Returns True if successful, False otherwise.
    """

    try:
        # Set API Key
        resend.api_key = current_app.config["RESEND_API_KEY"]

        params = {
            "from": "Cloud File Storage <onboarding@resend.dev>",
            "to": recipients,
            "subject": subject,
            "text": body,
        }

        resend.Emails.send(params)

        print("=" * 50)
        print("✅ Email sent successfully!")
        print("Recipients:", recipients)
        print("=" * 50)

        return True

    except Exception as e:
        print("=" * 50)
        print("❌ Email sending failed!")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)

        return False