from random import randint

from obd import OBDStatus, OBD
from obd.protocols import ISO_15765_4_11bit_500k
from obd.protocols.protocol import Frame, Message, ECU


class ObdStub(OBD):
	def status(self):
		return OBDStatus.CAR_CONNECTED

	@property
	def interface(self):
		if not hasattr(self, '__interface'):
			self.__interface = ELMStub()
		return self.__interface

	@interface.setter
	def interface(self, _):
		pass


class ELMStub:
	def set_protocol(self, protocol_):
		return True

	def manual_protocol(self, protocol_):
		return False

	def auto_protocol(self):
		return True

	def set_baudrate(self, baud):
		return True

	def auto_baudrate(self):
		return False

	def port_name(self):
		return ""

	def status(self):
		return OBDStatus.CAR_CONNECTED

	def ecus(self):
		return True

	def protocol_name(self):
		return ISO_15765_4_11bit_500k

	def protocol_id(self):
		return "8"

	def low_power(self):
		return self.__read()

	def normal_power(self):
		return self.__read()

	def close(self):
		pass

	def send_and_parse(self, cmd):
		return self.__read()

	def __read(self):
		result = []
		for _ in range(1):
			message = Message([Frame("1" * 256)])
			message.ecu = ECU.ALL
			message.data = bytearray([randint(0, 255) for _ in range(6)])
			result.append(message)
		return result
