import resend
import traceback

from flask import current_app


def send_email(subject, recipients, body):
    """
    Send email using Resend API.
    Returns True if successful.
    """

    try:

        resend.api_key = current_app.config["RESEND_API_KEY"]

        response = resend.Emails.send(
            {
                "from": f"Cloud File Storage <{current_app.config['RESEND_FROM_EMAIL']}>",
                "to": recipients,
                "subject": subject,
                "text": body,
            }
        )

        print("=" * 60)
        print("EMAIL SENT SUCCESSFULLY")
        print(response)
        print("=" * 60)

        return True

    except Exception as e:

        print("=" * 60)
        print("EMAIL FAILED")
        print(type(e).__name__)
        print(e)
        traceback.print_exc()
        print("=" * 60)

        return False