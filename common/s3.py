import logging
import boto3
import uuid
from botocore.exceptions import ClientError

from backend import config


def upload_file(file_path, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_path is used
    :return: True if file was uploaded, else False
    """

    if not object_name:
        object_name = uuid.uuid4().hex

    s3_client = boto3.client(
        's3',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return None

    return f'https://{bucket}.s3-us-west-2.amazonaws.com/{object_name}'


def delete_file(file_url, bucket=config.AWS_S3_BUCKET):
    object_name = file_url.replace(f'https://{bucket}.s3-us-west-2.amazonaws.com/', '')

    s3_client = boto3.client(
        's3',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    try:
        s3_client.delete_object(Key=object_name, Bucket=bucket)
    except ClientError as e:
        logging.error(e)
        return False

    return True
