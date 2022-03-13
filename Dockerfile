FROM python:3.8-alpine
LABEL authors="Michael Osakoh"

# python output is sent straight to terminal (e.g. your container log) without being first buffered and
# that you can see the output of your application (e.g. django logs) in real time. It also ensures that no
# partial output is held in a buffer somewhere and never written in case the python application crashes.
ENV PYTHONUNBUFFERED 1

# switch to the app folder located in the project directory
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# install postgresql client
# --no-cache: don't store the registry index
RUN apk add --update --no-cache postgresql-client jpeg-dev
# --virtual .tmp-build-deps: temporary build dependencies: sets up alias for removing these dependencies later
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib libjpeg zlib-dev

# to avoid Pillow installation error pip install --user
# RUN python3 -m pip install --user --upgrade pip

# install requirements
RUN pip install -r requirements.txt
# delete temporary dependencies using the alias above(.tmp-build-deps)
RUN apk del .tmp-build-deps


# create app folder in the linux image
RUN mkdir -p /app
# switch to app folder
WORKDIR /app
# copy files from the app folder to the app folder in the linux image
COPY ./app /app


# -p: make subdirectories as well
# stores images
RUN mkdir -p /vol/web/media
# stores static(JS, CSS, etc) files
RUN mkdir -p /vol/web/static
## creates a new user in the linux image
#RUN useradd -ms /bin/bash user
RUN adduser -D user
# assign ownership of the vol directory to the user
# -R: recursive
RUN chown -R user:user /vol/
#user/owner has read, write, & execute permission
RUN chmod -R 755 /vol/web
## switch to the user instead of the root user
USER user