FROM python:3.9
LABEL authors="Michael Osakoh"

ENV PYTHONUNBUFFERED 1

# switch to the app folder located in the project directory 
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# create app folder in the linux image
RUN mkdir -p /app
# switch to app folder  
WORKDIR /app 
# copy files from the app folder to the app folder in the linux image
COPY ./app /app

# creates a new user in the linux image
RUN useradd -ms /bin/bash user
# switch to the user instead of the root user
USER user