FROM python:3.8-alpine
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

# to avoid Pillow installation error
RUN python3 -m pip install --upgrade pip

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

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user


## creates a new user in the linux image
#RUN useradd -ms /bin/bash user
## switch to the user instead of the root user
#USER user


#FROM python:3.8-alpine
#LABEL authors="Michael Osakoh"
#
#ENV PYTHONUNBUFFERED 1
#
#COPY ./requirements.txt /requirements.txt
#RUN apk add --update --no-cache postgresql-client jpeg-dev
#RUN apk add --update --no-cache --virtual .tmp-build-deps \
#      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
#RUN pip install -r /requirements.txt
#RUN apk del .tmp-build-deps
#
#RUN mkdir /app
#WORKDIR /app
#COPY ./app /app
#
#RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static
#RUN adduser -D user
#RUN chown -R user:user /vol/
#RUN chmod -R 755 /vol/web
#USER user