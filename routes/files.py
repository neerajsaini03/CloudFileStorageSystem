import os
import secrets

from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user

from database.db import db
from database.models import File
from utils.activity_logger import log_activity
from utils.aws import delete_file_from_s3

from utils.aws import (
    download_file_from_s3,
    delete_file_from_s3
)

files = Blueprint("files", __name__)


# ======================================================
# My Files
# ======================================================

@files.route("/my-files")
@login_required
def my_files():

    search = request.args.get("search", "")

    if search:
        uploaded_files = File.query.filter(
            File.user_id == current_user.id,
            File.original_filename.ilike(f"%{search}%")
        ).all()
    else:
        uploaded_files = File.query.filter_by(
            user_id=current_user.id
        ).all()

    return render_template(
        "my_files.html",
        files=uploaded_files,
        search=search
    )


# ======================================================
# Download File
# ======================================================

@files.route("/download/<int:file_id>")
@login_required
def download_file(file_id):

    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first_or_404()

    file_stream = download_file_from_s3(file.filename)

    if file_stream is None:
        flash("Unable to download file.", "danger")
        return redirect(url_for("files.my_files"))
    log_activity(
        current_user.id,
        "File Downloaded",
        f"{file.original_filename} downloaded."
    )

    return send_file(
        file_stream,
        as_attachment=True,
        download_name=file.original_filename,
        mimetype=file.file_type
    )


# ======================================================
# Preview File
# ======================================================

@files.route("/preview/<int:file_id>")
@login_required
def preview_file(file_id):

    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first_or_404()

    file_stream = download_file_from_s3(file.filename)

    if file_stream is None:
        flash("Unable to preview file.", "danger")
        return redirect(url_for("files.my_files"))
    log_activity(
        current_user.id,
        "File Previewed",
        f"{file.original_filename} previewed."
    )

    return send_file(
        file_stream,
        mimetype=file.file_type,
        download_name=file.original_filename,
        as_attachment=False
    )


# ======================================================
# Delete File
# ======================================================

@files.route("/delete/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):

    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first_or_404()

    success = delete_file_from_s3(file.filename)

    if not success:
        flash("Unable to delete file from AWS S3.", "danger")
        return redirect(url_for("files.my_files"))

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        file.filename
    )

    if os.path.exists(path):
        os.remove(path)

    db.session.delete(file)
    db.session.commit()
    log_activity(
        current_user.id,
        "File Deleted",
        f"{file.original_filename} deleted."
    )

    flash("File deleted successfully!", "success")

    return redirect(url_for("files.my_files"))


# ======================================================
# Generate Share Link
# ======================================================

@files.route("/share/<int:file_id>")
@login_required
def share_file(file_id):

    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first_or_404()

    if not file.share_token:
        file.share_token = secrets.token_urlsafe(32)
        file.is_public = True
        db.session.commit()
        log_activity(
            current_user.id,
            "File Shared",
            f"{file.original_filename} shared publicly."
        )

    share_url = url_for(
        "files.shared_file",
        token=file.share_token,
        _external=True
    )

    flash(f"Share Link: {share_url}", "success")

    return redirect(url_for("files.my_files"))


# ======================================================
# Public Shared Page
# ======================================================

@files.route("/shared/<string:token>")
def shared_file(token):

    file = File.query.filter_by(
        share_token=token,
        is_public=True
    ).first_or_404()

    return render_template(
        "shared_file.html",
        file=file
    )


# ======================================================
# Download Shared File
# ======================================================

@files.route("/shared/download/<string:token>")
def download_shared_file(token):

    file = File.query.filter_by(
        share_token=token,
        is_public=True
    ).first_or_404()

    file_stream = download_file_from_s3(file.filename)

    if file_stream is None:
        flash("Unable to download file.", "danger")
        return redirect(url_for("files.shared_file", token=token))

    return send_file(
        file_stream,
        as_attachment=True,
        download_name=file.original_filename,
        mimetype=file.file_type
    )
# ======================================================
# File Version History
# ======================================================

@files.route("/versions/<int:file_id>")
@login_required
def file_versions(file_id):

    current_file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first_or_404()

    # Find the root file
    root_id = (
        current_file.parent_file_id
        if current_file.parent_file_id
        else current_file.id
    )

    versions = File.query.filter(
        (File.id == root_id) |
        (File.parent_file_id == root_id)
    ).order_by(
        File.version.desc()
    ).all()

    return render_template(
        "file_versions.html",
        current_file=current_file,
        versions=versions
    )