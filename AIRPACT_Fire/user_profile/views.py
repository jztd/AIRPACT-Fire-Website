from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from user_profile.models import UserProfile
from forms import UserProfileForm

# Create your views here.
@login_required
def update_profile(request):
	userProfile = UserProfile.object.get(user=request.user)
	form = UserProfileForm(initial={'bio':userProfile.bio})
	return render_to_response('user_profile/update_profile.html', 
		{'form':form}, RequestContext(request))