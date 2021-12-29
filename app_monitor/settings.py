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

BOT_NAME = 'app_monitor'

SPIDER_MODULES = ['app_monitor.spiders']
NEWSPIDER_MODULE = 'app_monitor.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'app_monitor (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

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
    'app_monitor.middlewares.AppMonitorSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'app_monitor.middlewares.AppMonitorDownloaderMiddleware': 300,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'app_monitor.pipelines.AppMonitorPipeline': 300,
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

APP_MONITOR_CONFIG_FILE = '~/.app_monitor.cfg'

SEND_MAIL = False
USE_PROXY = False
SMTP_SERVER = ''
SMTP_PORT = ''
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
SMTP_SENDER = ''
SMTP_RECEIVER = ''
PROXY_HOST = ''
PROXY_USERNAME = ''
PROXY_PASSWORD = ''

ES_ENABLE = False
ES_HOSTS = []
ES_USERNAME = ''
ES_PASSWORD = ''
ES_USE_SSL = True
ES_PORT = 443
ES_CERT = ''
ES_INDEX = ''
ES_TYPE = ''

GITHUB_USER = ''
GITHUB_ACCESS_TOKEN = ''

if not os.path.isfile(os.path.expanduser(APP_MONITOR_CONFIG_FILE)):
    SEND_MAIL = False
    USE_PROXY = False
    ES_ENABLE = False
else:
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(APP_MONITOR_CONFIG_FILE))

    SEND_MAIL = config.getboolean('mail', 'enable')
    SMTP_SERVER = config['mail']['smtp_server']
    SMTP_PORT = config['mail']['smtp_port']
    SMTP_USERNAME = config['mail']['smtp_username']
    SMTP_PASSWORD = config['mail']['smtp_password']
    SMTP_SENDER = config['mail']['sender']
    SMTP_RECEIVER = config['mail']['receiver']

    USE_PROXY = config.getboolean('proxy', 'enable')
    PROXY_HOST = config['proxy']['url']
    PROXY_USERNAME = config['proxy']['username']
    PROXY_PASSWORD = config['proxy']['password']

    ES_ENABLE = config.getboolean('elasticsearch', 'enable')
    ES_HOSTS = config.get('elasticsearch', 'hosts').split(',')
    ES_PORT = config.getint('elasticsearch', 'port')
    ES_USERNAME = config['elasticsearch']['username']
    ES_PASSWORD = config['elasticsearch']['password']
    ES_USE_SSL = config['elasticsearch']['use_ssl']
    ES_CERT = config['elasticsearch']['cert']
    ES_INDEX = config['elasticsearch']['index']
    ES_TYPE = config['elasticsearch']['type']
    if ES_TYPE == '':
        ES_TYPE = '_doc'

    GITHUB_USER = config['github']['username']
    GITHUB_ACCESS_TOKEN = config['github']['access_token']
