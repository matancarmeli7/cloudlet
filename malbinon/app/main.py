from flask import Flask, request, render_template, Response, redirect, stream_with_context
import docker_functions as df
import forms
import time
import os

app = Flask(__name__, static_folder='/static')
app.config['SECRET_KEY'] = 'ananongo123123nogiveup'

HOST_IP = os.environ['HOST_IP']

@app.route('/')
def index_form():
    form = forms.IndexForm()
    return render_template('index.html', title='Malbinon', form=form)

@app.route('/', methods=['POST'])
def my_form_post():
    newdir = df.create_images_dir("/app/static")
    form = forms.IndexForm()
    if form.validate_on_submit():
        images_list = [x for x in form.image_list.data.split("\r\n") if not x.isspace() and x]

    def generate():
        len_images_list = len(images_list)
        bad_images = []
        # Pull images
        yield f"Starting pulling images<br><br>"
        for c, image in enumerate(images_list, 1):
            try:
                yield f"pulling {image}... --> "
                df.pull_image(image)
                yield f"success!<br>"
            except Exception as e:
                yield f"could not pull {image}, error of type {type(e).__name__} occured.<br>"
                bad_images.append(f"{image}")
                continue
        yield f"pulled {len_images_list - len(bad_images)}/{len_images_list} images<br><br>"
        # clean image list
        for bad_image in bad_images:
            images_list.remove(bad_image)
        # Save images
        yield f"Starting saving images<br><br>"
        for c, image in enumerate(images_list, 1):
            try:
                yield f"saving {image}... --> "
                df.save_image(image, newdir)
                yield f"success!<br>"
            except Exception as e:
                yield f"could not save {image}, error of type {type(e).__name__} occured.<br>"
                continue

        yield f"<br><br>Finished! your images are at: https://{HOST_IP}/static/{newdir.split('/')[-1]}/<br><br>"
        yield render_template('link.html',link_url=f"https://{HOST_IP}/static/{newdir.split('/')[-1]}/")

    resp = Response(stream_with_context(generate()))
    resp.headers['X-Accel-Buffering'] = 'no'

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=555) 
