from multiprocessing import Process,Array,Lock
from threading import Thread
from socket import *
import image_tool_v6 as im
import cv2
import time
import re
import numpy as np
import pickle

# Strip arguments from command
def parsecommand(command):
	seperator_1=command.find('/')
	seperator_2=command.find('/',seperator_1+1)
	arg1=command[seperator_1+1:seperator_2]
	seperator_1=seperator_2
	seperator_2=command.find('/',seperator_1+1)
	arg2=command[seperator_1+1:seperator_2]
	seperator_1=seperator_2
	seperator_2=command.find('/',seperator_1+1)
	arg3=command[seperator_1+1:seperator_2]
	return arg1,arg2,arg3


class Server(Thread):

	def __init__(self, sock,  lock, timeout=30):
		self.lock = lock
		self.sock = sock
		self.timeout=timeout
		Thread.__init__(self)

	def run(self):

		# Initializations
		start = time.time()
		request = self.sock.recv(1024)
		self.image=im.LabeledImage()
		self.ug=im.UserGroup.getInstance()
		
		# Authentication
		login=request.decode()
		self.userName=login[:login.find(':')]
		self.pw=login[login.find(':')+1:]
		if(self.userName=='admin'):
			self.sock.send(b'Logged in with administrator privilages.')
			print('An admin is connected.')
		else:
			ug = im.UserGroup.getInstance()
			exp='ug.checkUser(("'+login.replace(':','","')+'"))'
			print(exp)
			if(eval(exp)):
				self.sock.send(b'Login succesful.')
				print(self.userName,"is now connected.")
			else:
				self.sock.send(b'Wrong login.')
				print("A login is denied!")
				return

		#Fulfilling user requests
		request=self.sock.recv(1024)
		while request != b'' and time.time()-start<=self.timeout:
			ret_val=b''
			print("request:",request.decode())
			command = request.decode()
			func=command[:command.find('/')]
			
			# Parse and evaluate requests

			if(func=='getImage'):
				exp='self.image.'+func+'(("'+self.userName+'","'+self.pw+'"))'
				print(exp,"is called")
				ret_val=eval(exp)
				if(type(ret_val)==type("") ):#only when it returns error
					ret_val=b'error'
				else:
					ret_val_dump=pickle.dumps(ret_val)
					print("length:",len(ret_val_dump))
					self.sock.send(str(len(ret_val_dump)).encode())
					time.sleep(0.3)
					ret_val=ret_val_dump

			elif(func=='imageList'):
				exp='self.image.'+func+'()'
				print(exp,"is called")
				ret_val=eval(exp)
				if(type(ret_val)==type("") ):#only when it returns error
					ret_val=b'error'
				else:
					ret_val=pickle.dumps(ret_val)
					print(len(ret_val))
					self.sock.send(str(len(ret_val)).encode())
					time.sleep(0.1)

			elif(func=='loadImage'):
				arg=command[command.find('/')+1:-1]
				exp='self.image.'+func+'("'+arg+'","'+self.userName+'")'
				print(exp,"is called")
				ret_val=(eval(exp)).encode()

			elif(func=='setImage'):
				seperator_1=command.find('/')+1
				seperator_2=command.find('/',seperator_1)
				size=command[seperator_1:seperator_2]
				self.sock.send(b'ready')
				arg1=self.sock.recv(int(size)+1024)
				ret_val=(self.image.setImage(pickle.loads(arg1),self.userName)).encode()

			elif(func=='load'):
				arg=command[command.find('/')+1:-1]
				exp='self.image.'+func+'("'+arg+'")'
				print(exp,"is called")
				ret_val=(eval(exp)).encode()
				
			elif(func=='save'):
				if(self.userName!=self.image.owner):
					ret_val=b'You are not privilaged to use '+func.encode()+b' on this image.'
				else:
					arg=command[command.find('/')+1:-1]
					exp='self.image.'+func+'("'+arg+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='setDefault'):
				if(self.userName!=self.image.owner):
					ret_val=b'You are not privilaged to use '+func.encode()+b' on this image.'
				else:
					arg=command[command.find('/')+1:-1]
					exp='self.image.'+func+'("'+arg+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='addRule'):
				if(self.userName!=self.image.owner):
					ret_val=b'You are not privilaged to use '+func.encode()+b' on this image.'
				else:
					arg1,arg2,arg3=parsecommand(command)
					exp='self.image.'+func+'("'+arg1+'",'+arg2+',"'+arg3+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='delRule'):
				if(self.userName!=self.image.owner):
					ret_val=b'You are not privilaged to use '+func.encode()+b' on this image.'
				else:
					arg=command[command.find('/')+1:-1]
					exp='self.image.'+func+'('+arg+')'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='addUser'):
				if(self.userName!='admin'):
					ret_val=b'You are not privilaged to use '+func.encode()+b'.'
				else:
					arg1,arg2,arg3=parsecommand(command)
					exp='self.ug.'+func+'("'+arg1+'",'+arg2+',"'+arg3+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='addGroup'):
				if(self.userName!='admin'):
					ret_val=b'You are not privilaged to use '+func.encode()+b'.'
				else:
					arg=command[command.find('/')+1:-1]
					exp='self.ug.'+func+'("'+arg+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='delUser'):
				if(self.userName!='admin'):
					ret_val=b'You are not privilaged to use '+func.encode()+b'.'
				else:
					arg=command[command.find('/')+1:-1]
					exp='self.ug.'+func+'("'+arg+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='delGroup'):
				if(self.userName!='admin'):
					ret_val=b'You are not privilaged to use '+func.encode()+b'.'
				else:
					arg=command[command.find('/')+1:-1]
					exp='self.ug.'+func+'("'+arg+'")'
					print(exp,"is called")
					ret_val=(eval(exp)).encode()

			elif(func=='getGroups'):
				arg=command[command.find('/')+1:-1]
				exp='self.ug.'+func+'("'+arg+'")'
				print(exp,"is called")
				print(eval(exp))
				ret_val=pickle.dumps(eval(exp))
				self.sock.send(str(len(ret_val)).encode())
				time.sleep(0.1)

			elif(func=='getUsers'):
				arg=command[command.find('/')+1:-1]
				exp='self.ug.'+func+'("'+arg+'")'
				print(exp,"is called")
				print(eval(exp))
				ret_val=pickle.dumps(eval(exp))
				self.sock.send(str(len(ret_val)).encode())
				time.sleep(0.1)

			elif(func=='setPasswords'):
				seperator_1=command.find('/')+1
				seperator_2=command.find('/',seperator_1)
				arg2=command[seperator_1:seperator_2]
				seperator_1=seperator_2+1
				seperator_2=command.find('/',seperator_1)
				arg3=command[seperator_1:seperator_2]
				exp='self.ug.'+func+'(("'+self.userName+'","'+arg2+'"),"'+arg3+'")'
				print(exp,"is called")
				ret_val=str(eval(exp)).encode()

			elif(func=='isMember'):
				seperator_1=command.find('/')+1
				seperator_2=command.find('/',seperator_1)
				arg1=command[seperator_1:seperator_2]
				seperator_1=seperator_2+1
				seperator_2=command.find('/',seperator_1)
				arg2=command[seperator_1:seperator_2]
				exp='self.ug.'+func+'("'+arg1+'","'+arg2+'")'
				print(exp,"is called")
				ret_val=str(eval(exp)).encode()

			elif(func=='commit'):
				db=im.Database.getInstance()
				db.commit()
				print("Commit successful.")
				ret_val=b'Updated database.'

			else:
				ret_val=b'Incorrect command! '+command.encode()
			
			# Error handling
			if(ret_val!=b''):
				self.sock.send(ret_val)
			else:
				self.sock.send(b'ERROR!') 
			# Receive next request
			request = self.sock.recv(2048)

		# Time out connection after given period
		if(time.time()-start>self.timeout):
			print(self.userName+"'s connection timed out!")
			self.sock.send(b'connection timed out!')

		# Commit changes to database when disconnecting
		db=im.Database.getInstance()
		db.commit()#???????????
		print(self.userName, "is disconnected.")


