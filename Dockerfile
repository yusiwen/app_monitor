FROM python:3.8.18-slim-bullseye AS builder

ARG BRANCH=master

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y git tini
RUN git clone --branch=$BRANCH --depth=1 https://github.com/yusiwen/app_monitor.git /scrapy

WORKDIR /scrapy
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt && \
    pip install scrapyd==1.4.3 scrapyd-client==1.2.3 && \
    python setup.py bdist_egg

FROM python:3.8.18-slim-bullseye
LABEL maintainer=yusiwen@gmail.com

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=builder /usr/bin/tini /usr/bin/tini
COPY --from=builder /scrapy/.venv/ /scrapy/.venv/
COPY --from=builder /scrapy/scrapyd.conf /etc/scrapyd/scrapyd.conf
COPY --from=builder /scrapy/dist/app_monitor-1.0-py3.8.egg /scrapy/eggs/app_monitor/app_monitor.egg

WORKDIR /scrapy

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["bash", "-c", "source .venv/bin/activate && scrapyd"]

EXPOSE 6800