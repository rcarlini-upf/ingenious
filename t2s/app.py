from flask import Flask

import os
import socket

import time
import sys
import torch
import numpy as np
from playsound import playsound
from scipy.io.wavfile import write

sys.path.append('/text2speech_folder')  # folder where GST_Tacotron2 and MelGAN projects are located

from hyper_parameters import tacotron_params
from training import load_model
from text import text_to_sequence

from melgan.model.generator import Generator
from melgan.utils.hparams import load_hparam

# Override warn function in warnings to mute it
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

TORCH_RANDOM_SEED = 1234
TORCH_DEVICE = 'cpu'


app = Flask(__name__)

model = None
vocoder_model = None


@app.route("/")
def hello():
    html = "<h3>Hello!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"

    return html.format(hostname=socket.gethostname())

def initialize():
    global model, vocoder_model

    torch.manual_seed(TORCH_RANDOM_SEED)

    # load trained tacotron 2 model:
    hparams = tacotron_params
    checkpoint_path = "models/checkpoint_78000"
    model = load_model(hparams)
    model.load_state_dict(torch.load(checkpoint_path, map_location='cpu')['state_dict'])
    _ = model.eval()

    # load pre trained MelGAN model for mel2audio:
    vocoder_checkpoint_path = "models/nvidia_tacotron2_LJ11_epoch6400.pt"
    checkpoint = torch.load(vocoder_checkpoint_path, map_location='cpu')
    # hp_melgan = load_hparam("melgan/config/default.yaml")
    vocoder_model = Generator(80)  # Number of mel channels
    vocoder_model.load_state_dict(checkpoint['model_g'])
    vocoder_model.eval(inference=False)

def process(text, scores=[0.58, 0.12, 0.3]):
    global model, vocoder_model

    save_path = '/text2speech_folder/test_speech_cpu.wav'

    # set the GST scores you desire for speaking style:
    gst_head_scores = np.array(scores)

    gst_scores = torch.from_numpy(gst_head_scores)
    gst_scores = torch.autograd.Variable(gst_scores).float()

    test_text = "Life is wonderful"

    sequence = np.array(text_to_sequence(text, ['english_cleaners']))[None, :]
    sequence = torch.from_numpy(sequence).to(device='cpu', dtype=torch.int64)
    print("Input text sequence pre-processed successfully...")

    # text2mel:
    t1 = time.time()
    with torch.no_grad():
      mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence, 
                                                                        gst_scores)
    elapsed = time.time() - t1
    print('Time elapsed in transforming text to mel has been {} seconds.'.format(elapsed))

    # mel2wav inference:
    t2 = time.time()
    with torch.no_grad():
      audio = vocoder_model.inference(mel_outputs_postnet)

    audio_numpy = audio.data.cpu().detach().numpy()
    elapsed_melgan = time.time() - t2

    print('Time elapsed in transforming mel to wav has been {} seconds.'.format(elapsed_melgan))

    write(save_path, 22050, audio_numpy)
    # ipd.Audio(audio_numpy, rate=22050)


@app.route("/text2speech")
def text2speech():
    result = process("Life is wonderful")
    return "<h3>Processed successfully!</h3>"


if __name__ == "__main__":
    initialize()
    app.run(host='0.0.0.0', port=80)

