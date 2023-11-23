FROM python:3.11
LABEL authors="ilmir.ziganshin"

RUN apt-get update -y && pip install --upgrade pip
WORKDIR /usr/src/mysite
COPY req.txt ./
RUN pip install -r req.txt
COPY . .

ENTRYPOINT ["top", "-b"]