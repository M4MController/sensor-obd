# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from gpiozero import Buzzer
from time import sleep
import requests

logger = logging.getLogger(__name__)

session = None


def init_sensor(uri, sensor_uuid):
    return 200 <= requests.post(
        '{uri}/private/sensor/{sensor_uuid}/register'.format(uri=uri, sensor_uuid=sensor_uuid),
        json={'sensor_type': 5, 'status': 1},
    ).status_code < 300


def json_send(uri, sensor_uuid, data):
    return requests.post(
        '{uri}/private/sensor/{sensor_uuid}/data'.format(uri=uri, sensor_uuid=sensor_uuid),
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
