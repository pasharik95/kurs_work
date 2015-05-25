from django.conf.urls import patterns, include, url
from kurs import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^login/', 'loginsys.views.login'),
    url(r'^logout/', 'loginsys.views.logout'),
    url(r'^register/', 'loginsys.views.register'),
    url(r'^editprofile/', 'loginsys.views.editprofile'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
