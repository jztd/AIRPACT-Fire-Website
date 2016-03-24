from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import AirpactUser
from django.template import RequestContext
from forms import UserCreationForm
from django.contrib.auth import get_user_model
import json
import random
import string

@login_required
def user_profile(request):
	if(request.method == 'POST'):
		form = UserProfileForm(request.POST, instance=request.user.profile)

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)

	# # For now, do not ask for the email
	# #email = request.POST['email']

	# print("\n ! !  This is the post information from login:")
	# print(request.POST)
	# print("\n ! !  This is the password:")
	# print(password)


		if user is not None:
		   auth.login(request, user)
		   return HttpResponseRedirect('/user/loggedin')
		else:
			return HttpResponseRedirect('/user/invalid')
	return HttpResponse("DONT GO HERE")
	
def loggedin(request):
	return render_to_response('loggedin.html')

def invalid_login(request):
	return render_to_response('invalid.html')


# Register/ Create a new user
def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/user/register_success')
		else:
			return render_to_response('register.html',  {'form':form}, context_instance=RequestContext(request) )

	form = UserCreationForm()
	return render_to_response('register.html',  {'form':form}, context_instance=RequestContext(request) )


def register_success(request): 
	return render_to_response('register_success.html', {'message': "successfull registration! "}, context_instance=RequestContext(request))

def user_app_auth(request):
	if request.method == 'POST':
		userdata = json.loads(request.body)
		user = auth.authenticate(username=userdata['username'], password=userdata['password'] )
		response_data = {}
		if user is not None:
			#generate secret key
			secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(22))
			response_data['isUser'] = 'true'
			response_data['secretKey'] = secret
		else:
			respones_data['isUser'] = 'false'
			respones_data['secretKey'] = ''
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse("HI")