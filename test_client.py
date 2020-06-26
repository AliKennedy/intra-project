import re
import unittest
import code.client as client

class TestClient(unittest.TestCase):

	def test_jsonify(self):
		dic = {"id" : "abcde", "fluid" : 78, "uses" : 36, "alerts" : 39, "ignored" : 3}
		result = client.jsonify(dic)
		self.assertIsInstance(result, str)

	def test_get_public_ip(self):
		result = client.get_public_ip()
		pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$") #ip address pattern
		#assert re.match((pattern), result)
		self.assertRegex(result, pattern)

	def test_dispenser_id(self):
		self.assertEqual(len(client.DISPENSER_ID), 5)

	def test_alerts(self):
		self.assertGreaterEqual(client.number_of_alerts, client.number_of_uses)

	def test_ignored(self):
		self.assertEqual((client.number_of_alerts - client.number_of_uses), client.num_ignored)

	def test_port_high(self):
		self.assertLessEqual(client.PORT, 65536) #num of ports on a computer

	def test_port_low(self):
		self.assertGreaterEqual(client.PORT, 1024) #0-1023 are 'system ports'