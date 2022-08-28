#Deriving the latest base image
FROM python:3.9.13-alpine3.16

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/src

#to COPY the remote file at working directory in container
COPY ./src /usr/src
# Now the structure looks like this '/my_server.py'

EXPOSE 5000

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python3", "./main.py"]