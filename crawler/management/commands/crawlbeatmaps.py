from django.core.management import BaseCommand, CommandError

from crawler.main import BeatmapCrawler, BeatmapNotRanked


class Command(BaseCommand):
    args = '<beatmap_id ...>'
    help = 'Crawls the information of the specified beatmaps without downloading them.'

    def handle(self, *args, **options):
        crawler = BeatmapCrawler()

        for beatmap_id in map(int, args):
            try:
                beatmap = crawler.crawl_single(beatmap_id)
                beatmap.save()
                self.stderr.write("Saved: %s" % beatmap)
            except BeatmapNotRanked:
                raise CommandError('Beatmap #%d was not ranked.' % beatmap_id)

