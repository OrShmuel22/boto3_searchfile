import boto3

# Replace with your own bucket name and secret key
bucket_name = "my-s3-bucket"
secret_key = "my-secret-key"

# Initialize the S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id="",
    aws_secret_access_key=secret_key,
    aws_session_token="",
)

# Replace with the names of the files you want to search for
file_names = ["file1.txt", "file2.txt", "file3.txt"]

# Set the pagination parameters for the list_objects_v2 method
paginator = s3.get_paginator("list_objects_v2")
page_iterator = paginator.paginate(Bucket=bucket_name)

# Iterate over the pages of results
for page in page_iterator:
    # Iterate over the objects in the current page of results
    for obj in page["Contents"]:
        if obj["Key"] in file_names:
            # Download the file from S3
            s3.download_file(bucket_name, obj["Key"], obj["Key"])
            print(f"Successfully downloaded '{obj['Key']}' from bucket '{bucket_name}'")
