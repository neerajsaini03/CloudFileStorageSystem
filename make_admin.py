from app import app
from database.db import db
from database.models import User

with app.app_context():
    user = User.query.filter_by(email="neerajsaini2619@gmail.com").first()

    if user is None:
        print("User not found!")
    else:
        user.is_admin = True
        db.session.commit()
        print("Admin access granted successfully!")