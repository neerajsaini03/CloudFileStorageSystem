import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # =====================================
    # Flask
    # =====================================
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

    # =====================================
    # Database
    # =====================================
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db"
    )

    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =====================================
    # Upload Settings
    # =====================================
    UPLOAD_FOLDER = "uploads"

    # Maximum upload size (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Maximum storage per user (1 GB)
    MAX_STORAGE_PER_USER = 1024 * 1024 * 1024
    
    # ==========================
    # Allowed File Extensions
    # ==========================

    ALLOWED_EXTENSIONS = {
        "txt",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "webp",
        "mp3",
        "wav",
        "mp4",
        "avi",
        "mov",
        "zip",
        "rar",
        "7z",
        "csv",
        "py",
        "java",
        "c",
        "cpp",
        "html",
        "css",
        "js",
        "json",
        "xml"
    }

    # =====================================
    # AWS S3
    # =====================================
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # =====================================
    # Resend Email
    # =====================================
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    RESEND_FROM_EMAIL = os.getenv(
        "RESEND_FROM_EMAIL",
        "noreply@cloudfilestorage.online"
    )