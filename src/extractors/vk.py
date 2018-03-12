# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import requests
try:
	import urllib.parse as urlparse
except ImportError:
	import urllib as urlparse
from .import baseFile
from update.utils import seconds_to_string

api_endpoint = "https://api-2.datmusic.xyz"

class interface(object):

	def __init__(self):
		self.results = []
		self.name = "vk"
		self.needs_transcode = False

	def search(self, text, page=1):
		self.results = []
		url = "{0}/search?q={1}".format(api_endpoint, text)
		search_results = requests.get(url)
		search_results = search_results.json()["data"]
		for i in search_results:
			s = baseFile.song(self)
			s.title = i["title"]
			# URRL is not needed here as download_url is already provided. So let's skip that part.
			s.duration = seconds_to_string(i["duration"])
			s.download_url = i["stream"]
			self.results.append(s)

	def get_download_url(self, url):
		return None