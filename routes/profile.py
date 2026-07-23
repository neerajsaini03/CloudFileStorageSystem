from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import ActivityLog

from database.db import db

profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["GET", "POST"])
@login_required
def user_profile():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")

        # Update full name
        current_user.fullname = fullname

        # Change password if provided
        if current_password and new_password:

            if not check_password_hash(
                current_user.password,
                current_password
            ):
                flash("Current password is incorrect.", "danger")
                return redirect(url_for("profile.user_profile"))

            current_user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("profile.user_profile"))

    return render_template("profile.html")

# ==================================
# Activity History
# ==================================

@profile.route("/activity-history")
@login_required
def activity_history():

    activities = (
        ActivityLog.query
        .filter_by(user_id=current_user.id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )

    return render_template(
        "activity_history.html",
        activities=activities
    )