SELECT COUNT(*)
FROM green_taxi_trips_201901
WHERE lpep_pickup_datetime::Date = '2019-01-15'
AND lpep_dropoff_datetime::Date = '2019-01-15'

SELECT lpep_pickup_datetime, trip_distance
FROM green_taxi_trips_201901
ORDER BY trip_distance DESC

SELECT passenger_count, COUNT(*)
FROM green_taxi_trips_201901
WHERE lpep_pickup_datetime::DATE = '2019-01-01'
AND passenger_count IN (2, 3)
GROUP BY passenger_count

SELECT "Zone" FROM taxi_zone WHERE "LocationID" IN 
(SELECT "DOLocationID" FROM (SELECT "DOLocationID",  MAX(tip_amount)
FROM green_taxi_trips_201901
WHERE "PULocationID" = (SELECT "LocationID" FROM taxi_zone WHERE "Zone" = 'Astoria')
GROUP BY "DOLocationID"
ORDER BY MAX DESC
LIMIT 1) AS max_tip)