from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from time import time
from base64 import b64decode
from django.core.files.base import ContentFile


from django.shortcuts import render
from django.http import HttpResponse

from file_upload.models import picture
from file_upload.forms import picture_upload_form

def index(request):
	#if there is a file to upload
	if request.method == 'POST':
		form = picture_upload_form(request.POST, request.FILES)
		if form.is_valid():
			newPic = picture(pic = request.FILES['pic'])
			newPic.save()
			return HttpResponseRedirect(reverse('file_upload.views.index'))
	else:
		form = picture_upload_form()

		pictures = picture.objects.all()
		return render_to_response(
        'index.html',
        {'pics': pictures, 'form': form},
        context_instance=RequestContext(request)
    )

# used specifically for the android app to send data to this webserver
@csrf_exempt

def upload(request):
	if request.method == 'POST':
		s = json.loads(request.body);
		image_data = b64decode(s['image'])

		newPic = picture(pic = ContentFile(image_data,str(time()+".jpg")), description = s['description'], user=s['user']);
		newPic.save()
		return HttpResponse("Success")
	else:
		return HttpResponse("HELLO")
