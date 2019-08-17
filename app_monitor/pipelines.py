# -*- coding: utf-8 -*-
import smtplib, ssl
import os, errno
import logging
import configparser
import app_monitor.settings

from packaging import version

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
class AppMonitorPipeline(object):
    def _send_mail(self, item):
        logging.info('Send mail.....')
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(app_monitor.settings.MAIL_CONFIG_FILE))

        smtp_server = config['mail']['smtp_server']
        smtp_port = config['mail']['smtp_port']
        username = config['mail']['smtp_username']
        password = config['mail']['smtp_password']
        sender_email = config['mail']['sender']
        receiver_email = config['mail']['receiver']
        message = "Subject: {name} Update Found\n\nNew version: {version}".format(**item)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, message)
        logging.info('Mail sent')

    def _write_data(self, filename, item):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
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
            self._send_mail(item)
        self._write_data(filename, item)

    def process_item(self, item, spider):
        logging.debug("current directory is: " + os.getcwd())
        logging.debug(item)
        self._check_version(item)
        return item
