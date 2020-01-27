import os
import tempfile
import socket

from flask import Flask, request, flash, redirect, secure_filename, url_for

import pipeline as pl

ALLOWED_EXTENSIONS = ['wav']


app = Flask(__name__)

pipeline = None


@app.route("/")
def hello():
    html = "<h3>Hello!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"

    return html.format(hostname=socket.gethostname())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/speech2text")
def speech2text():
    global pipeline

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            with tempfile.NamedTemporaryFile() as fd:
                file.save(fd)
                result = pipeline.process(fd.name)

            return result

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":

    pipeline = pl.S2TPipeline()

    app.run(host='0.0.0.0', port=80)

