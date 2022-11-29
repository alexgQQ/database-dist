FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN apt-get update -yq && \
    apt-get install -yq gcc libmariadb-dev && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /code
CMD ["python", "main.py"]
