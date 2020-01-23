from flask import Flask
import argparse
import os
import ntpath
import sox
from shutil import copyfile, rmtree

parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', default='./audio_A.wav', type=str, help='path to audio file')
args = parser.parse_args()

app = Flask(__name__)

@app.route("/")
def speech2text():
    audio_path = args.audio_path
    container_data_path = '/ASR/data/'
    sample_id = '000000000'
    list_name = 'test.lst'
    temporal_audio_name = sample_id + '.wav'
    container_audio_path = container_data_path + temporal_audio_name
    audio_list_path = container_data_path + list_name
    container_output_path = '/ASR/results/20191126_1207'
    container_hyp_name = 'data#test.lst.hyp'

    with open(audio_list_path, 'w') as audio_list:
        audio_length = str(sox.file_info.duration(audio_path))
        transcript = '<no_transcript>'

        writeline = []
        writeline.append(sample_id)  # sampleid
        writeline.append(container_audio_path)
        writeline.append(audio_length)  # length
        writeline.append(transcript)
        audio_list.write("\t".join(writeline) + "\n")

    copy_command = 'cp ' + audio_path + ' ' + container_audio_path
    os.system(copy_command)

    decoding_command = 'root/wav2letter/build/Decoder --flagsfile ASR/conf/decode.cfg'
    os.system(decoding_command)

    with open(container_output_path + '/' + container_hyp_name, 'r', encoding="utf-8") as f:
        hypothesis = f.readlines()[0].split('(')[0]
    return hypothesis

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)