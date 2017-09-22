from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^room/(?P<room_id>.*)/$', views.chat, name='room'),
]