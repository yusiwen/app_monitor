import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from airium import Airium

from app_monitor import settings


def _gen_mail(item):
    # Create the container (outer) email message.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = item['name'] + ' Update Found'
    text = "{name}\n{version}\n{date}\n{notes}\n{download_url}".format(
        **item)

    a = Airium()
    # Generating HTML file
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(item['name'] + ' Update Found')
        with a.body():
            with a.p():
                a(item['name'])
            with a.p():
                a(item['category'])
            with a.p():
                a(item['version'])
            with a.p():
                a(item['date'])
            with a.p():
                a(item['notes'])
            urls = item['download_url']
            if isinstance(urls, str):
                with a.p():
                    with a.a(href=urls):
                        a(urls)
            elif isinstance(urls, list):
                for x in urls:
                    with a.p():
                        with a.a(href=x):
                            a(x)

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(str(a), 'html'))
    return msg


def send_mail(item):
    logging.info('Send mail.....')

    message = _gen_mail(item)
    message['From'] = 'Software Updater <' + settings.SMTP_SENDER + '>'
    message['To'] = settings.SMTP_RECEIVER

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(settings.SMTP_USERNAME,
                     settings.SMTP_PASSWORD)
        logging.debug('Mail server logged in')
        server.sendmail(settings.SMTP_SENDER,
                        settings.SMTP_RECEIVER, message.as_string())
        server.quit()
    logging.info('Mail sent')
