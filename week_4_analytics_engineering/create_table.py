from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/x/OneDrive/Documents/Python/Jan_2023/DE_Zoomcamp/week_4_analytics_engineering/.google/credentials/google_credentials.json'

client = bigquery.Client()
# # TODO(developer): Set table_id to the ID of the table to create.
# table_id = "dtc-de-375918.taxi_rides_ny.external_green_tripdata_2019"


# # TODO(developer): Set source uri prefix.
# source_uri_prefix = (
#     "gs://dtc_data_lake_dtc-de-375918/green_tripdata_2019-"
# )


project = 'dtc-de-375918'
dataset = 'taxi_rides_ny'

dataset_ref = bigquery.DatasetReference(project, dataset)

table_id = 'sample'

table = bigquery.Table(dataset_ref.table(table_id))
external_config = bigquery.ExternalConfig("CSV")
external_config.source_uris = ["gs://dtc_data_lake_dtc-de-375918/green_tripdata_2019-*.csv.gz"]
# external_config.options.skip_leading_rows = 1
table.external_data_configuration = external_config

table = client.create_table(table)

query_job = client.query('select * FROM `{}.{}` limit 10'.format(dataset, table_id))

results = query_job.result()
for row in results:
    print(row)