from django.conf.urls import patterns, include, url
import loginsys
from django.contrib import admin
import settings
from api import *
from tastypie.api import Api
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProfileResource())
v1_api.register(LotResource())
v1_api.register(LikeResource())
v1_api.register(CommentResource())
v1_api.register(RegistrationResource())
v1_api.register(RateResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^lots/get/(?P<lot_id>\d+)/$', 'lots.views.lot'),
    url(r'^lots/addlike/(?P<lot_id>\d+)/$', 'lots.views.addlike'),
    url(r'^lots/addrate/(?P<lot_id>\d+)/$', 'lots.views.addrate'),
    url(r'^lots/addcomment/(?P<lot_id>\d+)/$', 'lots.views.addcomment'),
    url(r'^addmoney/$', 'lots.views.addmoney'),
    url(r'^lots/all/$', 'lots.views.lots'),
    url(r'^mylots/$', 'lots.views.mylots'),
    url(r'^myshopping/$', 'lots.views.myshopping'),
    url(r'^myrates/$', 'lots.views.myrates'),
    url(r'^statistics/$', 'lots.views.statistics'),
    url(r'^add/lot/', 'lots.views.newlot'),
    url(r'^lot/delete/(?P<lot_id>\d+)/$', 'lots.views.delete'),
    url(r'^lot/edit/(?P<lot_id>\d+)/$', 'lots.views.editA'),
    url(r'^lot/register/(?P<lot_id>\d+)/$', 'lots.views.registration_on_lot'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('loginsys.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^', 'lots.views.lots'),
)
