from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from website.sitemaps import StaticSitemap, BeatmapSitemap, ListingSitemap


urlpatterns = patterns('',
                       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
                           {'sitemaps': {
                               'static': StaticSitemap,
                               'beatmap': BeatmapSitemap,
                               'listing': ListingSitemap,
                           }}, name='django.contrib.sitemaps.views.sitemap')
)

urlpatterns += i18n_patterns('',
                             url(r'^', include('website.urls', namespace="website")),
)
