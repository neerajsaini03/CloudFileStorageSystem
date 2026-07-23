from collections import Counter

from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

from database.models import File

main = Blueprint("main", __name__)


# ==========================
# Home Page
# ==========================

@main.route("/")
def home():
    return render_template("index.html")


# ==========================
# Dashboard
# ==========================

@main.route("/dashboard")
@login_required
def dashboard():

    # --------------------------------
    # Get all uploaded files
    # --------------------------------

    uploaded_files = File.query.filter_by(
        user_id=current_user.id
    ).all()

    # --------------------------------
    # Recent Uploads
    # --------------------------------

    recent_files = (
        File.query
        .filter_by(user_id=current_user.id)
        .order_by(File.upload_date.desc())
        .limit(5)
        .all()
    )

    # --------------------------------
    # File Type Statistics
    # --------------------------------

    file_types = []

    for file in uploaded_files:

        if file.file_type:
            file_types.append(file.file_type)

    type_counter = Counter(file_types)

    chart_labels = list(type_counter.keys())

    chart_values = list(type_counter.values())

    # --------------------------------
    # Monthly Upload Statistics
    # --------------------------------

    monthly_counter = Counter()

    for file in uploaded_files:

        if file.upload_date:

            month = file.upload_date.strftime("%b %Y")

            monthly_counter[month] += 1

    month_labels = list(monthly_counter.keys())

    month_values = list(monthly_counter.values())

    # --------------------------------
    # Dashboard Statistics
    # --------------------------------

    total_files = len(uploaded_files)

    storage_used = sum(
        file.file_size or 0
        for file in uploaded_files
    )

    storage_limit = current_app.config["MAX_STORAGE_PER_USER"]

    storage_remaining = storage_limit - storage_used

    usage_percentage = (
        (storage_used / storage_limit) * 100
        if storage_limit > 0 else 0
    )

    # --------------------------------
    # Render Dashboard
    # --------------------------------

    return render_template(
        "dashboard.html",
        total_files=total_files,
        storage_used=storage_used,
        storage_limit=storage_limit,
        storage_remaining=storage_remaining,
        usage_percentage=usage_percentage,
        recent_files=recent_files,
        chart_labels=chart_labels,
        chart_values=chart_values,
        month_labels=month_labels,
        month_values=month_values
    )