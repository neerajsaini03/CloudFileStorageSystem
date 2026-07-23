import random
from datetime import datetime, timedelta
from database.models import User, indian_time
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.db import db
from database.models import User

from utils.email import send_email
from utils.activity_logger import log_activity

auth = Blueprint("auth", __name__)


# ==================================
# Register
# ==================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        user = User(
            fullname=fullname,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        log_activity(
            user.id,
            "User Registered",
            f"{user.fullname} created a new account."
        )

        subject = "Welcome to Cloud File Storage"

        body = f"""
Hello {user.fullname},

Welcome to Cloud File Storage!

Your account has been created successfully.

You can now:

• Upload files
• Preview files
• Download files
• Share files securely
• Manage your cloud storage

Thank you for using our application.

Cloud File Storage Team
"""

        try:
            send_email(
                subject=subject,
                recipients=[user.email],
                body=body
            )
        except Exception as e:
            print(f"Email Error: {e}")

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ==================================
# Login
# ==================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)
            log_activity(
                user.id,
                "User Login",
                "Logged into the system."
            )

            flash("Login successful!", "success")

            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# ==================================
# Forgot Password
# ==================================

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account found with this email.", "danger")
            return redirect(url_for("auth.forgot_password"))

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP and expiry
        user.otp = otp
        user.otp_expiry = indian_time() + timedelta(minutes=5)

        db.session.commit()

        # Send OTP Email
        subject = "Cloud File Storage - Password Reset OTP"

        body = f"""
Hello {user.fullname},

Your password reset OTP is:

{otp}

This OTP will expire in 5 minutes.

If you did not request a password reset, please ignore this email.

Cloud File Storage Team
"""

        try:
            send_email(
                subject=subject,
                recipients=[user.email],
                body=body
        )
        except Exception as e:
            print(f"Email Error: {e}")

        flash(
            "OTP has been sent to your email.",
            "success"
        )

        return render_template(
            "verify_otp.html",
            email=user.email
        )

    # Handle GET request
    return render_template("forgot_password.html")
# ==================================
# Verify OTP
# ==================================

@auth.route("/verify-otp", methods=["POST"])
def verify_otp():

    email = request.form.get("email")
    otp = request.form.get("otp")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if user.otp != otp:
        flash("Invalid OTP.", "danger")
        return render_template(
            "verify_otp.html",
            email=email
        )

    if (
        user.otp_expiry is None or
        user.otp_expiry < indian_time()
    ):
        flash("OTP has expired.", "danger")
        return redirect(url_for("auth.forgot_password"))

    return render_template(
        "reset_password.html",
        email=email
    )


# ==================================
# Reset Password
# ==================================

@auth.route("/reset-password", methods=["POST"])
def reset_password():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    user.password = generate_password_hash(password)

    # Clear OTP after successful reset
    user.otp = None
    user.otp_expiry = None

    db.session.commit()
    log_activity(
        user.id,
        "Password Reset",
        "Password changed successfully."
    )
    flash(
        "Password updated successfully. Please login.",
        "success"
    )

    return redirect(url_for("auth.login"))

# ==================================
# Logout
# ==================================

@auth.route("/logout")
@login_required
def logout():

    log_activity(
        current_user.id,
        "User Logout",
        "Logged out of the system."
    )

    logout_user()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect(url_for("auth.login"))