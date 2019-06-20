#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import json
import requests
import logging
import config
from bs4 import BeautifulSoup
from . import base

log = logging.getLogger("extractors.zaycev.net")

class interface(base.baseInterface):
	name = "zaycev.net"
	enabled = True

	def search(self, text, page=1):
		if text == "" or text == None:
			raise ValueError("Text must be passed and should not be blank.")
		site = "http://zaycev.net/search.html?query_search=%s" % (text,)
		log.debug("Retrieving data from {0}...".format(site,))
		r = requests.get(site)
		soup = BeautifulSoup(r.text, 'html.parser')
		search_results = soup.find_all("div", {"class": "musicset-track__title track-geo__title"})
		self.results = []
		for i in search_results:
			# The easiest method to get artist and song names is to fetch links. There are only two links per result here.
			data = i.find_all("a")
			# from here, data[0] contains artist info and data[1] contains info of the retrieved song.
			s = base.song(self)
			s.title = data[1].text
			s.artist = data[0].text
			s.url = "http://zaycev.net%s" % (data[1].attrs["href"])
#			s.duration = self.hd[i]["duration"]
#			s.size = self.hd[i]["size"]
#			s.bitrate = self.hd[i]["bitrate"]
			self.results.append(s)
		log.debug("{0} results found.".format(len(self.results)))

	def get_download_url(self, url):
		log.debug("Getting download URL for {0}".format(url,))
		soups = BeautifulSoup(requests.get(url).text, 'html.parser')
		data = json.loads(requests.get('http://zaycev.net' + soups.find('div', {'class':"musicset-track"}).get('data-url')).text)
		log.debug("Download URL: {0}".format(data["url"]))
		return data["url"]

	def format_track(self, item):
		return "{0}. {1}. {2}".format(item.title, item.duration, item.size)