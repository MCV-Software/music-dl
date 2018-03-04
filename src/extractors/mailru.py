#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals    # at top of module
try:
	import urllib.parse as urlparse
except ImportError:
	import urllib as urlparse
import requests
import youtube_dl
from bs4 import BeautifulSoup
from . import baseFile

class interface(object):

	def __init__(self):
		self.results = []
		self.name = "mailru"
		self.needs_transcode = False

	def search(self, text, page=1):
		site = 'https://my.mail.ru/music/search/%s' % (text)
		r = requests.get(site)
		soup = BeautifulSoup(r.text, 'html.parser')
		search_results = soup.find_all("div", {"class": "songs-table__row__col songs-table__row__col--title title songs-table__row__col--title-hq-similar resize"})
		self.results = []
		for search in search_results:
			data = search.find_all("a")
			s = baseFile.song(self)
			s.title = data[0].text.replace("\n", "").replace("\t", "")
#			s.artist = data[1].text.replace("\n", "").replace("\t", "")
#			print(data)
			s.url = u"https://my.mail.ru"+urlparse.quote(data[0].__dict__["attrs"]["href"])
			self.results.append(s)

	def get_download_url(self, url):
		ydl = youtube_dl.YoutubeDL({'quiet': True, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
		with ydl:
			result = ydl.extract_info(url, download=False)
			if 'entries' in result:
				video = result['entries'][0]
			else:
				video = result
		return video["url"]