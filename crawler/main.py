import cgi
import pickle
from requests import Session
from datetime import datetime
from requests.cookies import cookiejar_from_dict
from requests.utils import dict_from_cookiejar

from pyquery import PyQuery

from settings import COOKIE_JAR_DUMP_FILE
from website.models import Beatmap, Genre, Language


class LoginFailed(Exception):
    pass


class BeatmapNotFound(Exception):
    pass


class BeatmapNotRanked(Exception):
    pass


class ParseFailed(Exception):
    pass


class BeatmapNotDownloading(Exception):
    pass


class BeatmapCrawler:
    def __init__(self, username=None, password=None):
        self.session = Session()
        self.username = username
        self.password = password

    def start_session(self):
        if self.session is None:
            self.session = Session()
        try:
            with open(COOKIE_JAR_DUMP_FILE, 'rb') as f:
                self.session.cookies = cookiejar_from_dict(pickle.load(f))
        except IOError:
            pass

    def end_session(self):
        try:
            with open(COOKIE_JAR_DUMP_FILE, 'wb') as f:
                pickle.dump(dict_from_cookiejar(self.session.cookies), f)
        except IOError:
            pass

    def check_login(self):
        """
        Check whether we have logged in to the official osu! website
        """
        response = self.session.get("http://osu.ppy.sh/")
        query = PyQuery(response.text)
        dropdown = query(".login-dropdown")
        return dropdown.size() == 0

    def login(self, username=None, password=None):
        username = self.username if username is None else username
        password = self.password if password is None else password
        response = self.session.get("https://osu.ppy.sh/")
        query = PyQuery(response.text)
        form = query(".login-dropdown form")
        fields = form.find('input')
        post_form = {}
        for field in fields:
            if field.name == 'username':
                field.value = username
            elif field.name == 'password':
                field.value = password
            elif field.name == 'autologin':
                field.value = 'on'
            post_form[field.name] = field.value
        post_form.update(
            {
                'username': username,
                'password': password,
                'autologin': 'on',
            }
        )
        self.session.post(form[0].action, post_form)
        if not self.check_login():
            raise LoginFailed

    def ensure_login(self):
        if not self.check_login():
            self.login()


    @staticmethod
    def get_genre(genre_id, caption):
        """

        :rtype : Genre
        """
        try:
            genre = Genre.objects.get(pk=genre_id)
        except Genre.DoesNotExist:
            genre = Genre(id=genre_id, caption=caption)
            genre.save()
        return genre

    @staticmethod
    def get_language(language_id, caption):
        """

        :rtype : Language
        """
        try:
            language = Language.objects.get(pk=language_id)
        except Language.DoesNotExist:
            language = Language(id=language_id, caption=caption)
            language.save()
        return language

    def crawl_single(self, beatmap_id):
        """

        :type beatmap_id int
        :param beatmap_id:
        :return crawled beatmap object
        :rtype Beatmap
        """
        url = "https://osu.ppy.sh/s/%d" % beatmap_id
        response = self.session.get(url)
        if "The beatmap you are looking for was not found!" in response.text:
            raise BeatmapNotFound
        query = PyQuery(response.text)
        table = query("table#songinfo")
        rows = table.find("tr")
        try:
            beatmap = Beatmap()
            beatmap.id = beatmap_id
            if "Ranked" not in rows.eq(6).find("td").eq(0).html():
                raise BeatmapNotRanked  # No "ranked on" field
            beatmap.artist = rows.eq(0).find("a").eq(0).text().strip()
            beatmap.title = rows.eq(1).find("a").eq(0).text().strip()
            beatmap.creator = rows.eq(2).find("a").eq(0).text().strip()
            beatmap.source = rows.eq(3).find("a").eq(0).text().strip()
            link = rows.eq(3).find("a").eq(1)
            beatmap.genre = self.get_genre(int(link.attr('href').split('=')[-1]), link.text().strip())
            link = rows.eq(3).find("a").eq(2)
            beatmap.language = self.get_language(int(link.attr('href').split('=')[-1]), link.text().strip())
            dates = map(lambda s: s.strip(), rows.eq(6).find("td").eq(1).html().split('<br />'))
            beatmap.date_submitted, beatmap.date_ranked = map(lambda s: datetime.strptime(s, '%b %d, %Y').date(), dates)
            post = query(".posttext")
            post.remove('a:first')
            beatmap.description = post.html().strip()
            beatmap.difficulties = ','.join(
                map(lambda element: element.attrib['class'].split()[-1].strip(), query("#tablist .beatmapTab div")))
            return beatmap
        except BeatmapNotRanked as e:
            raise e
        except Exception as e:
            raise ParseFailed(e)

    def download_beatmap(self, beatmap_id):
        """
        :return tuple of suggested filename and file-like object
        :type beatmap_id int
        :rtype tuple
        """
        url = "https://osu.ppy.sh/d/%d?understood=yes" % beatmap_id
        response = self.session.get(url, stream=True)
        if response.headers['Content-Type'] != 'application/download':
            raise BeatmapNotDownloading
        content_disposition = response.headers['Content-Disposition']
        _, options = cgi.parse_header(content_disposition)
        suggested_filename = options['filename']
        return suggested_filename, response.raw

