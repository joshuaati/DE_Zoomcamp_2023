


`docker image tag ae5772c94203 dbt_all:1.0` 


docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-dtc run --select stg_green_tripdata