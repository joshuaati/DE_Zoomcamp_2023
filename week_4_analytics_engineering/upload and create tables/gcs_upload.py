from google.cloud import storage
import requests
import os
from prefect import flow, task

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/x/OneDrive/Documents/Python/Jan_2023/DE_Zoomcamp/week_4_analytics_engineering/.google/credentials/google_credentials.json'

# prevent timeout due to low network
storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024* 1024  # 5 MB
storage.blob._MAX_MULTIPART_SIZE = 5 * 1024* 1024  # 5 MB

@task(retries=4)
def get_response(url_:str) -> bytes:
    '''Download files from a url'''
    response = requests.get(url_) #get response
    content = response.content
    return content


@task(retries=4)
def write_to_gcs(bucket_name: str, content: bytes, filename: str):
    '''Upload files to a google storage bucket'''
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)     #get bucket 

    blob = bucket.blob(filename)                    #create file
    blob.upload_from_string(content)                #upload file to bucket


@flow()
def etl_web_to_gcs(color: str, year: int, month: int) -> None:
    """Main ETL flow to load data into google storage bucket"""
    url_ = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{color}_tripdata_{year}-{month:02}.csv.gz'
    filename = f'{color}_tripdata_{year}-{month:02}.csv.gz'
    bucket_name = 'dtc_data_lake_dtc-de-375918'
    content = get_response(url_)
    write_to_gcs(bucket_name, content, filename)


@flow()
def parent_etl_web_to_gcs(color: str, year: int, months: list[int]):
    for month in months:
        etl_web_to_gcs(color, year, month)


if __name__ == '__main__':
    color = 'green'
    months = [*range(1,13)]
    year = 2019
    parent_etl_web_to_gcs(months, year)
