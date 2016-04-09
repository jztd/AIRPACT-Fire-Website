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
from user_profile.models import AuthToken
from user_profile.models import AirpactUser
from user_profile.views import edit_profile
from convos.models import convoPage
from file_upload.forms import picture_upload_form
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	#if there is a file to upload

	if request.method == 'POST':
	
		form = picture_upload_form(request.POST, request.FILES)
		if form.is_valid():
			newPic = picture(pic = request.FILES['pic'], user=request.user)
			newPic.save()

			#Creating some conversation stuffs
			conversations = convoPage(picture = newPic)
			conversations.save()

			#At some point I hsould delete these... maybe 
			print("This is the picture: ")
			print(newPic.id)
			print("This is the conversation: ")
			print(conversations.id)			

			return HttpResponseRedirect(reverse('file_upload.views.index'))
	else:
		form = picture_upload_form()

		pictures = picture.objects.all()
		conversations = convoPage.objects.all()

		return render_to_response(
        'index.html',
        {'pics': pictures, 'form': form, 'conversations':conversations},
        context_instance=RequestContext(request)
    )

# used specifically for the android app to send data to this webserver
@csrf_exempt
def upload(request):
	if request.method == 'POST':
		response_data = {}
		s = json.loads(request.body);
		toke = AuthToken.objects.filter(token=s['secretKey'])
		if toke.count() > 0:
			AuthToken.objects.get(token=s['secretKey']).delete()
			image_data = b64decode(s['image'])
			userob = AirpactUser.objects.get(username=s['user'])
			newPic = picture(pic = ContentFile(image_data,str(str(time())+".jpg")), description = s['description'], user=userob);
			newPic.save()

			#Creating some conversation stuffs
			conversations = convoPage(picture = newPic)
			conversations.save()
			response_data['status'] = 'success'
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			response_data['status'] = 'keyFailed'
			return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse("For app uploads only")

@login_required
def delete_picture(request, id):
	img = picture.objects.get(id = id)
	print("users id: "+str(request.user.id)+"pictureid:"+str(img.id))
	if request.user.id == img.user.id:
		print("deleteing shit")
		img.delete()
	return edit_profile(request)

def test(request):
	userob = AirpactUser.objects.get(username='JZTD')
	print(userob.id)
	return HttpResponse(userob.id)