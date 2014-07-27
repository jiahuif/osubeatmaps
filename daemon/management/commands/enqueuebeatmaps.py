from django.core.management import BaseCommand

from redis import StrictRedis

from daemon.settings import FETCH_QUEUE_KEY


class Command(BaseCommand):
    args = '<beatmap_id ...>'
    help = 'Enqueue specified beatmaps and schedule them for crawling and downloading.'

    def handle(self, *args, **options):
        redis = StrictRedis()
        for beatmap_id in map(int, args):
            redis.rpush(FETCH_QUEUE_KEY, beatmap_id)
