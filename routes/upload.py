import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from database.db import db
from database.models import File
from utils.activity_logger import log_activity

from utils.aws import upload_file_to_s3
from utils.security import (
    validate_file,
    sanitize_filename
)

upload = Blueprint("upload", __name__)


# ==========================
# Upload File
# ==========================

@upload.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():

    if request.method == "POST":

        uploaded_file = request.files.get("file")

        if not uploaded_file:
            flash("Please select a file.", "danger")
            return redirect(request.url)

        # ==========================
        # Validate File
        # ==========================

        valid, message = validate_file(uploaded_file)

        if not valid:
            flash(message, "danger")
            return redirect(request.url)

        # ==========================
        # Calculate File Size
        # ==========================

        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)

        # ==========================
        # Check User Storage Limit
        # ==========================

        storage_used = sum(
            file.file_size or 0
            for file in File.query.filter_by(
                user_id=current_user.id
            ).all()
        )

        storage_limit = current_app.config["MAX_STORAGE_PER_USER"]

        if storage_used + file_size > storage_limit:

            remaining = storage_limit - storage_used

            flash(
                f"Storage limit exceeded! "
                f"You have only {remaining / (1024 * 1024):.2f} MB remaining.",
                "danger"
            )

            return redirect(request.url)

        # ==========================
        # File Information
        # ==========================

        original_filename = uploaded_file.filename

        safe_filename = sanitize_filename(original_filename)

        unique_filename = f"{uuid.uuid4()}_{safe_filename}"

        display_name = request.form.get("display_name")

        description = request.form.get("description")

        file_type = uploaded_file.mimetype

        # ==========================
        # Save Temporary File
        # ==========================

        os.makedirs(
            current_app.config["UPLOAD_FOLDER"],
            exist_ok=True
        )

        local_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        uploaded_file.save(local_path)

        # ==========================
        # Upload to AWS S3
        # ==========================

        with open(local_path, "rb") as file_data:

            success = upload_file_to_s3(
                file_data,
                unique_filename
            )

        if not success:

            if os.path.exists(local_path):
                os.remove(local_path)

            flash(
                "AWS S3 upload failed.",
                "danger"
            )

            return redirect(request.url)

        # ==========================
        # Save Database Record
        # ==========================

        existing_file = File.query.filter_by(
            user_id=current_user.id,
            original_filename=original_filename
        ).order_by(
            File.version.desc()
        ).first()

        if existing_file:

            new_file = File(
                filename=unique_filename,
                original_filename=original_filename,
                display_name=display_name,
                description=description,
                file_type=file_type,
                file_size=file_size,
                version=existing_file.version + 1,
                parent_file_id=existing_file.id,
                user_id=current_user.id
            )

            message = (
                f"New version (v{new_file.version}) "
                "uploaded successfully!"
            )

        else:

            new_file = File(
                filename=unique_filename,
                original_filename=original_filename,
                display_name=display_name,
                description=description,
                file_type=file_type,
                file_size=file_size,
                version=1,
                parent_file_id=None,
                user_id=current_user.id
            )

            message = "File uploaded successfully!"

        db.session.add(new_file)
        db.session.commit()
        log_activity(
            current_user.id,
            "File Uploaded",
            f"{new_file.original_filename} (Version {new_file.version}) uploaded."
        )

        flash(
            message,
            "success"
        )

        return redirect(url_for("files.my_files"))

    return render_template("upload.html")