
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^auth', views.auth_view),
    #include('file_upload.urls')
    #more to come...
]