import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")


def upload_image_to_s3(file_name):
    file_path = os.path.join("processing_image", file_name)
    try:
        s3 = boto3.client(
            "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
        )
        # s3.upload_file(file_name, s3_bucket_name, file_name)
        s3.upload_file(file_path, s3_bucket_name, file_name)
        print("File uploaded to S3 successfully")
        
        return True
    
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
def get_s3_image_url(file_name):
    try:
        s3 = boto3.client(
            "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
        )
        region = s3.get_bucket_location(Bucket=s3_bucket_name)['LocationConstraint']
        file_url = f"https://{s3_bucket_name}.s3.{region}.amazonaws.com/{file_name}"
        return file_url
    
    except Exception as e:
        print(f"Get s3 image url failed: {e}")
        return False
