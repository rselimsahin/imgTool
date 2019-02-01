import image_tool_v6 as im
import cv2

# Tester for image_tool_v6 for self testing purposes


"""
Database = im.Database.getInstance()
UserGroups = im.UserGroup.getInstance()

img3=im.LabeledImage()
img4=im.LabeledImage()
img3.loadImage("test.jpg","admin")
img4.loadImage("test.png","admin")
print("img3 initiated and test image loaded ")
print("Images table before save:")
Database.printTable("Images")
img3.save("test1")
img4.save("test2")
print("img3 saved to database as test1")
print("img4 saved to database as test2")
print("Images table after save:")
Database.printTable("Images")
img4.imageList()
"""


"""
UserGroups.addGroup("Under7")
UserGroups.addGroup("Under13")
UserGroups.addGroup("Under18")
UserGroups.addGroup("General")


UserGroups.addUser("Tom",["Under7","Under13","Under18","General"],"12345")
UserGroups.addUser("Sam",["Under13","Under18","General"],"12356")
UserGroups.addUser("John",["Under13","General"],"12378")
UserGroups.addUser("Obama",["Under13","Under18","General"],"Illimunati")
UserGroups.addUser("Trump",["Under7"],"makeAmericaGreatAgain")
UserGroups.addUser("Sally",["General"],"12390")
UserGroups.addUser("Hitler",["Under7"],"Waffen-SS")



UserGroups.printGroups()
print("Under7")
print(UserGroups.getUsers("Under7"))
print("Under13")
print(UserGroups.getUsers("Under13"))
print("Under18")
print(UserGroups.getUsers("Under18"))
print("General")
print(UserGroups.getUsers("General"))
UserGroups.printUsers()
inp = input("\nDelete Sam")

UserGroups.delUser("Sam")


UserGroups.printGroups()
print("Under7")
print(UserGroups.getUsers("Under7"))
print("Under13")
print(UserGroups.getUsers("Under13"))
print("Under18")
print(UserGroups.getUsers("Under18"))
print("General")
print(UserGroups.getUsers("General"))
UserGroups.printUsers()

inp = input("\nDelete Jimmy")
UserGroups.delUser("Jimmy")


UserGroups.printGroups()
UserGroups.printUsers()

inp = input("\nDelete Under7 and Under15")
UserGroups.delGroup("Under7")
UserGroups.delGroup("Under15")


UserGroups.printGroups()
print("Under7")
print(UserGroups.getUsers("Under7"))
print("Under13")
print(UserGroups.getUsers("Under13"))
print("Under18")
print(UserGroups.getUsers("Under18"))
print("General")
print(UserGroups.getUsers("General"))
UserGroups.printUsers()


inp = input("\nGetGroups Test")
print(UserGroups.getGroups("Tom"))
print(UserGroups.getGroups("Sam"))
print(UserGroups.getGroups("Mehmet"))


print(UserGroups.getUsers("General"))
print(UserGroups.getUsers("Under7"))
inp = input("\nSetPassword Test")

UserGroups.setPasswords(("Tom","12345"),"asdqwe")
UserGroups.setPasswords(("Sally","12390"),"newpasswd")
UserGroups.setPasswords(("John","11223"),"notchanged")

UserGroups.printUsers()
inp = input("\nIsMember Test")

print(UserGroups.isMember("Sally","Under7"))
print(UserGroups.isMember("Arthur","Under18"))
print(UserGroups.isMember("Tom","Under18"))

print()


inp = input("\nImage tool tester.")


#setimage test
print("--Testing setImage function--")
img1=im.LabeledImage()
print("img1 initiated as a LabeledImage")
print("getImage when image not loaded")
img1.getImage("admin")
test=cv2.imread("test.jpg")
buff=cv2.imencode('.jpg',test)[1]
print("test.jpg readed and encoded as", buff.tostring()[:20]+b"...")
print("loading image with setImage(buff) and calling getImage")
img1.setImage(buff,"admin")
img1.getImage("admin")

print()

#loadimage test
print("--Testing loadImage function--")
img2=im.LabeledImage()
print("img2 initiated as a LabeledImage")
print("getImage when image not loaded")
img2.getImage("admin")
print("loading image with loadImage(location) and calling getImage")
img2.loadImage("test.jpg","admin")
img2.getImage("admin")

print()

#save-load test
print("--Testing save and load functions--")
img3=im.LabeledImage()
img3.loadImage("test.jpg","admin")
print("img3 initiated and test image loaded ")
print("Images table before save:")
Database.printTable("Images")
img3.save("test")
print("img3 saved to database as test")
#Database.insertImage('test',im2)
#Database.deleteImage('test')
print("Images table after save:")
Database.printTable("Images")
img4=im.LabeledImage()
print("img4 initiated as a LabeledImage ")
print("getImage when image not loaded")
img4.getImage("admin")
print("loading image with load function and calling getImage")
img4.load("test")
img4.getImage("admin")

print()

# setDefault-getImage-Rule test 
ug1 = im.UserGroup.getInstance()
ug1.addUser("Elijah",["Under18"],"asd")
#ug1.setPasswords(("Elijah","111"),"asd")
print("--Testing defaultAction--")
img5=im.LabeledImage()
img5.loadImage("test.jpg","admin")
print("img5 initiated and test image loaded ")
print("calling getImage with defaultAction set as default(ALLOW)")
print("getImage as Elijah")
img5.getImage(("Elijah","asd"))
print("adding the rule ('u:Elijah',('RECTANGLE',100,200,300,400),'ALLOW')")
img5.addRule("u:Elijah",("RECTANGLE",100,200,300,400),"ALLOW")
print("adding the rule ('r:^[a-z]lij?',('CIRCLE',300,300,100),'DENY')")
img5.addRule("r:^[A-Z]lij*",("CIRCLE",300,300,100),"DENY")
print("adding the rule ('g:Under18',('CIRCLE',300,300,100),'DENY')")
img5.addRule("g:Under18",("CIRCLE",0,0,30),"DENY")
print(UserGroups.isMember("Elijah","Under18"))
print("getImage as Elijah")
img5.getImage(("Elijah","asd"))
print("changing defaultAction to DENY")
img5.setDefault("DENY")
print("getImage as Elijah")
img5.getImage(("Elijah","asd"))
img5.delRule(1)
print("getImage as Elijah after deleted rule at index 1")
img5.getImage(("Elijah","asd"))

"""





