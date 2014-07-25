from django.conf.urls import patterns, url

from website import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^(?P<beatmap_id>\d+)/$', views.item, name='item'),
                       url(r'^detail/(?P<beatmap_id>\d+)/$', views.detail, name='detail'),
                       url(r'^download/(?P<beatmap_id>\d+)/$', views.download, name='download'),
                       url(r'^user/(?P<username>.+)/$', views.user, name='user'),
                       url(r'^listing/(?P<genre_id>\d+)/(?P<language_id>\d+)/(?P<page_id>\d+)/$', views.listing,
                           name='listing'),
                       url(r'^disclaimer/$', views.DisclaimerView.as_view(), name='disclaimer'),
)