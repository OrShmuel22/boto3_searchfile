import argparse
import boto3
import json
from tqdm import tqdm

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Search and download files from an S3 bucket")
parser.add_argument("--config", required=True, help="Path to the configuration file")
parser.add_argument("--dest", required=True, help="Destination directory for the downloaded files")
parser.add_argument("--files", nargs="+", required=True, help="Names of the files to search for")
args = parser.parse_args()

# Load the configuration file
with open(args.config) as f:
    config = json.load(f)

# Initialize the S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=config["access_key_id"],
    aws_secret_access_key=config["secret_access_key"],
    aws_session_token=config["session_token"],
)

# Set the pagination parameters for the list_objects_v2 method
paginator = s3.get_paginator("list_objects_v2")
page_iterator = paginator.paginate(Bucket=config["bucket_name"])

# Iterate over the pages of results
for page in tqdm(page_iterator, desc="Searching for files"):
    # Iterate over the objects in the current page of results
    for obj in page["Contents"]:
        if obj["Key"] in args.files:
            # Download the file from S3
            s3.download_file(config["bucket_name"], obj["Key"], args.dest + obj["Key"])
            print(f"Successfully downloaded '{obj['Key']}' from bucket '{config['bucket_name']}'")
