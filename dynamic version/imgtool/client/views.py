from django.shortcuts import render,redirect
from django.template import Template, Context
import datetime
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from client.models import Image
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from client.forms import UploadFileForm
from django.contrib.auth.models import User, Group
import cv2
import os
import re
import numpy as np
from django.core.files import File

#TODO add rule simplification

# Create your views here.

# Signing up handling
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# Initialize current image
current_image=Image()


# Function for index page rendering
@login_required
def index(request,message=None):
    global current_image
    current_image=None
    if(message):
        message=message.replace('_',' ')
    ulist=list(User.objects.all())
    glist=list(Group.objects.all())
    imagelist = Image.objects.all().order_by('name')
    context = {'ulist':ulist, 'glist': glist, 'message': message, 'imagelist':imagelist, 'username': request.user.username, 'button' : 'Add'}
    return render(request, "clientview.html", context)


# Function for usergroup page rendering
@login_required
def usergroup(request,message=None):
    if(message):
        message=message.replace('_',' ')
    ulist=list(User.objects.all())
    glist=list(Group.objects.all())
    context = {'ulist':ulist, 'glist': glist,  'username': request.user.username, 'button' : 'Add'}
    return render(request, "usergroup.html", context)


# Function for image page rendering
@login_required
def image(request,message=None):
    global current_image
    
    # Parse message
    if(message):
        message=message.replace('_',' ')
    
    # If an image is captured create new image object and update related fields
    if(message=="image served"):
        imagelist = Image.objects.all().order_by('name')
        c = {'message': message, 'form' : UploadFileForm(), 'imagelist': imagelist, 'username': request.user.username}
        if(not(current_image.imagex)):
            return render(request, "image.html", c)
        dir=os.getcwd()
        im_path=dir+"/media/"+current_image.imagex.name[:-4]
        im_p=current_image.imagex.name[:-4]
        im_ext=current_image.imagex.name[-4:]
        Image(name="ruled_image").imagex.save(current_image.imagex.name[15:],File(open(im_path+"_ruled"+im_ext, 'rb')))
        ruled_image=Image.objects.get(name="ruled_image")
        Image.objects.get(name="ruled_image").delete()
        if(ruled_image and ruled_image.imagex):
            c['current_image']= ruled_image
        return render(request, "image.html", c)
    
    # If requesting user is admin serve raw image
    elif(message=='raw image served to admin'):
        imagelist = Image.objects.all().order_by('name')
        c = {'message': message, 'form' : UploadFileForm(), 'imagelist': imagelist, 'username': request.user.username}
        if(current_image and current_image.imagex):
            c['current_image']= current_image
        return render(request, "image.html", c)
    
    # Else keep current image
    else:
        imagelist = Image.objects.all().order_by('name')
        c = {'message': message, 'form' : UploadFileForm(), 'imagelist': imagelist, 'username': request.user.username}
        if(current_image and current_image.imagex):
            c['current_image']= current_image
        return render(request, "image.html", c)


# Load an image from database
def load(request):
    global current_image
    try:
        if request.method=='POST':
            im_name=(request.POST['image'])
            current_image=Image.objects.get(name=im_name)
            print(current_image.imagex)
            return JsonResponse(str(current_image.imagex), safe=False)
        else:
            return redirect('/client/image/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/') # redirect to home page


# Save an image to database
def save(request):
    global current_image
    try:
        if request.method=='POST':
            name=request.POST['name']
            Image(name=name, rules=current_image.rules, owner=current_image.owner,defaultAction=current_image.defaultAction, imagex=current_image.imagex).save()
            return HttpResponse("")
        else:
            return redirect('/client/image/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/') # redirect to home page


# Load an image from location
def loadImage(request,owner):
    global current_image
    try:
        if request.method=='POST':
            form = UploadFileForm(request.POST, request.FILES)
            # If form exists parse form data
            if form.is_valid():
                m = Image(name='currentLoadedImage')
                m.imagex = form.cleaned_data['file']
                m.save()
                current_image=Image.objects.get(name="currentLoadedImage")
                current_image.owner=request.user.username
                Image.objects.get(name="currentLoadedImage").delete()
                print(current_image.imagex)
                return JsonResponse(str(current_image.imagex),safe=False)
        else:
            return redirect('client/image/msg/Invalid_request/')
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/')
    return redirect('/client/image')


