#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Base components useful for all other extractors. """
import logging
import wx
import config
log = logging.getLogger("extractors.config")

class baseInterface(object):
	name = "base"
	enabled = False
	needs_transcode = False
	results = []

	def __init__(self):
		super(baseInterface, self).__init__()
		log.debug("started extraction service for {0}".format(self.name,))

	def search(self, text, *args, **kwargs):
		raise NotImplementedError()

	def get_download_url(self, url):
		raise NotImplementedError()

	def format_track(self, item):
		raise NotImplementedError()

	def get_file_format(self):
		return "mp3"

	def transcoder_enabled(self):
		return False

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

class baseSettings(wx.Panel):
	config_section = "base"

	def __init__(self, *args, **kwargs):
		super(baseSettings, self).__init__(*args, **kwargs)
		self.map = []

	def save(self):
		for i in self.map:
			config.app["services"][self.config_section][i[0]] = i[1].GetValue()

	def load(self):
		for i in self.map:
			if i[0] in config.app["services"][self.config_section]:
				i[1].SetValue(config.app["services"][self.config_section][i[0]])
			else:
				log.error("No key available: {key} on extractor {extractor}".format(key=i[0], extractor=self.config_section))