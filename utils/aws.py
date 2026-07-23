import boto3
from io import BytesIO
from flask import current_app


def get_s3_client():
    """
    Create and return an AWS S3 client.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
        region_name=current_app.config["AWS_REGION"]
    )


def test_s3_connection():
    """
    Test the AWS S3 connection by listing buckets.
    """
    try:
        s3 = get_s3_client()

        response = s3.list_buckets()

        print("\n✅ AWS Connection Successful!\n")
        print("Available Buckets:")

        for bucket in response["Buckets"]:
            print("-", bucket["Name"])

        return True

    except Exception as e:
        print("\n❌ AWS Connection Failed!\n")
        print(e)
        return False


def upload_file_to_s3(file_object, object_name):
    """
    Upload a file object to AWS S3.
    """
    try:
        s3 = get_s3_client()

        s3.upload_fileobj(
            Fileobj=file_object,
            Bucket=current_app.config["AWS_BUCKET_NAME"],
            Key=object_name
        )

        return True

    except Exception as e:
        print(e)
        return False


def download_file_from_s3(object_name):
    """
    Download a file from AWS S3.
    """
    try:
        s3 = get_s3_client()

        file_stream = BytesIO()

        s3.download_fileobj(
            Bucket=current_app.config["AWS_BUCKET_NAME"],
            Key=object_name,
            Fileobj=file_stream
        )

        file_stream.seek(0)

        return file_stream

    except Exception as e:
        print(e)
        return None


def delete_file_from_s3(object_name):
    """
    Delete a file from AWS S3.
    """
    try:
        s3 = get_s3_client()

        s3.delete_object(
            Bucket=current_app.config["AWS_BUCKET_NAME"],
            Key=object_name
        )

        return True

    except Exception as e:
        print(e)
        return False