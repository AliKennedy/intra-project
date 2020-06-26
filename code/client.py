import socket
import select
import time
from datetime import datetime
import sys
import json
import requests
import random


#values read/importded from dispenser software
fluid_pc = random.randint(0, 100)
number_of_uses = random.randint(0, 40)
number_of_alerts = number_of_uses + random.randint(0, 10)
num_ignored = number_of_alerts - number_of_uses
#to be optionally changed by end user through app
volume_to_dispense = 5 #dispense 5 ml

PORT = 52872 #predecided arbitrary port number
DISPENSER_ID = input("5 character dispenser ID: ") #for testing
IP = '0.0.0.0' #any/all IP addresses on this device

def get_public_ip():
	return requests.get('https://checkip.amazonaws.com').text.strip()

def connect_to_server(ip=IP, port=PORT, dispenser_id=DISPENSER_ID):

	server_details = (ip, port)
	global server_connection
	#IPv4, TCP
	server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server_connection.connect(server_details)
		announce_to_network()
	except:
		reconnect()

def announce_to_network():
	#announce itself to network
	i = 0
	while i < 5:
		try:#announce itself 5 times in case to be guarenteed server receives message
			server_connection.send(DISPENSER_ID.encode()) #send id in string form
			time.sleep(5) #wait for server to process that it has received the ID
			i += 1
		except: #connection error
			reconnect()

def jsonify(dic):
	return (json.dumps(dic, indent=4)) #returns json string to be sent to server


def send_to_server(status):
	server_connection.sendall(status.encode())


def report_status():

	date = str(datetime.date(datetime.now()))
	time = str(datetime.time(datetime.now()))

	date_time = date + " " + time[:-6]
	status = {'id' : DISPENSER_ID,
		'fluid' : str(fluid_pc),
		'uses' : str(number_of_uses),
		'alerts' : str(number_of_alerts),
		'ignored' : str(num_ignored),
		'date_time' : date_time}
	status = jsonify(status) #convert to JSON string

	try:
		send_to_server(status)
		# send_log_to_server()
		print("sent!")
	except KeyboardInterrupt:
		print("Disconnecting...")
		server_connection.shutdown(2)
		server_connection.close()
		sys.exit(0)
	except: #server down
		print('hi')

def change_fluid_dispensed(ml):
	volume_to_dispense = ml
	#change in dispenser software also

def reconnect(ip=IP, port=PORT):
	connected = False

	while not connected:
		try:
			server_connection.connect((ip, port))
			connected = True
			announce_to_network()
		except OSError: #already connected
			connected = True
			announce_to_network()
		except: #server down or internet down
			pass

def run():
	while True: # main loop
		try:
			t = 60 * 1 #seconds * minutes - Send data every 10 minutes
			while t > 0:
				time.sleep(1)
				t -= 1

			report_status()
			#read in new dispenser values here
		except ConnectionRefusedError: #server is down
			reconnect()
		except OSError:
			reconnect()
		except BrokenPipeError:
			reconnect()
		except KeyboardInterrupt: #(CTRL + C)
			print("Disconnecting...")
			server_connection.shutdown(2)
			server_connection.close()
			sys.exit(0)
		except: #internet is down
			reconnect()

connect_to_server()
time.sleep(2)
run()
