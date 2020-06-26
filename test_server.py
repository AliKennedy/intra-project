import unittest
import code.server as server

class TestServer(unittest.TestCase):

	def test_port_high(self):
		self.assertLessEqual(server.PORT, 65536) #num of ports on a computer

	def test_port_low(self):
		self.assertGreaterEqual(server.PORT, 1024) #0-1023 are 'system ports'

	def test_dispenser_connected_response_type(self):
		result = server.dispenser_is_connected("abcde")
		self.assertIsInstance(result, bool)

	def test_dispenser_connected(self):
		result = server.dispenser_is_connected("abcde")
		self.assertFalse(result)