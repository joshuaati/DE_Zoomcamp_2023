

- To start orion 
`prefect orion start`

- To build a deployment
`prefect deployment build parameterized_flow.py:etl_parent_flow -n "Parameterized ETL" `
Where 
`parameterized_flow.py` is the name of the file
`etl_parent_flow` is the entry flow point 

It outputs
`etl_parent_flow-deployment.yaml` that contains the necessary instructions for prefect to execute

- To apply a deployment
`prefect deployment apply etl_parent_flow-deployment.yaml`

- To run the workqueue
`prefect agent start --work-queue "default"` 