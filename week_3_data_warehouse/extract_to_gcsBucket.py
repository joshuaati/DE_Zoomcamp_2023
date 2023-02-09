from pathlib import Path
from datetime import timedelta
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3) #cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    df= pd.read_csv(dataset_url)
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as a Parquet file"""
    path = Path(f"03_data/{dataset_file}.csv.gzip")
    df.to_csv(path, compression="gzip")
    return path


@task(retries=4)
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoomcamp-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def etl_web_to_gcs(year: int, month: int) -> None:
    """The main ETL function to extract from github into Google Cloud Storage"""

    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month:02}.csv.gz'
    df = fetch(dataset_url)
    path = write_local(df, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(months: list[int] = [1, 2], year: int = 2021):
    for month in months:
        etl_web_to_gcs(year, month)


if __name__ == '__main__':
    months = [*range(2,13)]
    year = 2019
    etl_parent_flow(months, year)