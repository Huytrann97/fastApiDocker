import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

def upload_image_to_s3(file_name):

    # Replace with your AWS credentials and file paths
    AWS_ACCESS_KEY = "AKIA556GHXWRODJP6BGM"
    AWS_SECRET_ACCESS_KEY = "OGA+uQTd7hQB1ZGOOMMN6lzyLyyOXAETnzmHzCL9"
    file_to_upload = "hau.jpg"  # Replace with the path to your image file
    s3_bucket_name = "maintokyo"

    if object_name is None:
        object_name = file_name  # Use the same file name as the object name in S3

    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Upload the file to S3
        s3.upload_file(file_name, bucket_name, object_name)

        print(f"Upload successful: {object_name}")
        return True

    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return False

    except NoCredentialsError:
        print("AWS credentials not available.")
        return False


# s3_object_name = "image.jpg"  # Optional: specify a different object (S3 key) name

# Set AWS credentials (you can also use environment variables or IAM roles)
boto3.setup_default_session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Upload the image to S3
upload_image_to_s3(file_to_upload, s3_bucket_name)
# upload_image_to_s3(file_to_upload, s3_bucket_name, s3_object_name)
