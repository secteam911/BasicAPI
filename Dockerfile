FROM python:latest

RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz \
  && tar xzvf docker-17.04.0-ce.tgz \
  && mv docker/docker /usr/local/bin \
  && rm -r docker docker-17.04.0-ce.tgz

WORKDIR /API

COPY related.txt related.txt

RUN pip3 install -r related.txt

COPY . . 
# to create the database 
CMD [ "python3", "app.py", "initdb"]

# to start the server 
CMD [ "python3", "app.py", "runserver", "--host=0.0.0.0"]
 
