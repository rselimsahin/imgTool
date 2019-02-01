# imgTool
An image annotation tool made in the scope of the course ceng445(METU).

Sometimes, you do want to share or broadcast an image while keeping some areas hidden for some group of people. A typical example is a sattelite image with military areas. Details of  those  areas  should  not  be  shown  to  civilians. When  the  image  is  downloaded  by  a military officer full image should be shown, however another user should get the image with the area censored (in black for example). A similar scenario can be considered for news photography. Some areas of the picture can contain violence that you do not want kids to see.

#### This project includes 4 versions:
1. Class structures
2. Socket version
3. Static version
4. Dynamic version

## 1. Class Structures
This version includes basic classes and command line testing application testing features of library. It is a class library that provides CRUD and annotation operations for images. Images has multiple security labels on targeted areas. Each label has a target group or individual who has allowed/restricted access to the labeled area. Areas can be rectangular, eliptic or polyline.

## 2. Socket Version
A server application  creating instances of class library and lets client connect and interact with them. Respects concurrency of the shared instances. 

## 3. Static Version

A django based web application that allows editing of labels through HTML forms. Can be realized as a HTLM form based wrapper for "Class Structures" 

## 4. Dynamic Version

A dynamic web application that allows interactive editing of labels with JavaScript, AJAX, JQuerry to enhance user experience. It includes HTML5 features like canvas. 
