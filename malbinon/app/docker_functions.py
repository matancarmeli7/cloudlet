import os
import math
from datetime import datetime
import docker
import time

# Global vars
CLIENT = docker.from_env()

# Functions
def create_images_dir(base_folder):
    mydir = os.path.join(base_folder, datetime.now().strftime('%d-%m-%Y.%H-%M-%S'))
    os.makedirs(mydir)
    return mydir

def save_image(image_name, path):
    image = CLIENT.images.get(image_name)
    file_name = image.tags[0].replace("/",".").replace(":","..")
    f = open(f'{path}/{file_name}', 'wb')
    for c ,chunk in enumerate(image.save(named=True)):
        f.write(chunk)
    f.close()

def pull_image(image_name):
    try:
        image = CLIENT.images.get(image_name)
    except docker.errors.ImageNotFound:
        image = CLIENT.images.pull(image_name)
    return image

# Main
def main():
    print("ma lo porim hayom?")

if __name__ == '__main__':
    main()
