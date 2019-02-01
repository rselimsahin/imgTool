from django.conf.urls import url
from django.contrib.auth import login
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^msg/(?P<message>.+)/$',views.index, name='index'),
    url(r'^image$', views.image, name='image'),
    url(r'^image/msg/(?P<message>.+)/$',views.image, name='image'),
    url(r'^usergroup$',views.usergroup, name='usergroup'),
    url(r'^usergroup/msg/(?P<message>.+)/$',views.usergroup, name='usergroup'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^loadImage/(?P<owner>.+)/$',views.loadImage, name='loadImage'),
    url(r'^setImage/(?P<owner>.+)/$',views.setImage, name='setImage'),
    url(r'^save/$',views.save, name='save'),
    url(r'^setDefault/$',views.setDefault, name='setDefault'),
    url(r'^addRule/$',views.addRule, name='addRule'),
    url(r'^delRule/$',views.delRule, name='delRule'),
	url(r'^load/$',views.load, name='load'),
	url(r'^getImage/$',views.getImage, name='getImage'),
	url(r'^pwscreen/$',views.pwscreen, name='pwscreen'),
	url(r'^setPasswords/$',views.setPasswords, name='setPasswords'),
    url(r'^getGroups/$',views.getGroups, name='getGroups'),
    url(r'^getUsers/$',views.getUsers, name='getUsers'),
    url(r'^isMember/$',views.isMember, name='isMember'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)