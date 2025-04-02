import logging

import requests

from app_monitor import settings


def send_notification(item):
    try:
        if not hasattr(settings, 'PUSH_TOKEN') or not settings.PUSH_TOKEN:
            raise ValueError("PUSH_TOKEN is not defined or empty in settings.")

        resp = requests.post(
            f"{settings.PUSH_URL}/message?token={settings.PUSH_TOKEN}",
            json={
                "message": f"Latest version: {item["version"]}",
                "priority": 2,
                "title": f"[{str(item["category"]).upper()}] {item["name"]} Update Found"
            },
            timeout=10  # 设置超时时间，避免无限等待
        )

        if resp.status_code == 200:
            logging.info(f"Notification sent successfully: {resp.status_code}")
        else:
            logging.error(f"Failed to send notification: {resp.status_code}, {resp.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while sending notification: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
