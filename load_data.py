import os
import boto3
import logging
import requests
from io import BytesIO

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3', region_name='eu-central-1')  # Frankfurt

def extract(api_url, api_key):
    """Fetches data from a given API using an API key."""
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.content

def load(data, bucket_name, object_name):
    """Loads the data into S3."""
    create_bucket(bucket_name)
    enable_encryption(bucket_name)
    set_lifecycle_policy(bucket_name)
    upload_data_to_s3(bucket_name, data, object_name)

def create_bucket(bucket_name):
    """Creates an S3 bucket."""
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})
        logger.info(f'Bucket {bucket_name} created.')
    except s3.exceptions.BucketAlreadyOwnedByYou:
        logger.warning(f'Bucket {bucket_name} already exists.')
    except s3.exceptions.BucketAlreadyExists:
        logger.error(f'The requested bucket name {bucket_name} is already in use by someone else.')
    except Exception as e:
        logger.error(f'An error occurred while creating bucket: {e}')

def enable_encryption(bucket_name):
    """Enables server-side encryption for the bucket."""
    try:
        s3.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        )
        logger.info(f'Server-side encryption enabled for {bucket_name}.')
    except Exception as e:
        logger.error(f'An error occurred while enabling encryption: {e}')

def set_lifecycle_policy(bucket_name):
    """Sets a basic lifecycle policy to transition objects to Glacier after 30 days."""
    policy = {
        "Rules": [
            {
                "Status": "Enabled",
                "Transitions": [
                    {
                        "Days": 30,
                        "StorageClass": "GLACIER"
                    }
                ]
            }
        ]
    }
    try:
        s3.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=policy)
        logger.info(f'Lifecycle policy set for {bucket_name}.')
    except Exception as e:
        logger.error(f'An error occurred while setting lifecycle policy: {e}')

def upload_data_to_s3(bucket_name, data, object_name):
    """Uploads data to the specified S3 bucket."""
    try:
        buffer = BytesIO(data)
        s3.upload_fileobj(buffer, bucket_name, object_name)
        logger.info(f'Data uploaded to {bucket_name}/{object_name}.')
    except Exception as e:
        logger.error(f'An error occurred while uploading data: {e}')

def lambda_handler(event, context):
    api_url = os.environ.get('API_URL', "https://example.com/api/data")
    api_key = os.environ.get('API_KEY')
    
    if not api_key:
        logger.error('API key is not set in environment variables.')
        return {
            'statusCode': 500,
            'body': 'API key is missing.'
        }

    bucket_name = "your-bucket-name"
    object_name = "data_from_api.json"
    
    try:
        data = extract(api_url, api_key)
        load(data, bucket_name, object_name)
        return {
            'statusCode': 200,
            'body': f'Data uploaded to {bucket_name}/{object_name}.'
        }
    except requests.RequestException as e:
        logger.error(f'An error occurred while fetching data from the API: {e}')
        return {
            'statusCode': 500,
            'body': 'Error fetching data from the API.'
        }
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return {
            'statusCode': 500,
            'body': 'Unexpected error occurred.'
        }
