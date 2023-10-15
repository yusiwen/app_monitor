# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name='app_monitor',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = app_monitor.settings']},
)
