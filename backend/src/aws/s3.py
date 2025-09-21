import json
from pathlib import Path
from botocore.exceptions import ClientError
from ..config import (
    MINIO_BUCKET, MINIO_ENDPOINT, public_minio_url, aws_session
)


s3_client = aws_session.client(
    service_name="s3",
    endpoint_url=MINIO_ENDPOINT
)


def _format_bucket_name(policy: dict, bucket_name: str):
    policy["Statement"][0]["Resource"] = policy["Statement"][0]["Resource"].format(
        bucket_name=bucket_name
    )


def upload_image(
    name: str, content: bytes,
    bucket_name: str = MINIO_BUCKET,
    client=s3_client
):
    client.put_object(
        Bucket=bucket_name,
        Key=name,
        Body=content,
        ContentType="image/png",
        ACL="public-read"
    )
    return public_minio_url + name


def upload_file(
    name: str, content: bytes,
    bucket_name: str = MINIO_BUCKET,
    client=s3_client
):
    client.put_object(
        Bucket=bucket_name,
        Key=name,
        Body=content,
        ACL="public-read"
    )
    return public_minio_url + name


def delete_file(name: str, bucket_name: str = MINIO_BUCKET, client=s3_client):
    client.delete_object(
        Bucket=bucket_name, Key=name
    )


def setup_bucket(bucket_name: str = MINIO_BUCKET, client=s3_client):
    try:
        client.head_bucket(Bucket=bucket_name)
        return
    except ClientError:
        pass

    client.create_bucket(
        Bucket=bucket_name,
        ACL="public-read"
    )

    policy_path = Path(__file__).parent.joinpath("policy.json").resolve()
    with open(policy_path) as file:
        policy = json.load(file)
        _format_bucket_name(policy, bucket_name)

    client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(policy)
    )
