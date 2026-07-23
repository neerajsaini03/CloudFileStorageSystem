from flask import current_app
from werkzeug.utils import secure_filename
import logging

# ==========================
# Configure Security Logger
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("CloudStorageSecurity")


# ==========================
# Check Allowed Extension
# ==========================

def allowed_file(filename):
    """
    Check whether uploaded file extension is allowed.
    """

    if "." not in filename:
        logger.warning(f"Rejected file (no extension): {filename}")
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in current_app.config["ALLOWED_EXTENSIONS"]:
        logger.warning(
            f"Blocked upload: {filename} ({extension})"
        )
        return False

    return True


# ==========================
# Sanitize Filename
# ==========================

def sanitize_filename(filename):
    """
    Remove dangerous characters from filename.
    """

    safe_name = secure_filename(filename)

    logger.info(
        f"Filename sanitized: {filename} -> {safe_name}"
    )

    return safe_name


# ==========================
# Validate Uploaded File
# ==========================

def validate_file(uploaded_file):
    """
    Validate uploaded file.

    Returns:
        (True, "")
        (False, error_message)
    """

    if uploaded_file.filename == "":

        logger.warning("Upload attempted without selecting a file.")

        return False, "No file selected."

    if not allowed_file(uploaded_file.filename):

        allowed = ", ".join(
            sorted(current_app.config["ALLOWED_EXTENSIONS"])
        )

        return (
            False,
            f"""
File type not allowed.

Allowed file types:

{allowed}
"""
        )

    logger.info(
        f"Validated upload: {uploaded_file.filename}"
    )

    return True, ""