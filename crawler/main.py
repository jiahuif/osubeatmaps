from requests import Session
from datetime import datetime

from pyquery import PyQuery

from website.models import Beatmap, Genre, Language


class LoginFailed(Exception):
    pass


class BeatmapNotFound(Exception):
    pass


class BeatmapNotRanked(Exception):
    pass


class ParseFailed(Exception):
    pass


def check_login(session):
    """
    Check whether we have logged in to the official osu! website
    @type session Session
    """
    response = session.get("http://osu.ppy.sh/")
    query = PyQuery(response.text)
    dropdown = query(".login-dropdown")
    return dropdown.size() == 0


def login(session, username, password):
    """
    @type session Session
    """
    response = session.get("https://osu.ppy.sh/")
    query = PyQuery(response.text)
    form = query(".login-dropdown form")
    fields = form.find('input')
    post_form = {}
    for field in fields:
        if field.name == 'username':
            field.value = username
        elif field.name == 'password':
            field.value = password
        post_form[field.name] = field.value
    session.post(form[0].action, post_form)
    if not check_login(session):
        raise LoginFailed


def get_genre(genre_id, caption):
    try:
        genre = Genre.objects.get(pk=genre_id)
    except Genre.DoesNotExist:
        genre = Genre(id=genre_id, caption=caption)
        genre.save()
    return genre


def get_language(language_id, caption):
    try:
        language = Language.objects.get(pk=language_id)
    except Language.DoesNotExist:
        language = Language(id=language_id, caption=caption)
        language.save()
    return language


def crawl_single(session, beatmap_id):
    """

    :param session:
    :type beatmap_id int
    :param beatmap_id:
    :return:
    """
    url = "https://osu.ppy.sh/s/%d" % beatmap_id
    response = session.get(url)
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
        beatmap.genre = get_genre(int(link.attr('href').split('=')[-1]), link.text().strip())
        link = rows.eq(3).find("a").eq(2)
        beatmap.language = get_language(int(link.attr('href').split('=')[-1]), link.text().strip())
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
