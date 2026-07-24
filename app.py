from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

from database.db import db
from database.models import User
from flask import Flask, render_template
from utils.email import send_email

from routes.auth import auth
from routes.dashboard import main
from routes.upload import upload
from routes.files import files
from routes.profile import profile
from routes.admin import admin

from utils.aws import test_s3_connection


# ==========================
# Create Flask App
# ==========================

app = Flask(__name__)
app.config.from_object(Config)


# ==========================
# Initialize Extensions
# ==========================

db.init_app(app)

migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message = "Please login first."
login_manager.login_message_category = "warning"


# ==========================
# Flask-Login User Loader
# ==========================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ==========================
# Register Blueprints
# ==========================

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(upload)
app.register_blueprint(files)
app.register_blueprint(profile)
app.register_blueprint(admin)


# ==========================
# Startup Tasks
# ==========================

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Database initialization failed:")
        print(e)

    try:
        test_s3_connection()
    except Exception as e:
        print("AWS connection failed:")
        print(e)


# ==========================
# Run Application
# ==========================
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
if __name__ == "__main__":
    app.run(debug=True)