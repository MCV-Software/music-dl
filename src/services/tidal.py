# -*- coding: utf-8 -*-
""" Tidal service support for MusicDL.
this service allows users to choose between 3 different qualities. Low, high and lossless.
Lossless quality is only available to the account of tidal capable of playing such kind of audio files.
for low and high qualities, the file is transcoded to mp3 because Tidal gives us that as m4a.
"""
import logging
import webbrowser
import wx
import tidalapi
import config
from update.utils import seconds_to_string
from .import base

log = logging.getLogger("services.tidal")

class interface(base.baseInterface):
    name = "tidal"
    if config.app != None: # Workaround for cx_freeze 6.2 in python 3.7.
        enabled = config.app["services"]["tidal"].get("enabled")
        # This should not be enabled if credentials are not set in config.
        if config.app["services"]["tidal"]["username"] == "" or config.app["services"]["tidal"]["password"] == "":
            enabled = False
    else:
        enabled = False

    def __init__(self):
        super(interface, self).__init__()
        self.setup()

    def setup(self):
        # Assign quality or switch to high if not specified/not found.
        if hasattr(tidalapi.Quality, config.app["services"]["tidal"]["quality"]):
            quality = getattr(tidalapi.Quality, config.app["services"]["tidal"]["quality"])
        else:
            quality = tidalapi.Quality.high
        # We need to instantiate a config object to pass quality settings.
        _config = tidalapi.Config(quality=quality)
        username = config.app["services"]["tidal"]["username"]
        password = config.app["services"]["tidal"]["password"]
        log.debug("Using quality: %s" % (quality,))
        self.session = tidalapi.Session(config=_config)
        self.session.login(username=username, password=password)

    def get_file_format(self):
        """ Returns the file format (mp3 or flac) depending in quality set. """
        if config.app["services"]["tidal"]["quality"] == "lossless":
            self.file_extension = "flac"
        elif config.app["services"]["tidal"]["avoid_transcoding"] == True:
            self.file_extension = "m4a"
        else:
            self.file_extension = "mp3"
        return self.file_extension

    def transcoder_enabled(self):
        # If quality is set to high, tidal returns audio in AAC format at 256 KBPS. So we convert it with vlc to mp3 at 320KBPS.
        # toDo: Shall this be a setting and allow MusicDL to spit out the m4a file directly?
        if config.app["services"]["tidal"]["quality"] == "lossless":
            return False
        elif config.app["services"]["tidal"]["avoid_transcoding"]:
            return False
        else:
            return True

    def search(self, text, page=1):
        if text == "" or text == None:
            raise ValueError("Text must be passed and should not be blank.")
        log.debug("Retrieving data from Tidal...")
        # Check for top:// protocol.
        if text.startswith("top://"):
            text = text.replace("top://", "")
            return self.search_for_top(text)
        fieldtypes = ["artist", "album", "playlist"]
        field = "track"
        for i in fieldtypes:
            if text.startswith(i+"://"):
                field = i
                text = text.replace(i+"://", "")
                log.debug("Searching for %s..." % (field))
        search_response = self.session.search(value=text, field=field)
        self.results = []
        if field == "track":
            data = search_response.tracks
        elif field == "artist":
            data = []
            artist = search_response.artists[0].id
            if config.app["services"]["tidal"]["include_albums"]:
                albums = self.session.get_artist_albums(artist)
                for album in albums:
                    tracks = self.session.get_album_tracks(album.id)
                    for track in tracks:
                        track.album = album
                        data.append(track)
            if config.app["services"]["tidal"]["include_compilations"]:
                compilations = self.session.get_artist_albums_other(artist)
                for album in compilations:
                    tracks = self.session.get_album_tracks(album.id)
                    for track in tracks:
                        data.append(track)
            if config.app["services"]["tidal"]["include_singles"]:
                singles = self.session.get_artist_albums_ep_singles(artist)
                for album in singles:
                    tracks = self.session.get_album_tracks(album.id)
                    for track in tracks:
#                                               track.single = True
                        data.append(track)
        for search_result in data:
            s = base.song(self)
            s.title = search_result.name
            s.artist = search_result.artist.name
            s.duration = seconds_to_string(search_result.duration)
            s.url = search_result.id
            s.tracknumber = str(search_result.track_num)
            s.album = search_result.album.name
            if search_result.album.num_tracks == None:
                s.single = True
            s.info = search_result
            self.results.append(s)
        log.debug("{0} results found.".format(len(self.results)))

    def search_for_top(self, artist):
        search_response = self.session.search(value=artist, field="artist")
        self.results = []
        artist = search_response.artists[0].id
        results = self.session.get_artist_top_tracks(artist)
        for search_result in results:
            s = base.song(self)
            s.title = search_result.name
            s.artist = search_result.artist.name
            s.duration = seconds_to_string(search_result.duration)
            s.url = search_result.id
            s.tracknumber = str(search_result.track_num)
            s.album = search_result.album.name
            if search_result.album.num_tracks == None:
                s.single = True
            s.info = search_result
            self.results.append(s)
        log.debug("{0} results found.".format(len(self.results)))

    def format_number(self, number):
        if number < 10:
            return "0%d" % (number)
        else:
            return number

    def get_download_url(self, url):
        url = self.session.get_media_url(url)
        if url.startswith("https://") or url.startswith("http://") == False:
            url = "rtmp://"+url
        return url

    def format_track(self, item):
        if not hasattr(item, "single"):
            return "{0}. {1}".format(self.format_number(int(item.tracknumber)), item.title)
        else:
            return "{title}. {artist}. {duration}".format(title=item.title, duration=item.duration, artist=item.artist)

