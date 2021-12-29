import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app_monitor import settings


def _gen_mail(item):
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


def send_mail(item):
    logging.info('Send mail.....')

    message = _gen_mail(item)
    message['From'] = settings.SMTP_SENDER
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
