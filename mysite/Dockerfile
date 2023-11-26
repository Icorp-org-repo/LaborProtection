FROM python:3.11

RUN apt-get update -y && pip install --upgrade pip
WORKDIR /usr/src/mysite
COPY req.txt ./
RUN pip install -r req.txt
COPY . .
