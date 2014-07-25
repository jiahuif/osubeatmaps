from django.contrib import admin

from common.models import Genre, Language, Beatmap, DownloadServer, Download

# Register your models here.


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Beatmap)
admin.site.register(DownloadServer)
admin.site.register(Download)
