from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns


urlpatterns = patterns('',
)

urlpatterns += i18n_patterns('',
                             url(r'^', include('website.urls', namespace="website")),
)
