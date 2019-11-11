# My App Monitor Scrapy Module

## Prerequisite

```sh
pip3 install setuptools wheel scrapy packaging
```

## Setting

Copy `mail.sample.cfg` to `~/.mail.cfg`, and edit `smtp_password` with real password

## Add new spider

```sh
scrapy genspider <name> <domain>
```
