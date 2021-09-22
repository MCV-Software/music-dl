# -*- coding: utf-8 -*-
import youtube_dl
import logging
import wx
import config
from update.utils import seconds_to_string
from .import base

log = logging.getLogger("extractors.youtube.com")

class interface(base.baseInterface):
    name = "YouTube"
    if config.app != None: # Workaround for cx_freeze 6.2 in python 3.7.
        enabled = config.app["services"]["youtube"].get("enabled")
    else:
        enabled = False

    def search(self, text, page=1):
        if text == "" or text == None:
            raise ValueError("Text must be passed and should not be blank.")
        if text.startswith("https") or text.startswith("http"):
            return self.search_from_url(text)
        type = "video"
        max_results = config.app["services"]["youtube"]["max_results"]
        log.debug("Retrieving data from Youtube...")
        ydl = youtube_dl.YoutubeDL({'quiet': True, 'ignore_errors': True, 'no_warnings': True, 'logger': log, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
        with ydl:
            search_param = "ytsearch{}:{}".format(max_results, text)
            result = ydl.extract_info(search_param, download=False)
        self.results = []
        for search_result in result["entries"]:
            s = base.song(self)
            s.title = search_result["title"]
            s.url = "https://www.youtube.com/watch?v="+search_result["id"]
            s.duration = seconds_to_string(search_result["duration"])
            if search_result.get("track") != None:
                s.title = search_result["track"]
            if search_result.get("album") != None:
                s.album = search_result["album"]
            if search_result.get("artist") != None:
                s.artist = search_result["artist"]
            self.results.append(s)
        log.debug("{0} results found.".format(len(self.results)))

    def search_from_url(self, url):
        log.debug("Getting download URL for {0}".format(url,))
        if "playlist?list=" in url:
            return self.search_from_playlist(url)
        ydl = youtube_dl.YoutubeDL({'quiet': True, 'ignore_errors': True, 'no_warnings': True, 'logger': log, 'prefer-free-formats': True, 'format': 'bestaudio', 'outtmpl': u'%(id)s%(ext)s'})
        with ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                videos = result['entries']
            else:
                videos = [result]
        for video in videos:
            s = base.song(self)
            s.title = video["title"]
            s.url = video["webpage_url"] # Cannot use direct URL here cause Youtube URLS expire after a minute.
            s.duration = seconds_to_string(video["duration"])
            self.results.append(s)
        log.debug("{0} results found.".format(len(self.results)))

    def search_from_playlist(self, url):
        id = url.split("=")[1]
        max_results = 50
        log.debug("Retrieving data from Youtube...")
        ydl = youtube_dl.YoutubeDL({'quiet': True, 'ignore_errors': True, 'no_warnings': True, 'logger': log, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
        with ydl:
            result = ydl.extract_info(url, download=False)
        self.results = []
        for search_result in result["entries"]:
            s = base.song(self)
            s.title = search_result["title"]
            s.url = "https://www.youtube.com/watch?v="+search_result["id"]
            s.duration = seconds_to_string(search_result["duration"])
            if search_result.get("track") != None:
                s.title = search_result["track"]
            if search_result.get("album") != None:
                s.album = search_result["album"]
            if search_result.get("artist") != None:
                s.artist = search_result["artist"]
            self.results.append(s)
        log.debug("{0} results found.".format(len(self.results)))

    def get_download_url(self, url):
        log.debug("Getting download URL for {0}".format(url,))
        ydl = youtube_dl.YoutubeDL({'quiet': True, 'no_warnings': True, 'logger': log, 'prefer_insecure': True, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
        with ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
        # From here we should extract the first format so it will contain audio only.
        log.debug("Download URL: {0}".format(video["formats"][0]["url"],))
        return video["formats"][0]["url"]

    def format_track(self, item):
        return "{0} {1}".format(item.title, item.duration)

    def transcoder_enabled(self):
        return config.app["services"]["youtube"]["transcode"]

class settings(base.baseSettings):
    name = _("Youtube")
    config_section = "youtube"

    def __init__(self, parent):
        super(settings, self).__init__(parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.enabled = wx.CheckBox(self, wx.NewId(), _("Enable this service"))
        self.enabled.Bind(wx.EVT_CHECKBOX, self.on_enabled)
        self.map.append(("enabled", self.enabled))
        sizer.Add(self.enabled, 0, wx.ALL, 5)
        max_results_label = wx.StaticText(self, wx.NewId(), _("Max results per page"))
        self.max_results = wx.SpinCtrl(self, wx.NewId())
        self.max_results.SetRange(1, 50)
        max_results_sizer = wx.BoxSizer(wx.HORIZONTAL)
        max_results_sizer.Add(max_results_label, 0, wx.ALL, 5)
        max_results_sizer.Add(self.max_results, 0, wx.ALL, 5)
        self.map.append(("max_results", self.max_results))
#               self.transcode = wx.CheckBox(self, wx.NewId(), _("Enable transcode when downloading"))
#               self.map.append(("transcode", self.transcode))
#               sizer.Add(self.transcode, 0, wx.ALL, 5)
        self.SetSizer(sizer)

    def on_enabled(self, *args, **kwargs):
        for i in self.map:
            if i[1] != self.enabled:
                if self.enabled.GetValue() == True:
                    i[1].Enable(True)
                else:
                    i[1].Enable(False)