# Function for starting servers that instantiates
# one server thread per each clients connected
def startserver(host, port, clients=1):
	sock = socket(AF_INET, SOCK_STREAM)
	print("Server initiated on host:",host," and port:",port)
	sock.bind( (host, port))
	sock.listen(15)
	lck = Lock()
	av = sock.accept()
	client_count=0
	threads=[]

	# Listen if accepted by socked and client limit not reached
	while av and client_count<clients:
		
		# Accept a client and start a thread for the client
		print('accepted: ', av[1],'client no:',client_count)
		client_count+=1
		s = Server(av[0], lck, 10000)
		threads.append(s)
		s.start()
		
		# Check for client limit
		if(client_count>=clients):
			continue
		
		# Listen for next client
		av = sock.accept()
	
	# Wait for termination of server threads
	print("Client limit reached.\nWaiting for clients to disconnect...")
	for thread in threads:
		thread.join()
	print('Managed all',str(clients)+'.','\nServer is closing in 15 seconds...')

if __name__ == '__main__':
	import sys
	print(sys.argv)
	
	# Initialize databases
	db = im.Database.getInstance()
	ug = im.UserGroup.getInstance()

	startserver('0.0.0.0', int(sys.argv[1]), int(sys.argv[2]))

	# Wait some time before closing database to prevent data loss
	time.sleep(15)
	db.closeDatabase()
