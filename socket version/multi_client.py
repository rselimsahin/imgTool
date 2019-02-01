from multiprocessing import Process, Lock, RLock, Queue, Value, Array
from threading import Thread
import random
import time
from socket import *
import numpy as np
import pickle
import cv2

# Functions provided for testing multithreading environment

# Beware that this script is written for self testing purposes
# and only for a specific version of the server and may 
# not work with current version you have!

# Given functions will act as multiple clients with different
# behaviors and interact with the server


def client(port,lck,n=-1):
    # send n random request
    # the connection is kept alive until client closes it.
    test=cv2.imread("test.jpg")
    buff=cv2.imencode('.jpg',test)[1]
    mess_image = [ 'setImage/'+str(len(buff))+'/ahmet/', 'loadImage/test.png/', 'getImage/', 'setDefault/DENY/', 'addRule/u:ahmet/("RECTANGLE",100,200,300,400)/ALLOW/)',\
             'addRule/u:ahmet/("RECTANGLE",100,200,300,400)/DENY/)','delRule/1/', 'getImage/', 'save/test/', 'load/test/']
    mess_group=['addGroup/Under18/','addUser/mehmet/["Under18"]/mehmehmeh/', 'getGroups/mehmet/'\
         ,'setPasswords/123asd/newpassword/', 'getUsers/Under18/', 'isMember/mehmet/Under18/', 'delGroup/Under18/']

    mess=mess_image
    if(n==-1):
        n=len(mess)
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('0.0.0.0', port))
    c.send(b'ahmet:123asd')
    #c.send(b'admin:admin')
    reply = c.recv(1024)
    if(reply==b'Wrong login.'):
        print("Login denied, closing port...")
        c.close
        return
    else:
        print(reply)
    for i in range(n):
        time.sleep(random.random()*1)
        c.send(mess[i].encode())
        reply = c.recv(1024)
        print(reply)
        if(mess[i]=='getImage/'):
            if(reply.decode()=="error"):
                print('Error: image not loaded!')
            else:    
                reply=int(reply.decode())+1024
                reply=c.recv(reply)
                nparr=pickle.loads(reply)
                print(nparr)
                lck.acquire()
                cv2.imshow('image3'+str(i),nparr)
                key=cv2.waitKey(0)&0xFF
                if(key==27):
                    cv2.destroyWindow('image3'+str(i))
                lck.release()
                reply='image shown.'
        if(mess[i][:mess[i].find('/')]=='setImage'):
            buff=pickle.dumps(buff)
            c.send(buff)
            reply=c.recv(1024)
            print(reply)
        if(mess[i][:mess[i].find('/')]=='getGroups' or mess[i][:mess[i].find('/')]=='getUsers'):
            reply=int(reply.decode())+1024
            reply=c.recv(reply)
            groups=pickle.loads(reply)
            print(mess[i]+' result:',groups)
        print(c.getsockname(), reply)
    time.sleep(1)
    print("closing port")
    c.close()

def mehmet(port,lck,n=-1):
    # send n random request
    # the connection is kept alive until client closes it.
    mess_image = ['load/test/','setDefault/DENY/', 'addRule/u:ahmet/("RECTANGLE",100,200,300,400)/ALLOW/)','getImage/' ]
    mess_group=['addGroup/Under18/','addUser/mehmet/["Under18"]/mehmehmeh/', 'getGroups/mehmet/'\
         , 'delGroup/Under18/']

    mess=mess_image
    if(n==-1):
        n=len(mess)
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('0.0.0.0', port))
    #c.send(b'ahmet:123asd')
    c.send(b'mehmet:123asd')
    reply = c.recv(1024)
    if(reply==b'Wrong login.'):
        print("Login denied, closing port...")
        c.close
        return
    else:
        print(reply)
    for i in range(n):
        time.sleep(random.random()*1)
        c.send(mess[i].encode())
        reply = c.recv(1024)
        print(reply)
        if(mess[i]=='getImage/'):
            if(reply.decode()=="error"):
                print('Error: image not loaded!')
            else:    
                reply=int(reply.decode())+2560
                reply=c.recv(reply)
                nparr=pickle.loads(reply)
                print(nparr)
                lck.acquire()
                cv2.imshow('image1',nparr)
                lck.release()
                key=cv2.waitKey(0)&0xFF
                if(key==27):
                    cv2.destroyWindow('image1')
                reply='image shown.'
        if(mess[i][:mess[i].find('/')]=='getGroups'):
            reply=int(reply.decode())+2560
            reply=c.recv(reply)
            groups=pickle.loads(reply)
            print('groups:',groups)
        print(c.getsockname(), reply)
    time.sleep(1)
    print("closing port")
    c.close()

def admin(port,n=-1):
    # send n random request
    # the connection is kept alive until client closes it.
    #mess = ['img2.getImage("admin")',"img2.addRule('g:Under18',('CIRCLE',0,0,30),'DENY')", 'img2.loadImage("test.jpg")',"img5.addRule('u:Elijah',('RECTANGLE',100,200,300,400),'ALLOW')", 'img2.getImage("admin")']
    mess=['getImage']
    if(n==-1):
        n=len(mess)
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('0.0.0.0', port))
    c.send(b'admin:admin')
    reply = c.recv(1024)
    if(reply==b'Wrong login.'):
        print("Login denied, closing port...")
        c.close
        return
    for i in range(n):
        time.sleep(random.random()*2)
        c.send(random.choice(mess).encode())
        reply = c.recv(1024)
        print('admin:', c.getsockname(), reply)
    time.sleep(1)
    print("closing port")
    c.close()


# create 5 clients
if __name__ == '__main__':
    import sys
    print(sys.argv)
    lck=Lock()
    #clients = [Process(target = client, args=(5, int(sys.argv[1]))) for i in range(5)]
    # start clients
    client_process=Process(target=client,args=(int(sys.argv[1]),lck,))
    admin_process=Process(target=admin,args=(int(sys.argv[1]),10))
    mehmet_process=Process(target=mehmet,args=(int(sys.argv[1]),lck,))
    #admin_process.start()
    client_process.start()
   
    #client_process.join()
    #mehmet_process.start()

    #for cl in clients: cl.start()
