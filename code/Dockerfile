FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python-is-python3 curl ca-certificates wait-for-it libpq-dev python3-dev build-essential gettext-base \
    proj-bin proj-data libgeos-dev libgdal-dev && \ 
    rm -rf /var/lib/apt/lists/*

ENV \
  LANG="C.UTF-8" \
  LC_ALL="C.UTF-8" 

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.3

RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/


RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --ansi

COPY . /code

CMD ["rq-dashboard"]
