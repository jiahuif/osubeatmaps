from django.contrib.sitemaps import Sitemap

from django.core.urlresolvers import reverse
from django.utils.translation import activate

from common.models import Beatmap, Genre, Language

from osubeatmaps.settings import LANGUAGES


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        views = ['index', 'disclaimer']
        return [[language[0], view] for language in LANGUAGES for view in views]

    def location(self, obj):
        activate(obj[0])
        return reverse('website:' + obj[1])


class BeatmapSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        beatmap_data_set = [[beatmap.id, beatmap.date_ranked] for beatmap in Beatmap.objects.all()]
        return [[language[0], beatmap_data] for language in LANGUAGES for beatmap_data in beatmap_data_set]

    def location(self, obj):
        activate(obj[0])
        return reverse('website:item', args=[obj[1][0]])

    def lastmod(self, obj):
        return obj[1][1]


class ListingSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.6

    def items(self):
        genre_ids = set([0] + [genre.id for genre in Genre.objects.all()])
        lang_ids = set([0] + [language.id for language in Language.objects.all()])
        return [
            [language[0], genre_id, language_id]
            for language in LANGUAGES
            for genre_id in genre_ids
            for language_id in lang_ids
        ]

    def location(self, obj):
        activate(obj[0])
        return reverse('website:listing', args=[obj[1], obj[2], 1])