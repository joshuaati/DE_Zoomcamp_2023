from google.cloud import storage
import requests
import os
from prefect import flow, task

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/x/OneDrive/Documents/Python/Jan_2023/DE_Zoomcamp/week_4_analytics_engineering/.google/credentials/google_credentials.json'


@task()
def get_response(url_):
    response = requests.get(url_)
    content = response.content
    return content


@task()
def write_to_gcs(bucket_name: str, content: bytes, filename: str):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(filename)
    blob.upload_from_string(content)


@flow()
def etl_web_to_gcs(color: str, year: int, month: int) -> None:
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
