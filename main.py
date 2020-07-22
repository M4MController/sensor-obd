import os
import sys
import time

from car import Car
from hardware import generate_uuid
from m4m_utils import *

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

polling_delay = int(os.environ.get('TIMEOUT', '1'))
logger.info("Current polling delay time: {}s".format(polling_delay))


def init(uri, sensor_uuid):
	while not init_sensor(uri, sensor_uuid):
		time.sleep(1)


def main():
	sensor_uuid = generate_uuid()

	device = os.environ.get('DEVICE', None)
	uri = os.environ.get('URI', None)

	if uri:
		init(uri, sensor_uuid)

	car = Car(device)

	while True:
		try:
			data = car.obd_read()
			if data and uri:
				json_send(uri, sensor_uuid, data)
		except Exception as e:
			logger.info("Failed reading data from obd! %s", e)

		time.sleep(polling_delay)


if __name__ == '__main__':
	main()
