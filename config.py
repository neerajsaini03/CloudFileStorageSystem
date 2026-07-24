import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


class Config:
    # ==========================
    # Flask
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

    # ==========================
    # Database
    # ==========================
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db"
    )

    # Fix old postgres:// URLs
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================
    # File Upload
    # ==========================
    UPLOAD_FOLDER = "uploads"

    # Maximum upload size (16 MB per file)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Maximum storage per user (1 GB)
    MAX_STORAGE_PER_USER = 1024 * 1024 * 1024

    # ==========================
    # AWS S3
    # ==========================
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # ==========================
    # Resend Email API
    # ==========================
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    # Must be a verified sender/domain in Resend
    RESEND_FROM_EMAIL = os.getenv(
        "RESEND_FROM_EMAIL",
        "onboarding@resend.dev"
    )