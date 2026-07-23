import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # ==========================
    # Flask Configuration
    # ==========================

    SECRET_KEY = os.getenv("SECRET_KEY")

    # ==========================
    # Database Configuration
    # ==========================

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db"
    )

    # Fix Render/Heroku-style PostgreSQL URL if needed
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================
    # File Upload Configuration
    # ==========================

    # Local upload folder (used temporarily before uploading to S3)
    UPLOAD_FOLDER = "uploads"

    # Maximum file size (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Maximum storage allowed per user (1 GB)
    MAX_STORAGE_PER_USER = 1024 * 1024 * 1024

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        "pdf",
        "doc",
        "docx",
        "txt",
        "png",
        "jpg",
        "jpeg",
        "gif",
        "zip",
        "rar"
    }

    # ==========================
    # AWS S3 Configuration
    # ==========================

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # ==========================
    # Flask-Mail Configuration
    # ==========================

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))

    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False