# My App Monitor Scrapy Module

## Prerequisite

```sh
pip3 install setuptools wheel scrapy packaging elasticsearch
```

## Setting

Copy `app_monitor.sample.cfg` to `~/.app_monitor.cfg`, and replace with real settings

## Start crawl spider

`scrapy crawl <spider_name>`

## Add new spider

```sh
scrapy genspider <name> <domain>
```
