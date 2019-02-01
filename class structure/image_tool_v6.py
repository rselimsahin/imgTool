import cv2
import numpy as np
import re
import os
import sqlite3
import pickle
import time

# This is a singleton that handles database access
class Database:
	
	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if Database.__instance == None:
			Database()
		return Database.__instance 
	def __init__(self):
		""" Virtually private constructor. """
		if Database.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			try:
				# Create tables
				self.path =  os.getcwd()+"/image_tool_db"
				self.connector = sqlite3.connect(self.path, check_same_thread=False)
				self.cursor = self.connector.cursor()
				self.image ='CREATE TABLE IF NOT EXISTS Images (\
 					name TEXT PRIMARY KEY,\
					 image TEXT NOT NULL,\
					 rules TEXT NOT NULL,\
					 owner TEXT NOT NULL,\
					 defaultAction TEXT NOT NULL)'
				self.cursor.execute(self.image)
				self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
				self.connector.execute("""PRAGMA foreign_keys = ON""")

				self.connector.execute('''CREATE TABLE IF NOT EXISTS Groups
					 (gname     TEXT PRIMARY KEY   NOT NULL);''')

				self.connector.execute('''CREATE TABLE IF NOT EXISTS Users
					 (uname     TEXT PRIMARY KEY   NOT NULL,
					  password TEXT               NOT NULL);''')

				self.connector.execute('''CREATE TABLE IF NOT EXISTS Member\
					 (gname     TEXT               NOT NULL,\
					  uname     TEXT               NOT NULL,\
					  FOREIGN KEY(gname) REFERENCES Groups(gname) \
					  ON DELETE CASCADE\
					  ON UPDATE CASCADE,\
					  FOREIGN KEY(uname) REFERENCES Users(uname)\
					  ON DELETE CASCADE
					  ON UPDATE CASCADE);''')
				print("Database initiated with tables: ",self.cursor.fetchall())
			except OSError :
				print("Database already created.")
			Database.				#self.connector.execute("DROP TABLE IF EXISTS Member")
__instance = self



	# Insert an image to database
	def insertImage(self,name,image,rules,owner,defaultAction):
		try:
			 self.image = pickle.dumps(image)
			 self.rules = pickle.dumps(rules)
			 self.owner = owner
			 self.defaultAction = defaultAction
			 self.sql = """
       				 INSERT INTO Images (name, image, rules, owner, defaultAction)
        			 VALUES (?, ?, ?, ?, ?)"""
			 self.cursor.execute(self.sql,(name,self.image, self.rules, self.owner, self.defaultAction))
			 print("Image: ",name,"succesfully inserted")
		except sqlite3.IntegrityError:
				self.connector.rollback()
				print('ERROR: ID already exists.')
		
	# Load the image with given name from database
	def loadImage(self,name):
		 self.sql = """
			   SELECT image,rules,owner,defaultAction FROM Images 
			   WHERE name = '{0}'
				""".format(name)
		 self.ret = self.cursor.execute(self.sql)
		 self.ans = self.cursor.fetchone()
		 
		 return self.ans

	# Load all images from database
	def loadAll(self):
		self.sql = """
			   SELECT name,owner FROM Images
				"""
		self.ret=self.cursor.execute(self.sql)
		self.ans=self.cursor.fetchall()
		return self.ans

	# Delete the image with given name from database
	def deleteImage(self,imageName):
		 try:
                        self.delete = "DELETE FROM Images where name = '{0}'".format(imageName)
                        self.cursor.execute(self.delete)
                        print(imageName+" is deleted.")
		 except sqlite3.OperationalError:
			 print(imageName+" does not exist.") 
		
	# Update the image with given name
	def updateImage(self,oldImageName,newImage):
		self.update = "UPDATE Images SET image = ? WHERE name = ?"
		self.obj = pickle.dumps(newImage)
		self.cursor.execute(self.update,(self.obj,oldImageName))  
		self.rs = self.cursor.fetchall()
		if(self.cursor.rowcount):
			print(oldImageName+" is succesfully updated.")
		else:
			print("UpdateImage error")

	# Commit the changes and close database
	def closeDatabase(self):
		self.connector.commit()
		self.connector.close()
	
	# Commit the changes
	def commit(self):
		self.connector.commit()

	# Print the requested table
	def printTable(self,name):
		self.sql = """SELECT name FROM '{0}'""".format(name)
		self.cursor.execute(self.sql)

		print(self.cursor.fetchall())



