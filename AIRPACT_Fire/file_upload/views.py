from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


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

# Create your views here.
