import logging
import os
import typing

from collections import namedtuple

import obd
from obd.OBDResponse import Status, StatusTest, Monitor, MonitorTest

from stubs import ObdStub

logger = logging.getLogger(__name__)

USE_STUBS = int(os.environ.get('USE_STUBS', "0"))

ResponseStub = namedtuple("ResponseStub", ["value"])


def deserialize_value(name, test) -> str:
	if isinstance(test, StatusTest):
		if test.available:
			if test.complete:
				result = True
			else:
				result = False
			return {name: result}
		return {}
	elif isinstance(test, MonitorTest):
		return test.__dict__
	else:
		return {name: test}


def deserialize(cmd, response) -> typing.Optional[typing.Dict[str, str]]:
	value = response.value
	if value is None:
		return None
	name = cmd.name.lower()

	if isinstance(value, Status) or isinstance(value, Monitor):
		result = {}
		for key, test_value in value.__dict__.items():
			if not key or key.startswith('_'):
				continue

			data = deserialize_value(key, test_value)

			for test, test_result_value in data.items():
				if test_result_value is not None:
					result[f"{name}_{test}"] = str(test_result_value)
		return result
	else:
		return {name: str(value)}


class Car:
	def __init__(self, device: str):
		self._device = device
		self._obd_con = None
		while self._obd_con is None or not self._obd_con.is_connected():
			self._obd_con = self._get_obd_connection()

	def _get_obd_connection(self) -> obd.OBD:
		logger.info("Connecting OBD...")
		obd_con = ObdStub(self._device) if USE_STUBS else obd.OBD(self._device)
		if obd_con.is_connected():
			logger.info("OBD connected")
		else:
			logger.info("OBD not connected")

		return obd_con

	def obd_read(self) -> typing.Dict[str, str]:
		data = {}

		for cmd in self._obd_con.supported_commands:
			response = self._obd_con.query(cmd)

			values = deserialize(cmd, response)
			if values is not None:
				data.update(**values)

		logger.info("%d records read: %s", len(data), data)

		return data
