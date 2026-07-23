from database.db import db
from database.models import ActivityLog


def log_activity(user_id, action, description=None):
    try:
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            description=description
        )

        db.session.add(activity)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Activity Log Error: {e}")