# -*- coding: utf-8 -*-
import datetime
import errno
import logging
import os

from app_monitor import es
from app_monitor import mail
from app_monitor import settings


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AppMonitorPipeline(object):

    @staticmethod
    def __get_previous_version_from_file(item):
        file_name = os.getcwd() + '/output/' + item['id']
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                return file.readline()
        return None

    @staticmethod
    def __get_previous_version_from_es(item):
        data = es.get(item['id'], item['category'])
        if data is not None:
            return data['_source']['version']
        else:
            return None

    @staticmethod
    def __get_previous_version(item):
        if settings.ES_ENABLE:
            return AppMonitorPipeline.__get_previous_version_from_es(item)
        else:
            return AppMonitorPipeline.__get_previous_version_from_file(item)

    @staticmethod
    def __save_version(item, update=False):
        item['last_check_time'] = str(datetime.datetime.now())
        item['last_check_status'] = 'success'
        if settings.ES_ENABLE:
            if update:
                es.update(item)
            else:
                es.add(item)
        else:
            file_name = os.getcwd() + '/output/' + item['id']
            AppMonitorPipeline.__write_data(file_name, item)

    @staticmethod
    def __write_data(file_name, item):
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    logging.error('Error: ' + os.strerror(exc.errno))
                    raise
        with open(file_name, "w") as f:
            f.write(item['version'])

    @staticmethod
    def __check_version(item):
        previous_ver = AppMonitorPipeline.__get_previous_version(item)
        if previous_ver is not None:
            if previous_ver != item['version']:
                AppMonitorPipeline.__save_version(item, update=True)
                mail.send_mail(item)
            else:
                logging.info('No Update found, skipping...%s', item['name'])
        else:  # if no previous version has been found, then this check is running the first time
            AppMonitorPipeline.__save_version(item)
            if settings.SEND_MAIL:
                mail.send_mail(item)

    @staticmethod
    def process_item(item, spider):
        logging.debug(item)
        AppMonitorPipeline.__check_version(item)
        return item
