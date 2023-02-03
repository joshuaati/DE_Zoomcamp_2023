

- To start orion 
`prefect orion start`

- To build a deployment
`prefect deployment build flows/03_deployments/parameterized_flow.py:etl_parent_flow -n "Parameterized ETL" `
Where 
`parameterized_flow.py` is the name of the file
`etl_parent_flow` is the entry flow point 

- To build deployment with cron scheduling
`prefect deployment build flows/03_deployments/parameterized_flow.py:etl_parent_flow -n "Parameterized ETL" --cron "0 0 * * *" -a`

It outputs
`etl_parent_flow-deployment.yaml` that contains the necessary instructions for prefect to execute

- To apply a deployment
`prefect deployment apply etl_parent_flow-deployment.yaml`

- To run the workqueue
`prefect agent start --work-queue "default"` 


- To build docker image
first create the Dockerfile then run
`docker image build -t joshuaati/prefect:zoomcamp .`
push the image to online repo
`docker image push joshuaati/prefect:zoomcamp`