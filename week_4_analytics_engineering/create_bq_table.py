from google.cloud import bigquery
# from prefect import flow, task
import os


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/x/OneDrive/Documents/Python/Jan_2023/DE_Zoomcamp/week_4_analytics_engineering/.google/credentials/google_credentials.json'

def create_bq_table(table_id, color, year):
  # Construct a BigQuery client object.
  client = bigquery.Client()

  # job_config = bigquery.QueryJobConfig(destination=table_id)

  sql = f"""
      CREATE OR REPLACE EXTERNAL TABLE dtc-de-375918.taxi_rides_ny.external_{color}_tripdata_{year}
  OPTIONS(
    format = 'CSV',
    uris = ['gs://dtc_data_lake_dtc-de-375918/{color}_tripdata_{year}-*.csv.gz']
  );
  """

  # Start the query, passing in the extra configuration.
  query_job = client.query(sql) #job_config=job_config)  # Make an API request.
  query_job.result()  # Wait for the job to complete.

  print("Query results loaded to the table {}".format(table_id))


def main(color, year):
  table_id = f"dtc-de-375918.taxi_rides_ny.external_{color}_tripdata_{year}"
  create_bq_table(table_id, color, year)

if __name__ == '__main__':
    color = 'green'
    year = 2019
    main(color, year)
    

