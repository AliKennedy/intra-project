import socket
import sys
import time
import threading as th
import select
import json
import mysql.connector
import datetime as datetime

#socket set up
HOST_IP = '0.0.0.0' #any/all ip addresses on this device
PORT = 52872 #predecided arbitrary port number
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
						mycursor.execute(("DELETE FROM notifications WHERE dispenser_id = '{}' AND type = 'offline'").format(dispenser_id),)
						mydb.commit()
						#store in database
						try: #fails if dispenser has already been registered on the system before
							#this is because dispenser_id is set as a UNIQUE field in MySQL database
							mycursor.execute("INSERT INTO dispensers (id, user_id) VALUES (%s, %s)", (dispenser_id, None))
							mydb.commit()
						except:
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
	sql = "INSERT INTO dispenserdata (id, fluidlevel, uses, alerts, ignored, date_time) VALUES (%s, %s, %s, %s, %s, %s)"
	while connected and server_running:
		try:
			data = connection.recv(4096) #receive up to 4kb of data
			if data:
				message = data.decode() #byte to string conversion
				if len(message) == 5: #extra attempts to send id upon connection
					pass
				elif len(message) > 5: #status
					print(message)
					status = json.loads(message)#convert to JSON object
					#send this data to database
					print(status["date_time"])
					values = (status["id"], status["fluid"], status["uses"], status["alerts"], status["ignored"], status["date_time"])
					mycursor.execute(sql, values)
					mydb.commit()
					if int(status["fluid"]) <= 10: #low fluid
						#alert user (add notification to database)
						sql = "INSERT INTO notifications (dispenser_id, type, message) VALUES (%s, %s, %s)"
						values = (status["id"], "low_fluid", "{} has low fluid".format(status["id"]))
						mycursor.execute(sql, values)
						mydb.commit()
					elif int(status["fluid"]) > 10:
						#check if it has recently been topped up
						sql = "SELECT * FROM notifications (dispenser_id, type) WHERE dispenser_id = '{}' AND type = 'low_fluid'".format(status["id"])
						mycursor.execute(sql,)
						result = mycursor.fetchone()
						if len(result) > 0:
							#remove low_fluid notification from table
							sql = "DELETE FROM notifications WHERE dispenser_id = '{}' and type = 'low_fluid'".format(status["id"])
							mycursor.execute(sql, )
							mydb.commit()

			else: #timeout, unexpected power loss etc
				#alert user which dispenser is no longer active
				print("dispenser {} is offline".format(id_string))
				del connected_dispensers[connection]
				sql = "INSERT INTO notifications (dispenser_id, type, message) VALUES (%s, %s, %s)"
				values = (status["id"], "offline", "{} has gone offline".format(id_string))
				mycursor.execute(sql,values)
				mydb.commit()
				connected = False
				break
		except KeyboardInterrupt:
			connected = False
			break

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
