from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from parameterized_flow import etl_parent_flow

docker_container_block = DockerContainer.load("zoomcamp")