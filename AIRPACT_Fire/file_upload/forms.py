from django import forms
from file_upload.models import picture
from file_upload.models import tag
sort_box = (('-','none'),('asc','Ascending'),('desc', 'decending'))
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
	#location = forms.DecimalField(label="location")

class GallerySortForm(forms.Form):
	uploaded = forms.ChoiceField(choices=sort_box, widget= forms.Select(attrs={'id':'uploaded', 'name':'uploaded', 'class':'form-control'}))
	vr = forms.ChoiceField(choices=sort_box, widget= forms.Select(attrs={'id':'vr','name':'vr','class':'form-control'}))
	# location = forms.ChoiceField(choices = getChoices(), widget= forms.Select(attrs={'id':'tags','name':'tags','class':'form-control'}))
	date = forms.CharField(required=False,widget=forms.TextInput(attrs={'id':'date','name':'date','class':'form-control'}))


