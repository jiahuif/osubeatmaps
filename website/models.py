from django.db import models

# Create your models here.


class Genre(models.Model):
    id = models.IntegerField(verbose_name="Genre ID", primary_key=True)
    caption = models.CharField(max_length=255)

    def __unicode__(self):
        return "%d - %s" % (self.id, self.caption)


class Language(models.Model):
    id = models.IntegerField(verbose_name="Language ID", primary_key=True)
    caption = models.CharField(max_length=255)

    def __unicode__(self):
        return "%d - %s" % (self.id, self.caption)


class Beatmap(models.Model):
    id = models.IntegerField(verbose_name="Beatmap ID", primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre)
    language = models.ForeignKey(Language)
    date_submitted = models.DateField()
    date_ranked = models.DateField()
    description = models.TextField()
    difficulties = models.TextField()

    def __unicode__(self):
        return "%d %s - %s" % (self.id, self.artist, self.title)


class Download(models.Model):
    beatmap = models.ForeignKey(Beatmap)
    server = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return "[%d][%s] %s" % (self.beatmap_id, self.server, self.url)
