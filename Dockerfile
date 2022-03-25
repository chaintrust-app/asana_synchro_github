# Container image that runs your code
FROM python:3.8.10
WORKDIR /code

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY requirements.txt /code/requirements.txt 
RUN pip install -r /code/requirements.txt
COPY asanaProject.py /code/asanaProject.py
COPY entrypoint.sh /code/entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/code/entrypoint.sh"]