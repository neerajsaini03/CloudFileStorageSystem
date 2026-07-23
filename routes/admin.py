from functools import wraps
from utils.aws import delete_file_from_s3

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from database.db import db
from database.models import User, File, ActivityLog

admin = Blueprint("admin", __name__)


# -------------------------
# Admin Access Decorator
# -------------------------

def admin_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("main.dashboard"))

        return func(*args, **kwargs)

    return decorated_function


# -------------------------
# Admin Dashboard
# -------------------------

@admin.route("/admin")
@login_required
@admin_required
def admin_dashboard():

    # Dashboard Statistics
    total_users = User.query.count()

    total_files = File.query.count()

    total_storage = sum(
        file.file_size or 0
        for file in File.query.all()
    )
    total_logs = ActivityLog.query.count()

    recent_logs = (
        ActivityLog.query
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )

    # Fetch all users
    users = User.query.order_by(User.id).all()

    # Fetch all uploaded files
    files = File.query.order_by(File.upload_date.desc()).all()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_files=total_files,
        total_storage=round(total_storage / (1024 * 1024), 2),
        total_logs=total_logs,
        users=users,
        files=files,
        recent_logs=recent_logs
 
    )
# =====================================
# TEMPORARY MAKE ADMIN ROUTE
# =====================================

@admin.route("/make-admin")
def make_admin():

    from database.models import User
    from database.db import db

    user = User.query.filter_by(
        email="neerajsaini2619@gmail.com"
    ).first()

    if not user:
        return "User not found"

    user.is_admin = True
    db.session.commit()

    return "Admin created successfully!"
# =====================================
# Delete User
# =====================================

@admin.route("/admin/delete-user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own admin account.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect(url_for("admin.admin_dashboard"))


# =====================================
# Delete File
# =====================================

@admin.route("/admin/delete-file/<int:file_id>", methods=["POST"])
@login_required
@admin_required
def delete_file(file_id):

    file = File.query.get_or_404(file_id)

    delete_file_from_s3(file.filename)

    db.session.delete(file)
    db.session.commit()

    flash("File deleted successfully.", "success")

    return redirect(url_for("admin.admin_dashboard"))