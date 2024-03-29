FROM --platform=$TARGETPLATFORM python:3.8.18-slim-bullseye AS builder
LABEL maintainer=yusiwen@gmail.com

ARG TARGETPLATFORM
ARG TARGETARCH
ARG BRANCH=master

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install -y git
RUN git clone --branch=$BRANCH --depth=1 https://github.com/yusiwen/app_monitor.git /scrapy

WORKDIR /scrapy
RUN pip install -r requirements.txt && \
    python setup.py bdist_egg

FROM --platform=$TARGETPLATFORM python:3.8.18-slim-bullseye
LABEL maintainer=yusiwen@gmail.com

ARG TARGETPLATFORM
ARG TARGETARCH

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install -y tini && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./scrapyd.conf /etc/scrapyd/scrapyd.conf
COPY --from=builder /scrapy/dist/app_monitor-1.0-py3.8.egg /scrapyd/eggs/app_monitor/app_monitor.egg

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["scrapyd"]

EXPOSE 6800