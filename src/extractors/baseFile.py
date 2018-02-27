#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class song(object):
	""" Represents a song in all services. Data will be filled by the service itself"""

	def __init__(self, extractor):
		self.extractor = extractor
		self.bitrate = 0
		self.title = ""
		self.artist = ""
		self.duration = ""
		self.size = 0
		self.url = ""
		self.download_url = ""

	def format_track(self):
		if self.size != 0:
			return "{0}. {1}. {2}".format(self.title, self.duration, self.size)
		else:
			return "{0} {1}".format(self.title, self.duration)

	def get_download_url(self):
		self.download_url = self.extractor.get_download_url(self.url)