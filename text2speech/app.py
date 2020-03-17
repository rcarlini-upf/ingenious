from io import BytesIO
import socket

from flask import Flask, request, make_response

import t2s_pipeline as pl 

app = Flask(__name__)

pipeline = None


@app.route("/")
def hello():
    html = "<h3>Hello!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"

    return html.format(hostname=socket.gethostname())


@app.route("/text2speech")
def text2speech():
    global pipeline

    text = request.args.get('text')
    if text:
        # scores=[0.58, 0.12, 0.3]
        with BytesIO() as output:
            pipeline.process(text, output)

            response = make_response(output.getvalue())

        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=audio.wav'

        return response


if __name__ == "__main__":

    tacotron_model_path = "models/checkpoint_7800.model"
    vocoder_model_path = "models/nvidia_tacotron2_LJ11_epoch6400.pt"

    config = pl.T2SPipelineConfiguration()
    pipeline = pl.T2SPipeline(tacotron_model_path, vocoder_model_path, config)

    app.run(host='0.0.0.0', port=80)

