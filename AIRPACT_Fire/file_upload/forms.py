from django import forms
from file_upload.models import picture

class picture_upload_form(forms.Form):
	pic = forms.FileField(label="select picture")
	vr = forms.DecimalField(label="visual range")
	location = forms.CharField(label='Location', required=True)
	Description = forms.CharField(label='Description', required=True)
	#location = forms.DecimalField(label="location")