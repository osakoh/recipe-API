FROM python:3.7-alpine
LABEL authors="Michael Osakoh"

ENV PYTHONUNBUFFERED 1

# switch to the app folder located in the project directory 
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# install postgresql client
# --no-cache: don't store the registry index
RUN apk add --update --no-cache postgresql-client
# setup alias for installing some temporary dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# install requirements
RUN pip install -r requirements.txt
# delete dependencies using the alias above
RUN apk del .tmp-build-deps


# create app folder in the linux image
RUN mkdir -p /app
# switch to app folder  
WORKDIR /app 
# copy files from the app folder to the app folder in the linux image
COPY ./app /app

# creates a new user in the linux image
# RUN useradd -ms /bin/bash user
# switch to the user instead of the root user
USER user