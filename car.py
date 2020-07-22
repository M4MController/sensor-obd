import itertools
import logging
import os
import typing

from collections import namedtuple
from random import random

import obd

logger = logging.getLogger(__name__)

USE_STUBS = int(os.environ.get('USE_STUBS', "0"))

command_table = list(filter(lambda x: x is not None, itertools.chain(*obd.commands.modes)))

ResponseStub = namedtuple("ResponseStub", ["value"])


class ObdStub:
	def __init__(self, _):
		logger.info("Stub created")

	def is_connected(self):
		return True

	def query(self, _) -> ResponseStub:
		return ResponseStub(random() * 100)


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
		for cmd in command_table:
			response = self._obd_con.query(cmd)
			logger.debug("Record '%s' received: %s", cmd.name, response.value)
			if response.value is not None:
				data[cmd.name.lower()] = str(response.value)

		logger.info("%d records read", len(data))

		return data
