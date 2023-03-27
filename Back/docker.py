import subprocess
from environment_variables import load_env as le

def docker_test(container_name, port='8080'):
    '''
    docker function to build a container and test it locally
    '''
    # building the container
    subprocess.run(f"docker build -t {container_name} .", shell=True)

    # running the container on the 8080 port (by default, can be overwritte)
    subprocess.run(f"docker run -e PORT=8000 -p {port}:8000 container", shell=True) #

def docker_deploy():
    # Getting env variables defined in the env folder
    gcp_project_id, docker_image_name, gcr_multi_region, gcr_region = le.get_env_variables()

    build = f"docker build -t {gcr_multi_region}/{gcp_project_id}/{docker_image_name} ."
    subprocess.run(build, shell=True)

    # Running the docker push command with the env variables
    push = f"docker push {gcr_multi_region}/{gcp_project_id}/{docker_image_name}"
    subprocess.run(push, shell=True)

    deploy = f"gcloud run deploy --image {gcr_multi_region}/{gcp_project_id}/{docker_image_name} --region {gcr_region}"
    subprocess.run(deploy, shell=True)

if __name__ == "__main__":
    # Asking the user what he wants: testing locally or deploying to Google Container?
    type = input("Do you want to test or deploy? ")

    if type.lower() == 'test':
    # Testing: executing the docker_test function above
        docker_test("container")
    # Go to localhost://8080 to check if the api.py file works

    elif type.lower() == 'deploy':
    # Deploying: pushing local modifications to Google Container (cloud where container is hosted)
        docker_deploy()

    else:
        print("I didn't understand, please input test or deploy")
else:
    docker_deploy()
