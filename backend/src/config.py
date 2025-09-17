import os
from dotenv import load_dotenv
from pathlib import Path

import boto3
from botocore.config import Config


load_dotenv()


POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

MINIO_ROOT_USER = os.environ.get("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.environ.get("MINIO_ROOT_PASSWORD")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET")
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")


base_minio_url = f"{MINIO_ENDPOINT}/{MINIO_BUCKET}/"
public_minio_url = f"http://localhost:9000/{MINIO_BUCKET}/"


s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ROOT_USER,
    aws_secret_access_key=MINIO_ROOT_PASSWORD,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"
)


def get_db_url():
    return (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


class S3:
    @staticmethod
    def upload_file(file_path: Path | str, file_name: str):
        s3_client.upload_file(file_path, MINIO_BUCKET, file_name)

    @staticmethod
    def upload_image(content: bytes, name: str):
        s3_client.put_object(
            Bucket=MINIO_BUCKET,
            Key=name,
            Body=content,
            ContentType="image/png",
            ACL="public-read"
        )
        return public_minio_url + name

    @staticmethod
    def delete_file(file_name: str):
        s3_client.delete_object(
            Bucket=MINIO_BUCKET, Key=file_name
        )