class LabeledImage:

	def __init__(self):
		self.defaultAction='ALLOW'
		self.rules=[]
		self.owner=""
		self.imLoaded=0  #is image loaded on class
	
	# Set an image from a buffer(nparray or byte array)
	def setImage(self, buff, owner):
		self.image=cv2.imdecode(buff,0)
		self.imLoaded=1
		self.owner=owner
		return "Image loaded from buffer."

	# Load an image from file
	def loadImage(self, filepath, owner):
		self.image=cv2.imread(filepath)
		if(!image.data):
			return "Error while loading image."
		self.imLoaded=1
		self.owner=owner
		return "Image loaded from file."
		
	# Load an image from database
	def load(self, name):
		db = Database.getInstance()
		self.imagetext = db.loadImage(name)
		if(self.imagetext == ""):
			print("Error while loading image.")
			return "Error while loading image."
		else:
			self.image = pickle.loads(self.imagetext[0])
			self.rules = pickle.loads(self.imagetext[1])
			self.owner = self.imagetext[2]
			self.defaultAction = self.imagetext[3]
			self.imLoaded=1
			return "Image loaded."

	# Save an image to database
	def save(self, name):
		db = Database.getInstance()
		db.insertImage(name,self.image,self.rules,self.owner,self.defaultAction)
		return "Image saved."

	# Set the default action for image
	def setDefault(self, action):
		self.defaultAction=action
		return 'defaultAction is set as '+action+'.'

	# Add a new rule to image
	def addRule(self, matchexpr, shape, action, pos=-1):
		if(pos==-1):
			self.rules.append((matchexpr,shape,action))
		else:
			self.rules.insert(pos,(matchexpr,shape,action))
		return "Rule is added."

	# Delete a rule from given index
	def delRule(self, pos):
		del self.rules[pos]
		return "Rule is deleted."

	# Print the current version of image to user
	def getImage(self, user):

		# Check if there is an image loaded
		if(self.imLoaded==0):
			print("Error:Image is not loaded")
			return "Error:Image is not loaded"

		# Serve raw image to admin
		if(user=="admin" or user==('admin','admin')):
			self.print("image")
			return self.image
		
		# Check login data
		ug=UserGroup.getInstance()
		if(ug.checkUser(user)==False):
			print("Wrong login!")
			return "Wrong login!"

		# Create mask
		self.mask = np.zeros(self.image.shape, dtype = "uint8")
		if(self.defaultAction=='ALLOW'):
			h = self.image.shape[0]
			w = self.image.shape[1]
			#print (h,w)
			for y in range(0, h):
				for x in range(0, w):
						self.mask[y, x] = 255

		# Apply rules to the image
		for rule in (self.rules):#reversed(self.rules):
			if (rule[0][0]=='u'):
				if(rule[0][2:]==user[0]):
					self.applyRule(rule)
			elif (rule[0][0]=='g'):
				group=rule[0][2:]
				u = UserGroup.getInstance()
				if(u.isMember(user[0],group)):
					self.applyRule(rule)
			elif (rule[0][0]=='r'):
				rexp=rule[0][2:]
				revalidator=re.compile(rexp)
				if(revalidator.match(user[0])):
					self.applyRule(rule)
			else:
				return []

		# Apply mask to the image
		self.maskedImg = cv2.bitwise_and(self.image, self.mask)
		
		return self.maskedImg

	# Helper function for applying rules on getimage function
	def applyRule(self,rule):
		if(rule[2]=='DENY'):
			action='DENY'
		elif(rule[2]=='ALLOW'):
			action='ALLOW'
		elif(rule[2]=='BLUR'):
			action='BLUR'
		else:
			action=defaultAction
		if(action=='DENY'):
			color=(0,0,0)
		elif(action=='ALLOW'):
			color=(255,255,255)
		if(rule[1][0]=='CIRCLE'):
			self.circ((rule[1][1],rule[1][2]),rule[1][3],color)
		elif(rule[1][0]=='RECTANGLE'):
			self.rect((rule[1][1],rule[1][2]),(rule[1][3],rule[1][4]),color)
		elif(rule[1][0]=='POLYLINE'):
			self.polylines(rule[1][1],color)

	# Helper function for drawing
	def circ(self, center, radius, color):
		cv2.circle(self.mask, center, radius, color, -1)
	
	# Helper function for drawing
	def rect(self,point1,point2,color):
		cv2.rectangle(self.mask, point1, point2,color,-1) 
	# Helper function for drawing
	def poly(self,lines,color):
		cv2.poly(self.mask,lines,True,color,-1)

	# Get a list of all images
	def imageList(self):
		db=Database.getInstance()
		allImages=db.loadAll()
		print(allImages)
		return allImages

	# Print the requested image(default prints mask applied)
	def print(self,im="maskedImg"):
		print("defaultAction:", self.defaultAction, "| Rules:", self.rules)
		if(self.imLoaded==1):
			print("image::")
			##cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
			#cv2.imshow('blank',self.blankImage)
			if(im=="image"):
				cv2.imshow('image',self.image)
			#cv2.imshow('vis',self.vis)
			else:
				cv2.imshow('masked',self.maskedImg)
			key=cv2.waitKey(0)&0xFF
			if(key==27):
				cv2.destroyAllWindows()
		else:
			print("Image is not loaded")

