import logging
import boto3
import uuid
from botocore.exceptions import ClientError

from backend import config


def get_s3_client(**kwargs):
    return boto3.client(
        's3',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        **kwargs
    )


def upload_file(file_path, object_name, bucket=config.AWS_S3_BUCKET):
    if not object_name:
        object_name = uuid.uuid4().hex

    s3_client = get_s3_client()

    try:
        s3_client.upload_file(file_path, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return None

    return f'https://{bucket}.s3-us-west-2.amazonaws.com/{object_name}'


def delete_file(document_url, bucket=config.AWS_S3_BUCKET):
    object_name = document_url.replace(f'https://{bucket}.s3-us-west-2.amazonaws.com/', '')

    s3_client = get_s3_client()

    try:
        s3_client.delete_object(Key=object_name, Bucket=bucket)
    except ClientError as e:
        logging.error(e)
        return False

    return True


def generate_presigned_url(
    document_url,
    expires_in=config.DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC,
    bucket=config.AWS_S3_BUCKET
):
    object_name = document_url.replace(f'https://{bucket}.s3-us-west-2.amazonaws.com/', '')

    s3_client = get_s3_client()
    return s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': object_name
        },
        ExpiresIn=expires_in
    )
