from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month:int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoomcamp-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f'data/')
    return Path(f"{gcs_path}")


# @task(log_prints=True)
# def transform(path: Path) -> pd.DataFrame:
#     """Data cleaning example"""
#     df = pd.read_parquet(path)
#     print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
#     df['passenger_count'].fillna(0, inplace=True)
#     print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
#     return df

@task(log_prints=True)
def read(path: Path) -> pd.DataFrame:
    """Read the dataframe"""
    df = pd.read_parquet(path)
    print(f'read {df.shape[0]} rows')
    return df


@task(retries=3)
def write_bq(df: pd.DataFrame, color: str, year: int, month:int) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("zoomcamp-gcp-creds")
    df.to_gbq(
        destination_table=f"trips_data_all.{color}_tripdata_{year}-{month:02}",
        project_id="dtc-de-375918",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq(year: int, month: int, color: str) -> None:
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    df = read(path)
    write_bq(df, color, year, month)

@flow()
def etl_parent_bq(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    for month in months:
       etl_gcs_to_bq(year, month, color)


if __name__ == "__main__":
    color = "yellow"
    months = [1, 2, 3]
    year = 2021
    etl_parent_bq(months, year, color)