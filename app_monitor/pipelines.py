# -*- coding: utf-8 -*-
import os
import errno
import logging

import json

from packaging import version
from app_monitor import settings
from app_monitor import mail
from app_monitor import es

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AppMonitorPipeline(object):

    def _get_previous_version_from_file(self, item):
        file_name = os.getcwd() + '/output/' + item['id']
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                return file.readline()
        return None

    def _get_previous_version_from_es(self, item):
        data = es.get(item['id'])
        if not data == None:
            return data['_source']['version']
        else:
            return None

    def _get_previous_version(self, item):
        if settings.ES_ENABLE:
            return self._get_previous_version_from_es(item)
        else:
            return self._get_previous_version_from_file(item)

    def _save_version(self, item, update=False):
        if settings.ES_ENABLE:
            if update:
                es.update(item)
            else:
                es.add(item)
        else:
            file_name = os.getcwd() + '/output/' + item['id']
            self._write_data(file_name, item)

    def _write_data(self, file_name, item):
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    logging.error('Error: ' + os.strerror(exc.errno))
                    raise
        with open(file_name, "w") as f:
            f.write(item['version'])

    def _check_version(self, item):
        previous_ver = self._get_previous_version(item)
        if not previous_ver == None:
            if version.parse(previous_ver) < version.parse(item['version']):
                self._save_version(item, update=True)
                mail.send_mail(item)
            else:
                logging.info('No Update found, skipping...')
        else:
            self._save_version(item)
            if settings.SEND_MAIL:
                mail.send_mail(item)

    def process_item(self, item, spider):
        logging.debug(item)
        self._check_version(item)
        return item
