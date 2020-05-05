# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from gpiozero import Buzzer
from time import sleep
import requests

logger = logging.getLogger(__name__)

session = None


def json_send(uri, sensor_id, data):
    return requests.post(
        '{uri}/private/sensor/{sensor_id}/data'.format(uri=uri, sensor_id=sensor_id),
        json={'value': data},
    )


def cur_date():
    return datetime.now().replace(tzinfo=timezone.utc).strftime("%b %d %H:%M:%S m4m: ")


def beep():
    buzzer = Buzzer(17)
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)
