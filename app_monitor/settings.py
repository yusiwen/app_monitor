# -*- coding: utf-8 -*-

import configparser
import os

# Scrapy settings for app_monitor project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "app_monitor"

SPIDER_MODULES = ["app_monitor.spiders"]
NEWSPIDER_MODULE = "app_monitor.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'app_monitor (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "app_monitor.middlewares.AppMonitorSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "app_monitor.middlewares.AppMonitorDownloaderMiddleware": 300,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "app_monitor.pipelines.AppMonitorPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

APP_MONITOR_CONFIG_FILES = [
    "/etc/scrapy/app_monitor.cfg",
    "~/.config/scrapy/app_monitor.cfg",
    "~/.app_monitor.cfg",
    "~\\.app_monitor.cfg"
]

SEND_MAIL = False
USE_PROXY = False
SMTP_SERVER = ""
SMTP_PORT = ""
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
SMTP_SENDER = ""
SMTP_RECEIVER = ""
PROXY_HOST = ""
PROXY_USERNAME = ""
PROXY_PASSWORD = ""

ES_ENABLE = False
ES_HOSTS = []
ES_USERNAME = ""
ES_PASSWORD = ""
ES_USE_SSL = True
ES_PORT = 443
ES_CERT = ""
ES_INDEX = ""
ES_TYPE = ""

GITHUB_USER = ""
GITHUB_ACCESS_TOKEN = ""

PUSH_URL = ""
PUSH_TOKEN = ""


def load_config(config_file):
    print("Loading configuration from: ", config_file)
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(config_file))

    global SEND_MAIL
    SEND_MAIL = config.getboolean("mail", "enable")
    global SMTP_SERVER
    SMTP_SERVER = config["mail"]["smtp_server"]
    global SMTP_PORT
    SMTP_PORT = config["mail"]["smtp_port"]
    global SMTP_USERNAME
    SMTP_USERNAME = config["mail"]["smtp_username"]
    global SMTP_PASSWORD
    SMTP_PASSWORD = config["mail"]["smtp_password"]
    global SMTP_SENDER
    SMTP_SENDER = config["mail"]["sender"]
    global SMTP_RECEIVER
    SMTP_RECEIVER = config["mail"]["receiver"]

    global USE_PROXY
    USE_PROXY = config.getboolean("proxy", "enable")
    global PROXY_HOST
    PROXY_HOST = config["proxy"]["url"]
    global PROXY_USERNAME
    PROXY_USERNAME = config["proxy"]["username"]
    global PROXY_PASSWORD
    PROXY_PASSWORD = config["proxy"]["password"]

    global ES_ENABLE
    ES_ENABLE = config.getboolean("elasticsearch", "enable")
    global ES_HOSTS
    ES_HOSTS = config.get("elasticsearch", "hosts").split(",")
    global ES_PORT
    ES_PORT = config.getint("elasticsearch", "port")
    global ES_USERNAME
    ES_USERNAME = config["elasticsearch"]["username"]
    global ES_PASSWORD
    ES_PASSWORD = config["elasticsearch"]["password"]
    global ES_USE_SSL
    ES_USE_SSL = config["elasticsearch"]["use_ssl"]
    global ES_CERT
    ES_CERT = config["elasticsearch"]["cert"]
    global ES_INDEX
    ES_INDEX = config["elasticsearch"]["index"]
    global ES_TYPE
    ES_TYPE = config["elasticsearch"]["type"]
    if ES_TYPE == "":
        ES_TYPE = "_doc"

    global GITHUB_USER
    GITHUB_USER = config["github"]["username"]
    global GITHUB_ACCESS_TOKEN
    GITHUB_ACCESS_TOKEN = config["github"]["access_token"]

    global PUSH_URL
    PUSH_URL = config["push"]["url"]
    global PUSH_TOKEN
    PUSH_TOKEN = config["push"]["token"]

loaded = False
for file in APP_MONITOR_CONFIG_FILES:
    if os.path.isfile(os.path.expanduser(file)):
        load_config(file)
        loaded = True
        break

if not loaded:
    print("Configuration file not found!")
    exit(1)