FROM python:3.6-slim as prod-build

LABEL maintainer="Sandeep Aggarwal <asandeep.me@gmail.com>"

# Environment varialbes to control python and pip behaviour.
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /pseudo

COPY requirements.txt /pseudo/

# Install Pseudo electronics django server requirements.
RUN pip install -r /pseudo/requirements.txt

COPY . /pseudo/

ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD ["python", "manage.py", "runserver"]
