Step 1) Open a terminal here and run:

docker build -f Dockerfile.dms -t speechie .

Step 2) Copy the image ID from the created image and run the container, calling to the speech2text.py script as seen below:

docker run -it -p 4000:80 --rm speechie

Step 3) If there are problems with the server, try "docker ps -a", and get the port direction from the container "s2t", which looks like "0.0.0.0:32806->80/tcp". Copy "0.0.0.0:32806" to the web browser and profit.
