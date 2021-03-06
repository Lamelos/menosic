from datetime import datetime
import importlib
import os
from music import helpers


def File(f):
    ext = os.path.splitext(f)[1].lower()
    if ext:
        try:
            module = importlib.import_module('music.backend.tags.reader%s' % ext)
            return module.Track(f)
        except ImportError:
            pass


class Track(object):
    filetype = None  # string

    def __init__(self, path):
        self.path = path
        stat = os.stat(path)
        self.mtime = datetime.fromtimestamp(stat.st_mtime)
        self.filesize = stat.st_size

        self.discnumber = None  # int
        self.tracknumber = None  # int
        self.title = None  # string
        self.album = None  # class
        self.artist = None  # class
        self.artists = []  # list classes
        self.genres = []  # list strings
        self.length = None  # int
        self.bitrate = None  # int
        self.musicbrainz_trackid = None  # uuid/string

    @property
    def duration(self):
        return helpers.duration(self.length)


class Album(object):
    def __init__(self):
        self.title = None  # string
        self.date = None  # string
        self.country = None  # string
        self.musicbrainz_albumid = None  # uuid/string
        self.musicbrainz_releasegroupid = None  # uuid/string
        self.artist = None
        self.labels = []  # list strings
        self.albumtypes = []  # list strings
        self.albumstatus = []  # list strings
        self.path = None  # string


class Artist(object):
    def __init__(self):
        self.name = None  # string
        self.sortname = None  # string
        self.musicbrainz_artistid = None  # uuid/string
        self.path = None  # string


# Helper functions

list_to_item = lambda l: None if not l else l[0]
item_to_list = lambda i: [] if not i else str(i).split('\x00')
data = lambda d: None if not d else d.data


def number(string):
    try:
        string = str(int(string))
    except:
        string = str(string)
    try:
        if '/' in string:
            return int(string.split('/')[0])
        else:
            return int(string)
    except:
        return None
