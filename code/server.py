import socket
import sys
import time
import threading as th
import select
import json
import mysql.connector

#socket set up
HOST_IP = '0.0.0.0' #any/all ip addresses on this device
PORT = 52871 #predecided arbitrary port number
connected_dispensers = {}

#MySQL connection set up
mydb = mysql.connector.connect(
	host="localhost",
	user="ali",
	password="Computing20*",
	database="intraproject")

mycursor = mydb.cursor()

#returns a boolean if dispenser is connected or not
def dispenser_is_connected(dispenser_id):
	print(connected_dispensers.values())
	for v in connected_dispensers.values():
		if dispenser_id in v.values():
			return True
	return False

#sets up thread and accepts announcement from dispenser with its ID
def start_dispenser_thread(connection, address):
	thread = th.Thread(target=dispenser_thread, args=(connection, address))
	connected_dispensers[connection]['thread'] = thread

	global id_received
	id_received = False

	while not id_received: #while we have not recieved the id
		try:
			data = connection.recv(4096) # recieve 4kb of data at one time
			if not data is None:
				data = data.decode() #byte conversion
				if len(data) == 5:
					dispenser_id = data
					print("Dispenser ID: {}".format(dispenser_id))
					if not dispenser_is_connected(dispenser_id): #check if the dispenser is already connected
						connected_dispensers[connection]['id'] = dispenser_id #add to the dictionary
						print("retrieved dispenser name")
						#store in database
						mycursor.execute("INSERT INTO dispensers (id, username) VALUES (%s, %s)", (dispenser_id, None))
						mydb.commit()

						id_received = True #stop looping
			else:
				pass
		except:
			pass
	thread.start() # start dispenser thread


#handles how each dispenser thread should behave
def dispenser_thread(connection, address):
	connected = True
	low_fluid = "dispenser {}'s fluid is low and needs to be topped up"
	id_string = connected_dispensers[connection]['id']
	sql = "INSERT INTO dispenserdata (id, fluidlevel, uses, alerts, ignored, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	while connected and server_running:
		try:
			data = connection.recv(4096) #receive up to 4kb of data
			if data:
				message = data.decode() #byte to string conversion
				if len(message) == 5: #extra attempts to send id upon connection
					pass
				elif len(message) > 5: #status
					status = json.loads(message)#convert to JSON object
					#send this data to database
					values = (status["id"], status["fluid"], status["uses"], status["alerts"], status["ignored"], status["date"], status["time"])
					mycursor.execute(sql, values)
					mydb.commit()
					if status['fluid percentage'] == 10:
						#alert user (web app or phone app)
						print(low_fluid.format(id_string))
			else: #timeout, unexpected power loss etc
				#alert user which dispenser is no longer active
				print("dispenser {} is offline".format(id_string))
				del connected_dispensers[connection]
				connected = False
		except KeyboardInterrupt:
			connected = False

		except:
			continue
	connection.close()


def setup():
	#server set up
	global server_running
	server_running = True

	global serversocket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 TCP
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	#give the socket an ip address and port
	socket_details = (HOST_IP, PORT)
	serversocket.bind(socket_details)
	serversocket.listen(100)  # max 100 connections (can be adjusted for larger settings)



def accept_connections():
	setup()
	#main loop - loop forever
	while True:
		try:
			print("accepting..")
			connection, address = serversocket.accept() # connection = connection object, address = dispenser ip and port
			connected_dispensers[connection] = { 'address' : address }# add to dictionary of connected dispensers
			#create a new thread for every new connection
			start_dispenser_thread(connection, address)
			print("New connection {}".format(address))
		except KeyboardInterrupt: # (CTRL + C)
			print("Server shutting down...")
			serversocket.close()
			server_running = False #shut down threads
			sys.exit(0)


if __name__ == '__main__':
	accept_connections()
