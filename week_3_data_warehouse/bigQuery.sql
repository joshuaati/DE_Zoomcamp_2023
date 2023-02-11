

CREATE OR REPLACE EXTERNAL TABLE dtc-de-375918.trips_data_all.external_2019_tripdata
OPTIONS(
  format = 'CSV',
  uris = ['gs://dtc_data_lake_dtc-de-375918/fhv_tripdata_2019-*.csv.gzip']
);


CREATE OR REPLACE TABLE 
  dtc-de-375918.trips_data_all.bqtable_2019_non_partitoned AS 
    SELECT * 
    FROM 
        dtc-de-375918.trips_data_all.external_2019_tripdata


SELECT COUNT(DISTINCT(Affiliated_base_number)) 
FROM `dtc-de-375918.trips_data_all.bqtable_2019_non_partitoned`


CREATE OR REPLACE TABLE 
  dtc-de-375918.trips_data_all.bqtable_2019_partitoned_clustered
  PARTITION BY DATE(pickup_datetime)
  CLUSTER BY affiliated_base_number AS 
    SELECT * 
    FROM 
        dtc-de-375918.trips_data_all.external_2019_tripdata;

SELECT COUNT(*) 
FROM `dtc-de-375918.trips_data_all.bqtable_2019_partitoned_clustered` 
WHERE PUlocationID IS NULL AND DOlocationID IS NULL

SELECT DISTINCT(Affiliated_base_number) 
FROM `dtc-de-375918.trips_data_all.bqtable_2019_partitoned_clustered` 
WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31'