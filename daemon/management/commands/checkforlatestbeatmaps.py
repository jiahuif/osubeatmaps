from django.core.management import BaseCommand
from redis import StrictRedis

from daemon.settings import FETCH_QUEUE_KEY

from common.models import Beatmap
from daemon.main import BeatmapDaemon


class Command(BaseCommand):
    help = "Scan the official site and enqueue new beatmaps. "

    def handle(self, *args, **options):
        daemon = BeatmapDaemon()
        daemon.crawler.start_session()
        page = 0
        flag = True
        redis = StrictRedis()
        while flag:
            flag = False
            page += 1
            url = "https://osu.ppy.sh/p/beatmaplist&s=4&r=0&page=%d" % page
            beatmap_ids = set(daemon.crawler.parse_listing_page(daemon.crawler.session.get(url).text))
            for beatmap in Beatmap.objects.filter(id__in=beatmap_ids).all():
                beatmap_ids.remove(beatmap.id)
            for beatmap_id in beatmap_ids:
                if redis.lrem(FETCH_QUEUE_KEY, 0, beatmap_id) == 0L:
                    flag = True
                redis.lpush(FETCH_QUEUE_KEY, beatmap_id)
                self.stderr.write('Enqueued #%d.' % beatmap_id)