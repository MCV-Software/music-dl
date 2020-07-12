# -*- coding: utf-8 -*-
import logging
import requests
import wx
import urllib.parse
from requests.auth import HTTPBasicAuth
import config
from update.utils import seconds_to_string
from .import base

log = logging.getLogger("services.vk")

url = "https://musicdl.manuelcortez.net"
application_name = "music_dl"
access_token = "e2237f17af545a4ba0bf6cb0b1a662e6"

class interface(base.baseInterface):
	name = "vk"
	enabled = config.app["services"]["vk"].get("enabled")

	#util functions.
	def get_auth(self):
		# Authentication object
		self.auth=HTTPBasicAuth(application_name, access_token)

	def get(self, endpoint, *args, **kwargs):
		response = requests.get(url+endpoint, auth=self.auth, *args, **kwargs)
		return response

	def __init__(self):
		super(interface, self).__init__()
		self.get_auth()

	def get_file_format(self):
		return "mp3"

	def transcoder_enabled(self):
		return False

	def search(self, text):
		if text == "" or text == None:
			raise ValueError("Text must be passed and should not be blank.")
		log.debug("Retrieving data from vk...")
		self.results = []
		results = self.get("/vk/search", params=dict(text=text, maxresults=config.app["services"]["vk"]["max_results"]))
		if results.status_code != 200:
			return
		results = results.json()
		for search_result in results:
			s = base.song(self)
			s.title = search_result["title"]
			s.artist = search_result["artist"]
			s.duration = seconds_to_string(search_result["duration"])
			s.url = search_result["url"]
			s.info = search_result
			self.results.append(s)

	def get_download_url(self, file_url):
		return "{url}/vk/download/?url={url2}".format(url=url, url2=file_url)

	def format_track(self, item):
		return "{title}. {artist}. {duration}".format(title=item.title, duration=item.duration, artist=item.artist)

class settings(base.baseSettings):
	name = _("VK")
	config_section = "vk"

	def __init__(self, parent):
		super(settings, self).__init__(parent=parent)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.enabled = wx.CheckBox(self, wx.NewId(), _("Enable this service"))
		self.enabled.Bind(wx.EVT_CHECKBOX, self.on_enabled)
		self.map.append(("enabled", self.enabled))
		sizer.Add(self.enabled, 0, wx.ALL, 5)
		max_results_label = wx.StaticText(self, wx.NewId(), _("Max results per page"))
		self.max_results = wx.SpinCtrl(self, wx.NewId())
		self.max_results.SetRange(1, 300)
		max_results_sizer = wx.BoxSizer(wx.HORIZONTAL)
		max_results_sizer.Add(max_results_label, 0, wx.ALL, 5)
		max_results_sizer.Add(self.max_results, 0, wx.ALL, 5)
		self.map.append(("max_results", self.max_results))
		self.SetSizer(sizer)

	def on_enabled(self, *args, **kwargs):
		for i in self.map:
			if i[1] != self.enabled:
				if self.enabled.GetValue() == True:
					i[1].Enable(True)
				else:
					i[1].Enable(False)