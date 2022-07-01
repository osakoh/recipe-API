FROM python:3.9-alpine3.13
LABEL authors="Michael Osakoh"

# adds the venv path to system PATH
ENV PATH="/py/bin:$PATH"

# python output is sent straight to terminal (e.g. your container log) without being first buffered and
# that you can see the output of your application (e.g. django logs) in real time. It also ensures that no
# partial output is held in a buffer somewhere and never written in case the python application crashes.
ENV PYTHONUNBUFFERED 1

# copy from host to docker image
# switch to the app folder located in the project directory
COPY requirements/base.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# creates virtual environment
# full path of venv to upgrade pip
# install requirements into venv
# remove tmp directory
# creates a new user(api-user) in the image: disable password, no home directory
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        api-user

# switch to the api-user
USER api-user
