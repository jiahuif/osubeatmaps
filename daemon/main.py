import logging
import os
import shutil
import tempfile
from threading import Thread
import time
import django.db

from redis import StrictRedis

from common.models import DownloadServer, Beatmap, Download
from crawler.main import BeatmapCrawler
from settings import SERVERS, OSU_ACCOUNT, FETCH_QUEUE_KEY, DOWNLOAD_SLEEP_TIME


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
        self.redis = None
        self.logger = logging.getLogger('osubeatmaps.daemon')
        """:type : logging.RootLogger """

    def ensure_beatmap(self, beatmap_id):
        try:
            beatmap = Beatmap.objects.get(pk=beatmap_id)
        except Beatmap.DoesNotExist:
            beatmap = self.crawler.crawl_single(beatmap_id)
            beatmap.save()
        return beatmap

    def check_all(self):
        for handler in self.handlers:
            downloads = handler.check_all()
            for download in downloads:
                beatmap = self.ensure_beatmap(download.beatmap_id)
                try:
                    Download.objects.get(server_id=handler.server.id, beatmap_id=beatmap.id)
                except Download.DoesNotExist:
                    download.save()

    def process_single(self, beatmap_id):
        """

        :param beatmap_id:
        :return: timestamp of finishing downloading
        """
        self.crawler.ensure_login()
        self.crawler.crawl_single(beatmap_id).save()
        p = self.crawler.download_beatmap(beatmap_id)
        tmp = tempfile.mkstemp()
        os.close(tmp[0])
        tmp_filename = tmp[1]
        tmp_file = open(tmp_filename, 'wb')
        shutil.copyfileobj(p[1], tmp_file)
        tmp_file.close()
        p[1].close()
        # record the finishing time.
        ret = time.time()
        threads = []
        """:type : list of Thread """
        # invoke each handler
        for handler in self.handlers:
            def handle():
                _tmp_file = open(tmp_filename, 'rb')
                handler.upload(p[0], _tmp_file).save()
                _tmp_file.close()

            thread = Thread(None, handle)
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        # remove downloaded file
        os.unlink(tmp_filename)
        # return the timestamp indicating download finishing time.
        return ret

    # noinspection PyBroadException
    def run_daemon(self):
        self.logger.info("Starting beatmap daemon.")
        self.redis = StrictRedis()
        while True:
            try:
                beatmap_id = int(self.redis.blpop(FETCH_QUEUE_KEY)[1])
                self.logger.info('Now processing beatmap #%d.', beatmap_id)
                try:
                    django.db.close_old_connections()
                    stamp = self.process_single(beatmap_id)
                    self.logger.info('Finished processing beatmap #%d.', beatmap_id)
                    delta_time = time.time() - stamp
                    if delta_time < DOWNLOAD_SLEEP_TIME:
                        time.sleep(DOWNLOAD_SLEEP_TIME - delta_time)
                except Exception as e:
                    self.logger.exception("An exception raised while processing beatmap #%d. Aborting.", beatmap_id)

            except KeyboardInterrupt:
                self.logger.info("stopping beatmap daemon.")
                quit()
            except Exception as e:
                self.logger.exception("An exception raised while processing crawling queue.")
                self.logger.critical("Error whiling processing crawling queue.")