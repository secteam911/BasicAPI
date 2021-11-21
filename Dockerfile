FROM python:latest

ENV VIRTUAL_ENV=/opt/venv 

RUN python3 -m venv $VIRTUAL_ENV

RUN python3 -m pip install --upgrade pip

WORKDIR /BasicAPI

COPY . . 

RUN pip install -r related.txt

# to create the database 
CMD [ "python", "app.py", "initdb"]

# to start the server 
CMD [ "python", "app.py", "runserver", "--host=0.0.0.0"]
 
