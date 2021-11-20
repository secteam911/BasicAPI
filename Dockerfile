FROM python:latest

WORKDIR /API

COPY related.txt related.txt

RUN pip3 install -r related.txt

COPY . . 
# to create the database 
CMD [ "python3", "app.py", "initdb"]

# to start the server 
CMD [ "python3", "app.py", "runserver", "--host=0.0.0.0"]
 
