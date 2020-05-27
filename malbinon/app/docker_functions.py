import os
import math
from datetime import datetime
import docker
import time

# Global vars
CLIENT = docker.from_env(timeout=300)

if ("REDHAT_USER" in os.environ and "REDHAT_PASSWORD" in os.environ):
    REDHAT_USER = os.environ['REDHAT_USER']
    REDHAT_PASSWORD = os.environ['REDHAT_PASSWORD']
    CLIENT.login(username=REDHAT_USER, password=REDHAT_PASSWORD, registry="registry.redhat.io")
    CLIENT.login(username=REDHAT_USER, password=REDHAT_PASSWORD, registry="registry.access.redhat.com")

# Functions
def create_images_dir(base_folder):
    mydir = os.path.join(base_folder, datetime.now().strftime('%d-%m-%Y.%H-%M-%S'))
    os.makedirs(mydir)
    return mydir

def save_image(image_name, path):
    image = pull_image(image_name)
    file_name = image.tags[0].replace("/",".").replace(":","..")
    with open(f'{path}/{file_name}', 'wb') as f:
        for chunk in (image.save(named=True)):
            f.write(chunk)

def pull_image(image_name):
    try:
        image = CLIENT.images.get(image_name)
    except docker.errors.ImageNotFound:
        image = CLIENT.images.pull(image_name)
    return image

def main():
    save_image("busybox:latest","/tmp")

if __name__ == '__main__':
    main()
