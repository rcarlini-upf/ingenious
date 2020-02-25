FROM python:3.6

RUN apt-get update

RUN apt-get install -y git

RUN git clone https://github.com/AlexMIIS/GST_Tacotron2.git text2speech_folder

RUN git clone https://github.com/seungwonpark/melgan.git text2speech_folder/melgan

RUN pip3 install torch==1.3.1+cu92 torchvision==0.4.2+cu92 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install -r text2speech_folder/requirements.txt

RUN pip install flask

ADD t2s_pipeline.py /t2s_pipeline.py

ADD app.py /app.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "/app.py"]
