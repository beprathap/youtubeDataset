import os
import boto3
import botocore
from datetime import datetime

def create_s3_bucket(bucket_name, region='us-east-1'):
    s3 = boto3.client('s3', region_name=region)
    try:
        # Check if the bucket already exists
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print(f"Bucket {bucket_name} does not exist. Creating now...")
            try:
                if region == 'us-east-1':
                    s3.create_bucket(Bucket=bucket_name)
                else:
                    s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                print(f"Bucket {bucket_name} created successfully.")
            except Exception as e:
                print(f"Error creating bucket: {e}")
        else:
            print(f"Unexpected error: {e}")

def upload_files_to_s3(local_folder, bucket_name):
    s3 = boto3.client('s3')

    # Get current date for organizing files
    extraction_date = datetime.now().strftime('%Y/%m/%d')

    # Iterate over files in the local folder
    for root, dirs, files in os.walk(local_folder):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)

            # Construct S3 key with the folder structure
            s3_key = f"RAW/{extraction_date}/{file_name}"

            try:
                # Upload the file to S3
                s3.upload_file(local_file_path, bucket_name, s3_key)
                print(f"Uploaded {file_name} to s3://{bucket_name}/{s3_key}")
            except Exception as e:
                print(f"Error uploading {file_name}: {str(e)}")