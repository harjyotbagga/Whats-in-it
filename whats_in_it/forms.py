from django import forms

class UploadURLForm(forms.Form):
    url_field = forms.CharField(max_length=254, required=False)
    
class UploadImageForm(forms.Form):
    image_field = forms.ImageField(required=False)
