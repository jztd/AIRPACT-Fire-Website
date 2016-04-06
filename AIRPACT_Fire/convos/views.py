from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
# Standard import things
from django.shortcuts import render
from django.http import HttpResponse
from file_upload.models import picture
from user_profile.models import AuthToken
from user_profile.models import AirpactUser
from file_upload.forms import picture_upload_form
from convos.models import convoPage
from django.contrib.auth.decorators import login_required
# Create your views here.

# render the convo! 
def render_convo(request, convo_id):
	convo = convoPage.objects.get(id=convo_id)
	picture = convo.picture
	return render_to_response(
    'convos.html',
    {'picture': picture, 'convos':convo, 'convo_id':convo_id },
    context_instance=RequestContext(request))	


# Overrides comment posted
def comment_post(request):
	print("I am at comment post, this is request: \n\n")
	print(request.url)
	return HttpResponseRedirect( "/" )
	