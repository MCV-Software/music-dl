#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals    # at top of module

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
		self.info = None

	def format_track(self):
		return self.extractor.format_track(self)

	def get_download_url(self):
		self.download_url = self.extractor.get_download_url(self.url)