# Set an image from buffer
def setImage(request,owner):
    global current_image
    try:
        if request.POST['submit'] == "SetImage":
            buff=request.POST['buffer']
            image=cv2.imdecode(buff,0)
            dir=os.getcwd()
            im_path=dir+"/media/labeled_images/"
            cv2.imwrite(im_path+"buffered.png",image,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])
            current_image.imagex.save("buffered_image.png",File(open(im_path+"buffered.png", 'rb')))
            current_image.owner=request.user.username
            return redirect('/client/image/msg/Image_set_from_buffer')
        else:
            return redirect('client/image/msg/Invalid_request/')
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/')
    return redirect('/client/image')


# Set the default action for image
def setDefault(request):
    global current_image
    try:
        if request.method=='POST':
            # If user is not owner reject
            if(not(request.user.username==current_image.owner or request.user.username=="admin")):
                return JsonResponse("You Are Not Privileged!", safe=False)
            action=request.POST['action']
            current_image.defaultAction=action
            return HttpResponse("")
        else:
            return redirect('/client/image/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/') # redirect to home page


# Add a new rule to image
def addRule(request):
    global current_image
    try:
        if request.method=='POST':
            # If user is not owner reject
            if(not(request.user.username==current_image.owner or request.user.username=="admin")):
                return JsonResponse("You Are Not Privileged!", safe=False)
            rule=request.POST['rule']
            pos=request.POST['pos']
            rules=current_image.getRules()
            if(int(pos)==-1):
                rules.append(eval(rule))
            else:
                rules.insert(int(pos),eval(rule))
            current_image.setRules(rules)
            return JsonResponse(rules, safe=False)
        else:
            return redirect('/client/image/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/') # redirect to home page


# Delete a rule from given index
def delRule(request):#
    global current_image
    try:
        if request.method=='POST':
            # If user is not owner reject
            if(not(request.user.username==current_image.owner or request.user.username=="admin")):
                return JsonResponse("You Are Not Privileged!", safe=False)
            pos=request.POST['pos']
            rules=current_image.getRules()
            del rules[int(pos)]
            current_image.setRules(rules)
            return JsonResponse(rules, safe=False)
        else:
            return redirect('/client/image/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/') # redirect to home page


# Check if requesting user is in the given group
def memberCheck(request,uname,gname):
    l = request.user.groups.values_list('name',flat=True)
    return gname in l


# Get the current image
def getImage(request):
    global current_image
    try:
        if request.method=='POST':
            if(current_image and current_image.imagex):
                dir=os.getcwd()
                image=cv2.imread(dir+"/media/"+current_image.imagex.name)
                
                # If admin is request user return raw image
                if(request.user.username=='admin'):
                    return JsonResponse(str(current_image.imagex), safe=False)
                
                global mask
                # If setdefault is blur create a blurred image
                if(current_image.defaultAction=='BLUR'):
                    image=cv2.blur(image,(7,7))
               
                # Initialize mask as nparray with all zeros
                mask = np.zeros(image.shape, dtype = "uint8")

                # Create mask depending on default action
                if(current_image.defaultAction=='ALLOW' or current_image.defaultAction=='BLUR'):
                    h = image.shape[0]
                    w = image.shape[1]
                    for y in range(0, h):
                        for x in range(0, w):
                                mask[y, x] = 255

                # Draw the rules on the mask
                rules=current_image.getRules()
                for rule in (rules):
                    if (rule[0][0]=='u'):
                        if(rule[0][2:]==request.user.username):
                            applyRule(rule)
                    elif (rule[0][0]=='g'):
                        gname=rule[0][2:]
                        if(memberCheck(request,request.user.username,gname)):
                            applyRule(rule)
                    elif (rule[0][0]=='r'):
                        rexp=rule[0][2:]
                        revalidator=re.compile(rexp)
                        if(revalidator.match(user[0])):
                            applyRule(rule)
                    else:
                        return redirect('/client/image/msg/?/')

                # Apply mask to the image
                maskedImg = cv2.bitwise_and(image, mask)

                # Handle file operations
                im_path=dir+"/media/"+current_image.imagex.name[:-4]
                im_ext=current_image.imagex.name[-4:]
                cv2.imwrite(im_path+"_ruled"+im_ext,maskedImg)
                imagelist = Image.objects.all().order_by('name')
                if(not(current_image.imagex)):
                    return HttpResponse("")

                # Create new image object
                dir=os.getcwd()
                im_path=dir+"/media/"+current_image.imagex.name[:-4]
                im_p=current_image.imagex.name[:-4]
                im_ext=current_image.imagex.name[-4:]
                Image(name="ruled_image").imagex.save(current_image.imagex.name[15:],File(open(im_path+"_ruled"+im_ext, 'rb')))
                
                # Handle file operations
                ruled_image=Image.objects.get(name="ruled_image")
                Image.objects.get(name="ruled_image").delete()

                if(ruled_image and ruled_image.imagex):
                    return JsonResponse(str(ruled_image.imagex),safe=False)
                else:
                    return JsonResponse(str(current_image.imagex),safe=False)
            else:
                return JsonResponse("Image Not Loaded!", safe=False)
        else:
            return redirect('/client/image/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/image/msg/Key_error/') # redirect to home page
    return redirect('/client')


