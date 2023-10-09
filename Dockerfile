FROM python:3.8.18-slim-bullseye
LABEL maintainer=yusiwen@gmail.com

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install -y tini && rm -rf /var/lib/apt/lists/*

COPY . /scrapy
WORKDIR /scrapy
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]
