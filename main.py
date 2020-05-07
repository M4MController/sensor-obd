# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import uuid

from random import random

from m4m_utils import *
from m4m_obd import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

polling_delay = int(os.environ.get('TIMEOUT', '1'))
logger.info("Current polling delay time: {}s".format(polling_delay))


def get_obd_con():
    while True:
        obd_con = obd_start()
        if obd_con.is_connected():
            return obd_con


def init(uri, sensor_uuid):
    while not init_sensor(uri, sensor_uuid):
        time.sleep(1)


def main():
    if not os.path.exists('uuid'):
        sensor_uuid = uuid.uuid4().hex
        with open('uuid', 'w+') as f:
            f.write(sensor_uuid)
    else:
        with open('uuid', 'r') as f:
            sensor_uuid = f.readline()


    use_stubs = int(os.environ.get('USE_STUBS', "0"))
    uri = os.environ.get('URI')

    init(uri, sensor_uuid)

    if not use_stubs:
        obd_con = get_obd_con()

    while True:
        if use_stubs:
            data = {'speed': random() * 100}
            for i in range(use_stubs):
                data[str(i)] = random() * 100
            json_send(uri, sensor_uuid, data)
        elif obd_con.is_connected():
            try:
                data = obd_read(obd_con)
                json_send(uri, sensor_uuid, data)
            except Exception as e:
                logger.info("Failed reading data from obd! %s", e)
        else:
            obd_con = get_obd_con()

        time.sleep(polling_delay)


if __name__ == '__main__':
    main()