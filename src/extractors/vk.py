# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import requests
import logging
try:
	import urllib.parse as urlparse
except ImportError:
	import urllib as urlparse
from .import baseFile
from update.utils import seconds_to_string

api_endpoint = "https://api-2.datmusic.xyz"
log = logging.getLogger("extractors.vk.com")

class interface(object):

	def __init__(self):
		self.results = []
		self.name = "vk"
		self.needs_transcode = False
		log.debug("started extraction service for {0}".format(self.name,))

	def search(self, text, page=1):
		self.results = []
		url = "{0}/search?q={1}".format(api_endpoint, text)
		log.debug("Retrieving data from {0}...".format(url,))
		search_results = requests.get(url)
		search_results = search_results.json()["data"]
		for i in search_results:
			s = baseFile.song(self)
			s.title = i["title"]
			s.artist = i["artist"]
			# URRL is not needed here as download_url is already provided. So let's skip that part.
			s.duration = seconds_to_string(i["duration"])
			s.download_url = i["stream"]
			self.results.append(s)
		log.debug("{0} results found.".format(len(self.results)))

	def get_download_url(self, url):
		log.debug("This function has been called but does not apply to this module.")
		return None

	def format_track(self, item):
		return "{0}. {1}".format(item.artist, item.title)