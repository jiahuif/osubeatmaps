from ftplib import FTP

from django.utils.http import urlquote

from common.models import Download
from daemon.handlers.base import BaseHandler


class SimpleFTPHandler(BaseHandler):
    def __init__(self, server, config):
        BaseHandler.__init__(self, server, config)
        self.ftp = None

    def open_connection(self):
        self.ftp = FTP(self.config['host'], self.config['username'], self.config['password'])
        if 'cwd' in self.config:
            self.ftp.cwd(self.config['cwd'])

    def close_connection(self):
        self.ftp.close()
        self.ftp = None

    def init(self):
        self.open_connection()
        self.ftp.close()

    @staticmethod
    def slug_filename_on_unix(filename):
        """

        :param filename:
        :type filename: str
        :rtype: str
        :return:
        """
        return filename.replace('/', ' ')

    def upload(self, suggested_filename, source):
        """

        :param suggested_filename:
        :param source:
        :type suggested_filename: str
        :type source file
        :return:
        :rtype Download
        """
        filename = self.slug_filename_on_unix(suggested_filename)
        beatmap_id = int(filename.split(' ')[0])
        try:
            return Download.objects.get(beatmap_id=beatmap_id, server=self.server)
        except Download.DoesNotExist:
            pass
        self.open_connection()
        self.ftp.storbinary('STOR ' + filename, source)
        self.close_connection()
        download = Download(beatmap_id=beatmap_id, server=self.server, url=self.get_url(filename))
        return download

    def get_url(self, filename):
        """

        :type filename: str
        :rtype: str
        """
        return self.config['url_base'] + urlquote(filename)

    def check_all(self):
        """
        :rtype: list of Download
        :return: list of all Download records
        """
        self.open_connection()
        file_list = self.ftp.nlst()
        self.close_connection()
        ret = []
        for filename in file_list:
            if filename.endswith('.osz'):
                beatmap_id = int(filename.split(' ')[0])
                download = Download(beatmap_id=beatmap_id, server=self.server, url=self.get_url(filename))
                ret.append(download)
        return ret
