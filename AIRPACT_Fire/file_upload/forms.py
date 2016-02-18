from django import forms

class picture_upload_form(forms.Form):
	pic = forms.FileField(label="select picture")
