from datetime import datetime, timedelta

from flask_login import UserMixin

from database.db import db
def indian_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)


# ==========================================
# User Model
# ==========================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    # ==========================
    # Password Reset (OTP)
    # ==========================

    otp = db.Column(
        db.String(6),
        nullable=True
    )

    otp_expiry = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==========================
    # Relationships
    # ==========================

    files = db.relationship(
        "File",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    activity_logs = db.relationship(
        "ActivityLog",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


# ==========================================
# File Model
# ==========================================

class File(db.Model):

    __tablename__ = "files"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    display_name = db.Column(
        db.String(255),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    file_type = db.Column(
        db.String(100),
        nullable=False
    )

    file_size = db.Column(
        db.Integer,
        nullable=False
    )

    upload_date = db.Column(
    db.DateTime,
    default=indian_time

    )

    # ==========================
    # File Versioning
    # ==========================

    version = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    parent_file_id = db.Column(
        db.Integer,
        db.ForeignKey("files.id"),
        nullable=True
    )

    versions = db.relationship(
        "File",
        backref=db.backref(
            "parent",
            remote_side=[id]
        ),
        lazy=True
    )

    # ==========================
    # File Sharing
    # ==========================

    share_token = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    is_public = db.Column(
        db.Boolean,
        default=False
    )

    # ==========================
    # Owner
    # ==========================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


# ==========================================
# Activity Log Model
# ==========================================

class ActivityLog(db.Model):

    __tablename__ = "activity_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
    db.DateTime,
    default=indian_time
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )