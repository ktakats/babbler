from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/logout/', views.log_out, name='logout'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^room/(?P<room_id>.*)/$', views.chat, name='room'),
    url(r'^new_room/', views.new_room, name='new_room'),
    url(r'^find_friends/', views.find_friends, name='find_friends')
]