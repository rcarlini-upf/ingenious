from flask import Flask
import argparse
import os
import ntpath
import sox
from shutil import copyfile, rmtree
from flask import Flask, request, flash, redirect, url_for

parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', default='./audio_A.wav', type=str, help='path to audio file')
args = parser.parse_args()

app = Flask(__name__)
ALLOWED_EXTENSIONS = ['wav']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def speech2text():
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

        audio_path = args.audio_path
        container_data_path = '/ASR/data/'
        sample_id = '000000000'
        list_name = 'test.lst'
        temporal_audio_name = sample_id + '.wav'
        container_audio_path = container_data_path + temporal_audio_name
        audio_list_path = container_data_path + list_name
        container_output_path = '/ASR/results/20191126_1207'
        container_hyp_name = 'data#test.lst.hyp'

        if file and allowed_file(file.filename):
            file.save(container_audio_path)

        with open(audio_list_path, 'w') as audio_list:
            #audio_length = str(sox.file_info.duration(audio_path))
            audio_length = str(sox.file_info.duration(container_audio_path))
            transcript = '<no_transcript>'

            writeline = []
            writeline.append(sample_id)  # sampleid
            writeline.append(container_audio_path)
            writeline.append(audio_length)  # length
            writeline.append(transcript)
            audio_list.write("\t".join(writeline) + "\n")

        decoding_command = 'root/wav2letter/build/Decoder --flagsfile ASR/conf/decode.cfg'
        os.system(decoding_command)

        with open(container_output_path + '/' + container_hyp_name, 'r', encoding="utf-8") as f:
            hypothesis = f.readlines()[0].split('(')[0]
        return hypothesis

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
    app.run(host='0.0.0.0', port=80)