from common.models import DownloadServer, Beatmap, Download
from crawler.main import BeatmapCrawler
from settings import SERVERS, OSU_ACCOUNT


class BeatmapDaemon:
    def __init__(self):
        self.crawler = BeatmapCrawler(OSU_ACCOUNT['username'], OSU_ACCOUNT['password'])
        handlers = []
        for SERVER in SERVERS:
            handler_class = SERVER['handler']
            handler = handler_class(DownloadServer.objects.get(pk=SERVER['server_id']), SERVER['config'])
            handler.init()
            handlers.append(handler)
        self.handlers = tuple(handlers)

    def ensure_beatmap(self, beatmap_id):
        try:
            beatmap = Beatmap.objects.get(pk=beatmap_id)
        except Beatmap.DoesNotExist:
            beatmap = self.crawler.crawl_single(beatmap_id)
            beatmap.upload()
        return beatmap

    def check_all(self):
        for handler in self.handlers:
            downloads = handler.check_all()
            for download in downloads:
                beatmap = self.ensure_beatmap(download.beatmap_id)
                try:
                    Download.objects.get(server_id=handler.server.id, beatmap_id=beatmap.id)
                except Download.DoesNotExist:
                    download.upload()

    def download_single(self, beatmap_id):
        self.crawler.ensure_login()
        self.crawler.crawl_single(beatmap_id).save()
        p = self.crawler.download_beatmap(beatmap_id)
        for handler in self.handlers:
            handler.upload(p[0], p[1]).save()