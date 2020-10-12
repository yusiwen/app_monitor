# -*- coding: utf-8 -*-
import smtplib
import ssl
import os
import errno
import logging
import configparser
import app_monitor.settings

from packaging import version
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AppMonitorPipeline(object):
    def _gen_mail(self, item):
        # Create the container (outer) email message.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = item['name'] + ' Update Found'
        text = "{name}\n{version}\n{date}\n{notes}\n{download_url}".format(
            **item)
        html = """<html><head></head><body>\
                <p>{name}</p>
                <p>{version}</p>
                <p>{date}</p>
                <p>{notes}</p>""".format(**item)
        urls = item['download_url']
        dwn_str = ''
        if isinstance(urls, str):
            dwn_str = "<p><a href='{}'>{}</a></p>".format(
                urls, urls)
        elif isinstance(urls, list):
            for x in urls:
                dwn_str += "<p><a href='{}'>{}</a></p>".format(
                    x, x)
        else:
            dwn_str = ''

        html += dwn_str + '</body></html>'

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        return msg

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
        message = self._gen_mail(item)
        message['From'] = sender_email
        message['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(username, password)
            logging.debug('Mail server logged in')
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
        logging.info('Mail sent')

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
            self._send_mail(item)
        self._write_data(filename, item)

    def process_item(self, item, spider):
        logging.debug("current directory is: " + os.getcwd())
        logging.debug(item)
        self._check_version(item)
        return item