class settings(base.baseSettings):
    name = _("Tidal")
    config_section = "tidal"

    def get_quality_list(self):
        results = dict(low=_("Low"), high=_("High"), lossless=_("Lossless"))
        return results

    def get_quality_value(self, *args, **kwargs):
        q = self.get_quality_list()
        for i in q.keys():
            if q.get(i) == self.quality.GetStringSelection():
                return i

    def set_quality_value(self, value, *args, **kwargs):
        q = self.get_quality_list()
        for i in q.keys():
            if i == value:
                self.quality.SetStringSelection(q.get(i))
                break

    def __init__(self, parent):
        super(settings, self).__init__(parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.enabled = wx.CheckBox(self, wx.NewId(), _("Enable this service"))
        self.enabled.Bind(wx.EVT_CHECKBOX, self.on_enabled)
        self.map.append(("enabled", self.enabled))
        sizer.Add(self.enabled, 0, wx.ALL, 5)
        self.avoid_transcoding = wx.CheckBox(self, wx.NewId(), _("Avoid transcoding when downloading"))
        self.map.append(("avoid_transcoding", self.avoid_transcoding))
        sizer.Add(self.avoid_transcoding, 0, wx.ALL, 5)
        username = wx.StaticText(self, wx.NewId(), _("Tidal username or email address"))
        self.username = wx.TextCtrl(self, wx.NewId())
        usernamebox = wx.BoxSizer(wx.HORIZONTAL)
        usernamebox.Add(username, 0, wx.ALL, 5)
        usernamebox.Add(self.username, 0, wx.ALL, 5)
        sizer.Add(usernamebox, 0, wx.ALL, 5)
        self.map.append(("username", self.username))
        password = wx.StaticText(self, wx.NewId(), _("Password"))
        self.password = wx.TextCtrl(self, wx.NewId(), style=wx.TE_PASSWORD)
        passwordbox = wx.BoxSizer(wx.HORIZONTAL)
        passwordbox.Add(password, 0, wx.ALL, 5)
        passwordbox.Add(self.password, 0, wx.ALL, 5)
        sizer.Add(passwordbox, 0, wx.ALL, 5)
        self.map.append(("password", self.password))
        self.get_account = wx.Button(self, wx.NewId(), _("You can subscribe for a tidal account here"))
        self.get_account.Bind(wx.EVT_BUTTON, self.on_get_account)
        sizer.Add(self.get_account, 0, wx.ALL, 5)
        quality = wx.StaticText(self, wx.NewId(), _("Audio quality"))
        self.quality = wx.ComboBox(self, wx.NewId(), choices=[i for i in self.get_quality_list().values()], value=_("High"), style=wx.CB_READONLY)
        qualitybox = wx.BoxSizer(wx.HORIZONTAL)
        qualitybox.Add(quality, 0, wx.ALL, 5)
        qualitybox.Add(self.quality, 0, wx.ALL, 5)
        sizer.Add(qualitybox, 0, wx.ALL, 5)
        # Monkeypatch for getting the right quality value here.
        self.quality.GetValue = self.get_quality_value
        self.quality.SetValue = self.set_quality_value
        self.map.append(("quality", self.quality))
        include = wx.StaticBoxSizer(parent=self, orient=wx.HORIZONTAL, label=_("Search by artist"))
        self.include_albums = wx.CheckBox(include.GetStaticBox(), wx.NewId(), _("Include albums"))
        self.include_compilations = wx.CheckBox(include.GetStaticBox(), wx.NewId(), _("Include compilations"))
        self.include_singles = wx.CheckBox(include.GetStaticBox(), wx.NewId(), _("Include singles"))
        sizer.Add(include, 0, wx.ALL, 5)
        self.map.append(("include_albums", self.include_albums))
        self.map.append(("include_compilations", self.include_compilations))
        self.map.append(("include_singles", self.include_singles))
        self.SetSizer(sizer)

    def on_enabled(self, *args, **kwargs):
        for i in self.map:
            if i[1] != self.enabled:
                if self.enabled.GetValue() == True:
                    i[1].Enable(True)
                else:
                    i[1].Enable(False)

    def on_get_account(self, *args, **kwargs):
        webbrowser.open_new_tab("https://tidal.com")
