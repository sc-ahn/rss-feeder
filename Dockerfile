# stage 1: Extract dependencies from pyproject.toml and generate requirements.txt
FROM python:3.11.10-bullseye

ENV POETRY_VERSION=1.8.3 POETRY_HOME=/poetry
ENV PATH=/poetry/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /rss-follow-up
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

# stage 2: Install dependencies and copy the rest of the files
FROM python:3.11.10-alpine
WORKDIR /rss-follow-up
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=0 /rss-follow-up/requirements.txt ./
COPY scripts scripts
COPY Makefile Makefile
COPY main.py main.py
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev
RUN pip install --no-cache-dir -r requirements.txt
