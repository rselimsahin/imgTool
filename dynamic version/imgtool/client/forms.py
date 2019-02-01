from django import forms

# Upload file form for images in load image function
class UploadFileForm(forms.Form):
    file = forms.ImageField()