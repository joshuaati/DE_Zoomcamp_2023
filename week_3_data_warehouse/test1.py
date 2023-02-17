from google.cloud import storage
import requests
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/emmanuel.ogunwede/Downloads/josh-shared-sa.json'

def write_to_gcs(bucket_name, file_name, content):
    # Create a client object
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob object from the content
    blob = bucket.blob(file_name)
    blob.upload_from_string(content)

# Example usage
url_ = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet"
response = requests.get(url_)
content = response.content
write_to_gcs("dagster-proj", "api-response.parquet", content)