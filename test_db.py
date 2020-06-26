import unittest
import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="ali",
	password="Computing20*",
	database="intraproject")

mycursor = mydb.cursor()

class TestDatabase(unittest.TestCase):

	#dispensers table
	def test_table_dispensers_exists(self):
		query = "SELECT * FROM dispensers LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result) , 0) 

	def test_table_dispensers_correct_fields(self):
		query = "SELECT id, user_id FROM dispensers LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result), 0)	

	#users table
	def test_table_users_exists(self):
		query = "SELECT * FROM users LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result) , 0)

	def test_table_users_correct_fields(self):
		query = "SELECT id, username, password, email FROM users LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result), 0)

	#dispenserdata table
	def test_table_dispenserdata_exists(self):
		query = "SELECT  * FROM dispenserdata LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result), 0)

	def test_table_dispenserdata_correct_fields(self):
		query = "SELECT id, fluidlevel, uses, alerts, ignored, date_time FROM dispenserdata LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result) , 0)

	#notifications table
	def test_table_notifications_exists(self):
		query = "SELECT * FROM notifications LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result) , 0)

	def test_table_notifications_correct_fields(self):
		query = "SELECT dispenser_id, type, message, date_time FROM notifications LIMIT 1"
		mycursor.execute(query)
		result = mycursor.fetchall()

		self.assertGreaterEqual(len(result), 0)