import resend
from flask import current_app
import traceback


def send_email(subject, recipients, body):
    try:
        resend.api_key = current_app.config["RESEND_API_KEY"]

        response = resend.Emails.send({
            "from": "Cloud File Storage <onboarding@resend.dev>",
            "to": recipients,
            "subject": subject,
            "text": body,
        })

        print("=" * 60)
        print("RESEND RESPONSE:")
        print(response)
        print("=" * 60)

        return True

    except Exception:
        print("=" * 60)
        print("RESEND ERROR")
        traceback.print_exc()
        print("=" * 60)
        return False