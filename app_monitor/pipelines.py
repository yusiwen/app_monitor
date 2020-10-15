# -*- coding: utf-8 -*-
import os
import errno
import logging

from packaging import version
from app_monitor import settings
from app_monitor import mail

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AppMonitorPipeline(object):

    def _write_data(self, filename, item):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    logging.error('Error: ' + os.strerror(exc.errno))
                    raise
        with open(filename, "w") as f:
            f.write(item['version'])

    def _check_version(self, item):
        filename = os.getcwd() + '/output/' + item['id']
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                data = file.readline()
                if version.parse(data) < version.parse(item['version']):
                    self._send_mail(item)
                else:
                    logging.info('No Update found, skipping...')
        else:
            if settings.SEND_MAIL:
                mail.send_mail(item)
        self._write_data(filename, item)

    def process_item(self, item, spider):
        logging.debug("current directory is: " + os.getcwd())
        logging.debug(item)
        self._check_version(item)
        return item
