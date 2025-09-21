import json
import pytest
import boto3
from moto import mock_aws
from src.aws import s3


@pytest.fixture(scope="session")
def bucket_name():
    return "test-bucket"


@pytest.fixture(scope="module")
def mock_aws_session():
    with mock_aws():
        yield boto3.Session(region_name="us-east-1")


@pytest.fixture(scope="module")
def mock_s3_client(mock_aws_session):
    yield mock_aws_session.client("s3")


@pytest.fixture(scope="module", autouse=True)
def mock_bucket(mock_s3_client, bucket_name):
    s3.setup_bucket(bucket_name, client=mock_s3_client)


def test_bucket_creation(mock_s3_client, bucket_name):
    mock_s3_client.head_bucket(Bucket=bucket_name)


def test_bucket_policy(mock_s3_client, bucket_name):
    response = mock_s3_client.get_bucket_policy(
        Bucket=bucket_name
    )
    policy = json.loads(response["Policy"])
    assert policy["Statement"][0]["Sid"] == "AllowPublicRead"


def test_upload_and_delete_file(mock_s3_client, bucket_name):
    file_content = b"1,2,3"
    file_name = s3.upload_file(
        name="file.csv",
        content=file_content,
        bucket_name=bucket_name,
        client=mock_s3_client
    )
    assert file_name.split("/")[-1] == "file.csv"

    s3.delete_file(
        name="file.csv", bucket_name=bucket_name, client=mock_s3_client
    )
