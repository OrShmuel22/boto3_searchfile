from flask import Flask, request
import argparse
import boto3
import json
from tqdm import tqdm

# Set up the Flask app
app = Flask(__name__)

# Set the values of the configuration, destination, and files variables
config = ""
dest = ""
files = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Set the configuration, destination, and files variables based on the user input
        config = request.form.get("config")
        dest = request.form.get("dest")
        files = request.form.getlist("files")

        # Load the configuration file
        with open(config) as f:
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
                if obj["Key"] in files:
                    # Download the file from S3
                    s3.download_file(config["bucket_name"], obj["Key"], dest + obj["Key"])
                    print(f"Successfully downloaded '{obj['Key']}' from bucket '{config['bucket_name']}'")

    return """
    <style>
    form {
        width: 500px;
        margin: 0 auto;
        padding: 10px;
        border: 1px solid #ccc;
    }

    input[type="text"],
    input[type="submit"] {
        width: 100%;
        padding: 12px;
        margin-top: 8px;
        margin-bottom: 8px;
        box-sizing: border-box;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 16px;
        font-family: sans-serif;
    }

    input[type="submit"] {
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
    }
</style>

    <form method="POST">
        Configuration file: <input type="text" name="config"><br>
        Destination directory: <input type="text" name="dest"><br>
        Files: <input type="text" name="files"><br>
        <input type="submit" value="Submit">
    </form>
    """

if __name__ == "__main__":
    app.run()
