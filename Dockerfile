FROM python:3.11

WORKDIR /src

ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app app