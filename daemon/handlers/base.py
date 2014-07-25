from common.models import DownloadServer


class BaseHandler:
    def __init__(self, server, config):
        """
        :param config:
        :type config: dict
        :type server: DownloadServer
        """
        self.server = server
        self.config = config

    def init(self):
        pass

    def close(self):
        pass

    def upload(self, suggested_filename, source):
        """

        :param suggested_filename:
        :param source:
        :type suggested_filename: basestring
        :type source: file
        :rtype: Download
        """
        pass

    def check_all(self):
        """

        :return: list of all existing download
        :rtype: list of Download
        """