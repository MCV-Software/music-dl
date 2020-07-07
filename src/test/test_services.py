# -*- coding: utf-8 -*-
""" Unittests for services present in MusicDL. """
from __future__ import unicode_literals
import sys
import unittest
import re
import i18n
import storage
import config
storage.setup()
config.setup()
i18n.setup()
import services
from services import base

# Pytohn 2/3 compat
if sys.version[0] == "2":
	strtype = unicode
else:
	strtype = str

class servicesTestCase(unittest.TestCase):

	def setUp(self):
		""" Configure i18n functions for avoiding a traceback later. """
		i18n.setup()

	def search(self, service_name, search_query="piano", skip_validation=False):
		""" Search a video in the passed service name. """
		# Test basic instance stuff.
		service_instance = getattr(services, service_name).interface()
		service_instance.search(search_query)
		self.assertIsInstance(service_instance.results, list)
		self.assertNotEqual(len(service_instance.results), 0)
		self.assertIsInstance(len(service_instance.results), int)
		# Take and test validity of the first item.
		item = service_instance.results[0]
		self.assertIsInstance(item, base.song)
		self.assertIsInstance(item.title, strtype)
		self.assertNotEqual(item.title, "")
		if service_name == "youtube": # Duration is only available for youtube.
			self.assertIsInstance(item.duration, strtype)
			self.assertNotEqual(item.duration, "")
		self.assertIsInstance(item.url, strtype)
		self.assertNotEqual(item.url, "")
		if service_name == "youtube" and skip_validation == False:
			match = re.search("((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", item.url)
			self.assertNotEqual(match, None)
		formatted_track = item.format_track()
		self.assertIsInstance(formatted_track, strtype)
		self.assertNotEquals(formatted_track, "")
		item.get_download_url()
		self.assertIsInstance(item.download_url, strtype)
		self.assertNotEquals(item.download_url, "")

	def search_blank(self, extractor_name, search_query=""):
		""" Attempt to search in any extractor by passing a blank string. """
		extractor_instance = getattr(services, extractor_name).interface()
		self.assertRaises(ValueError, extractor_instance.search, search_query)

	def test_youtube_search(self):
		""" Testing a Youtube search. """
		self.search("youtube")

	def test_youtube_search_unicode(self):
		""" Testing a Youtube search using unicode characters. """
		self.search("youtube", "Пианино")

	def test_youtube_search_blank(self):
		""" Testing a youtube search when text is blank or not passed. """
		self.search_blank("youtube")

	def test_youtube_direct_link(self):
		""" Testing a search in youtube by passing a direct link. """
		self.search("youtube", "https://www.youtube.com/watch?v=XkeU8w2Y-2Y")

	def test_youtube_playlist(self):
		""" Testing a youtube search by passing a link to a playlist. """
		self.search("youtube", "https://www.youtube.com/channel/UCPTYdUGtBMuqGg6ZtvYC1zQ", skip_validation=True)
	# Uncomment the following test only if you live or test this in Russia.
#	def test_zaycev_search(self):
#		""" Testing a search made in zaycev.net """
#		self.search("zaycev")

#	def test_zaycev_search_unicode(self):
#		""" Testing a search made in zaycev.net with unicode characters. """
#		self.search("zaycev", "Пианино")

#	def test_zaycev_search_blank(self):
#		""" Testing a search in zaycev.net when text is blank. """
#		self.search_blank("zaycev")

if __name__ == "__main__":
	unittest.main()