"""imx=im.LabeledImage()
imx.loadImage("img1.jpg")
imx.defaultAction='DENY'
imx.addRule("u:Felicity",("RECTANGLE",100,200,300,400),"ALLOW")
imx.addRule("u:Felicity",("RECTANGLE",10,200,250,300),"DENY")
imx.addRule("u:Felicity",("CIRCLE",500,500,100),"DENY")
imx.addRule("u:Felicity",("CIRCLE",550,550,100),"ALLOW")
imx.getImage(("Felicity","Obama"))"""

"""im2=im.LabeledImage()
im2.loadImage("test.png")
Database.insertImage('test',im2)
#Database.deleteImage('test')
Database.printTable("Images")
im2.print()
im3=im.LabeledImage()
im3.load("test")
im3.print()
Database.updateImage("test3",im3)"""

Database.closeDatabase()
"""
im=cv2.imread("img.jpg")
buff=cv2.imencode('.png',im)[1]
image1=LabeledImage()
image1.setDefault("DENY")
image1.print()
image1.addRule("Ahmet",("RECTANGLE",1,2,2,3),"ALLOW")
image1.print()
image1.delRule(0)
image1.print()
image1.setImage(buff)
#image1.loadImage("flowchart.jpg")
image1.print()
"""


'''
ug=im.UserGroup()
ug.addGroup("group1")
ug.addGroup("group2")
ug.addGroup("group3")
ug.addUser("ali",["group1","group2"],"123")
ug.addUser("mehmet",["group3","group2"],"123")

ug.print()

image2=im.LabeledImage()
image2.loadImage("img.jpg")
image2.setDefault("DENY")
image2.print()
#image2.addRule("u:ali",("CIRCLE",250,250,100),"DENY")
#image2.addRule("u:ali",("CIRCLE",350,350,100),"DENY")
#image2.addRule("g:group2",("RECTANGLE",500,350,300,550),"DENY")
#image2.addRule("g:group2",("RECTANGLE",50,12,300,550),"DENY")
#image2.addRule("r:^[a-z]l?",("CIRCLE",500,500,50),"DENY")
#image2.circ((50,50),50,(0,0,0))
#image2.circ((75,75),50,(0,0,0))
#image2.rect((150,200),(200,250),(0,0,0))
image2.addRule("r:^[a-z]l?",("CIRCLE",500,500,50),"DENY")
image2.getImage(("ali","123"))
image2.print()

'''

"""

def rect(self,point1,point2,color):
		cv2.rectangle(self.image, pt1, pt2,color) 
		#cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)

	def polylines(self,lines,color):
		cv2.polylines(self.image,lines,True,color)
		# cv2.polylines(img,[pts],True,(0,255,255))
"""
"""
image=cv2.imread("flowchart.jpg")
cv2.circle(image, (0,0), 100, (0,0,0), -1)
print("image::")
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('image',image)
key=cv2.waitKey(0)&0xFF
if(key==27):
	cv2.destroyAllWindows()"""

