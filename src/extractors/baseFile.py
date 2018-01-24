#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class song(object):
	""" Represents a song in all services. Data will be filled by the service itself"""

	def __init__(self):
		self.bitrate = 0
		self.title = ""
		self.artist = ""
		self.duration = ""
		self.size = 0
		self.url = ""

	def format_track(self):
		return "{0}. {1}. {2}".format(self.title, self.duration, self.size)