# Helper function for applying rules on getimage function
def applyRule(rule):
    global current_image
    if(rule[2]=='DENY'):
        action='DENY'
    elif(rule[2]=='ALLOW'):
        action='ALLOW'
    elif(rule[2]=='BLUR'):
        action='BLUR'
    else:
        action=current_image.defaultAction
    if(action=='DENY'):
        color=(0,0,0)
    elif(action=='ALLOW'):
        color=(255,255,255)
    if(rule[1][0]=='CIRCLE'):
        circ((rule[1][1],rule[1][2]),rule[1][3],color)
    elif(rule[1][0]=='RECTANGLE'):
        rect((rule[1][1],rule[1][2]),(rule[1][3],rule[1][4]),color)
    elif(rule[1][0]=='POLYLINE'):
        polylines(rule[1][1],color)


# Helper function for drawing
def circ(center, radius, color):
    global mask
    cv2.circle(mask, center, radius, color, -1)

# Helper function for drawing
def rect(point1,point2,color):
    global mask
    cv2.rectangle(mask, point1, point2,color,-1) 

# Helper function for drawing
def poly(lines,color):
    global mask
    cv2.poly(mask,lines,True,color,-1)


# Render password change screen
def pwscreen(request):
    return render(request,"setpasswords.html")


# Reset passwords of users
def setPasswords(request):
    try:
        if request.POST['submit'] == 'SetPassword': # form submitted, process it
            new_pw=request.POST['password']
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(new_pw)
            u.save()
            return redirect('/client/msg/Password_changed/') # redirect to home page
        else:
            return redirect('/client/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/msg/Key_error/') # redirect to home page


# Get the groups user is in
def getGroups(request):
    try:
        if request.method=='POST':
            user_name=request.POST['username']    
            ulist=list(User.objects.all())
            glist=list(Group.objects.all())
            ugroups=list(User.objects.get(username=user_name).groups.all())
            groupnames=""
            for group in ugroups:
                groupnames+=" "+group.name
            return JsonResponse(groupnames, safe=False)
        else:
            return redirect('/client/usergroup/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/usergroup/msg/Key_error/') # redirect to home page


# Get the users group contains
def getUsers(request):
    try:
        if request.method=='POST':
            group_name=request.POST['groupname']    
            ulist=list(User.objects.all())
            glist=list(Group.objects.all())
            gusers=list(User.objects.filter(groups__name=group_name))
            usernames=""
            for user in gusers:
                usernames+=" "+user.username
            return JsonResponse(usernames, safe=False)
        else:
            return redirect('/client/usergroup/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/usergroup/msg/Key_error/') # redirect to home page


# Check if the given user is member of given group
def isMember(request):
    try:
        if request.method=='POST':
            group_name=request.POST['groupname']    
            user_name=request.POST['username']  
            ulist=list(User.objects.all())
            glist=list(Group.objects.all())
            for group in User.objects.get(username=user_name).groups.all():
                if(group.name==group_name):
                    return JsonResponse(str(True), safe=False)
            return JsonResponse(str(False), safe=False)
        else:
            return redirect('/client/usergroup/msg/Invalid_request/') # redirect to home page
    except KeyError:    # form not submitted yet, show it
        return redirect('/client/usergroup/msg/Key_error/') # redirect to home page