class UserGroup():
	"""docstring for UserGroup"""

	__instance = None
	@staticmethod
	def getInstance():
		""" Static access method. """
		if UserGroup.__instance == None:
			UserGroup()
			print("UserGroup initiated.")
		return UserGroup.__instance 

	def __init__(self):
		""" Virtually private constructor. """
		if UserGroup.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			self.Database_ = Database.getInstance()
			self.conn = self.Database_.connector
			UserGroup.__instance = self

	# Add a user to database(subscribed groups must be specified)
	def addUser(self, uname, groups, password):
		try:
			self.conn.execute("""INSERT INTO Users (uname,password) VALUES (?,?)"""\
						,(uname,password))
			for gname in groups:
				self.conn.execute('''INSERT INTO Member (gname,uname)\
								VALUES (?,?)''',(gname,uname))
			print("user:",uname," is added." )
			#self.conn.commit()
			return "user:"+uname+" is added." 
		except sqlite3.IntegrityError:
			print("Integrity Error! Group does not exist or user: "+uname+" is already added.")
			return "Integrity Error! Group does not exist or user: "+uname+" is already added."

	# Add a group to database
	def addGroup(self, gname):
		try:
			self.conn.execute('''INSERT INTO Groups (gname)\
							VALUES (?)''',(gname,))
			print("group:",gname," is added.")
			return "group:"+gname+" is added."
		except sqlite3.IntegrityError:
			print("group: "+gname+" is already added.")
			return "group: "+gname+" is already added."

	# Delete user with given name from database
	def delUser(self, uname):
		c=self.conn.execute("""SELECT uname FROM Users WHERE Users.uname=?""",(uname,))
		if(len(c.fetchall())==0):
			return uname+ ' does not exist.'
		else:
			self.conn.execute("""DELETE FROM Users WHERE Users.uname=?""",(uname,))
			return uname+' is deleted.'

	# Delete group with given name from database
	def delGroup(self, gname):
		c=self.conn.execute("""SELECT gname FROM Groups WHERE Groups.gname=?""",(gname,))
		if(len(c.fetchall())==0):
			return gname+ ' does not exist.'
		else:
			self.conn.execute("""DELETE FROM Groups WHERE Groups.gname=?""",(gname,))
			return gname+' is deleted.'

	# Get groups subscribed by given user
	def getGroups(self, uname):
		c=self.conn.execute("""SELECT gname FROM Member WHERE Member.uname=?""",(uname,))
		return(c.fetchall())

	# Get users in given group
	def getUsers(self, gname):
		c=self.conn.execute("""SELECT uname FROM Member WHERE Member.gname=?""",(gname,))
		return(c.fetchall())

	# Change passwords of users
	def setPasswords(self, user, password):
		cu=self.conn.execute("""SELECT password FROM Users WHERE uname=?""",(user[0],))
		for row in cu:
			old_pw=row[0]
		if(old_pw==user[1]):
			cp=self.conn.execute("""UPDATE Users SET password=? WHERE uname=?""",(password,user[0]))
			print(user[0],"'s password is successfully changed.")
			return user[0]+"'s password is successfully changed."
		else:
			print("Wrong password.")
			return "Wrong password."
		
	# Check if the given user is a member of the given group
	def isMember(self, uname, gname):
		cm=self.conn.execute("""SELECT uname FROM Member WHERE uname=? AND gname=?""",(uname,gname))
		return len(cm.fetchall())>0
	
	# Check if given userdata is correct
	def checkUser(self,user):
		cm=self.conn.execute("""SELECT uname FROM Users WHERE uname=? AND password=?""",(user[0],user[1]))
		return len(cm.fetchall())>0

	# Print all groups
	def printGroups(self):
		print("Groups")
		c = self.conn.execute("""SELECT * FROM Groups""")
		print(c.fetchall())

	# Print all users
	def printUsers(self):
		print("Users")
		c = self.conn.execute("""SELECT * FROM Users""")
		print(c.fetchall())




