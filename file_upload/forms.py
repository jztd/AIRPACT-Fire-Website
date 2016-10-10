from django import forms
from file_upload.models import picture
from file_upload.models import tag
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models
from django.contrib.gis import forms

def getChoices():
	T = tag.objects.values('text').distinct()

	x = []
	for g in T:
		for i,k in g.items():
			print(i)
			x.append((k,k))
	return x

class picture_upload_form(forms.Form):
	pic = forms.FileField(label="select picture")
	vr = forms.DecimalField(label="visual range")
	location = forms.CharField(label='Location', required=True)
	description = forms.CharField(label='Description', required=True)
	lowColorX = forms.DecimalField(label="Near Object X Coordinate", widget=forms.HiddenInput())
	lowColorY = forms.DecimalField(label="Near Object Y Coordinate", widget=forms.HiddenInput())
	highColorX = forms.DecimalField(label="far Object X Coordinate", widget=forms.HiddenInput())
	highColorY = forms.DecimalField(label="far Object Y Coordinate", widget=forms.HiddenInput())

	#location = forms.DecimalField(label="location")

# The search form for the gallery
class GallerySortForm(forms.Form):
	vr_choices=[(0, "None"), (1,'0-50'),(2,'50-300'), (3,'300-1000'), (4,'1000-5000'), (5,'5000+')]
	ascending_choices = [(0,"Ascending time"), (1,"Descending time"), 
	(2,"Ascending visual Range"),(3,"Descending visual Range")]

	ascending = forms.ChoiceField(ascending_choices, label = "Order by:", widget = forms.Select())

	visual_range = forms.ChoiceField(choices=vr_choices, label = "Visual Range(in meters):",
		widget= forms.Select(attrs={'id':'vr','name':'Visual Range(in meters)','class':'form-control'}))

	point = forms.PointField(widget=
		forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

	location = forms.CharField(required = False, label = "Location Tag(s):", )

	date = forms.CharField(required=False,widget=forms.TextInput(attrs={'id':'date','name':'date',
		'class':'form-control'}))


