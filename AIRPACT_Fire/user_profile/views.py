from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import AirpactUser
from django.template import RequestContext
from forms import UserCreationForm
from django.contrib.auth import get_user_model


@login_required
def user_profile(request):
	if(request.method == 'POST'):
		form = UserProfileForm(request.POST, instance=request.user.profile)

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST['username']
	password = request.POST['password']
	

	# For now, do not ask for the email
	#email = request.POST['email']

	print("\n ! !  This is the post information from login:")
	print(request.POST)
	print("\n ! !  This is the password:")
	print(password)
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/user/loggedin')
	else:
		return HttpResponseRedirect('/user/invalid')

def loggedin(request):
	return render_to_response('loggedin.html')

def invalid_login(request):
	return render_to_response('invalid.html')


# Register/ Create a new user
@login_required(login_url='/accounts/login/')
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