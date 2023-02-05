

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



## To create a deployment from phython file and docker,
- To build docker image
first create the Dockerfile then run
`docker image build -t joshuaati/prefect:zoomcamp .`
push the image to online repo
`docker image push joshuaati/prefect:zoomcamp`

create the docker block on prefect orion server using `joshuaati/prefect:zoomcamp` as image url

create the `docker_deploy.py` file with the prefect block code

check the profile available
`prefect profile ls`

make docker to interface with orion server
`prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"`

start docker agent
`prefect agent start -q default`

run the task. parameters can be changed using -p argument
`prefect deployment run etl-parent-flow/docker-flow -p "months=[1]"`

Deploy from github
`prefect deployment build flows/02_gcp/etl_web_to_gcs.py:etl_web_to_gcs --name github_deploy --apply -sb github/github-block`