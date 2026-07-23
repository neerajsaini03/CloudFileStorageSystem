import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:

    # ==========================
    # Flask Configuration
    # ==========================

    SECRET_KEY = os.getenv("SECRET_KEY")

    # ==========================
    # Database Configuration
    # ==========================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ==========================
    # File Upload Configuration
    # ==========================

    # Upload folder
    UPLOAD_FOLDER = "uploads"

    # Maximum size of a single uploaded file (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Maximum storage allowed per user (1 GB)
    MAX_STORAGE_PER_USER = 1024 * 1024 * 1024

    # Allowed upload extensions
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

    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"

    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    MAIL_SUPPRESS_SEND = False

    MAIL_ASCII_ATTACHMENTS = False