from django.db import models
import json
# Create your models here.

# Image model which holds image path
class Image(models.Model):
    # Fields
    name=models.CharField(max_length=30, primary_key=True)
    rules=models.CharField(max_length=1000000, blank=True, default='[]')#TODO length
    owner=models.CharField(max_length=30)
    defaultAction=models.CharField(max_length=30, blank=True,default="ALLOW")
    imagex=models.ImageField(upload_to='labeled_images/', blank=True)
    
    def __str__(self):
	    return ' '.join([str(self.name),str(self.rules),str(self.owner),str(self.defaultAction)])
    
    # Get function for transferring rules to array
    def getRules(self):
        if(self.rules):
            return json.loads(self.rules)
        else:
            return []#not necessary
    
    # Set function for transferring rules to json
    def setRules(self,rules):
        self.rules=json.dumps(rules)
        