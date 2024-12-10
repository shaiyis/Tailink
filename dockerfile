FROM python:3.9-alpine3.13

# who is maintaining the docker image
LABEL maintainer="maintainer_website"

# We don't want to buffer the output from python but it should be printed directly to the console to prevent delays
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
# copy the django app to the container 
COPY ./app /app
# the working directory for commands in our image
WORKDIR /app
# expose port 8000 from the container to our machine
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user





