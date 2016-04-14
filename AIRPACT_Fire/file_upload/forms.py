from django import forms
from file_upload.models import picture

class picture_upload_form(forms.Form):
	pic = forms.FileField(label="select picture")
