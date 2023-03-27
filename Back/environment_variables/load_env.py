import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env_variables.txt')
load_dotenv(dotenv_path)

def get_env_variables():
    #
    gcp_project_id = os.environ.get("GCP_PROJECT_ID")
    docker_image_name = os.environ.get("DOCKER_IMAGE_NAME")
    gcr_multi_region = os.environ.get("GCR_MULTI_REGION")
    gcr_region = os.environ.get("GCR_REGION")
    return gcp_project_id, docker_image_name, gcr_multi_region, gcr_region

if __name__ == '__main__':
    print(dotenv_path)
    gcp_project_id, docker_image_name, gcr_multi_region, gcr_region = get_env_variables()
    print(gcp_project_id)
    print(docker_image_name)
    print(gcr_multi_region)
    print(gcr_region)
