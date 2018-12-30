""" Unittests for extractors present in MusicDL. """
from __future__ import unicode_literals
import sys
import unittest
import re
import i18n
import extractors
from extractors import baseFile

# Pytohn 2/3 compat
if sys.version[0] == "2":
	strtype = unicode
else:
	strtype = str

class extractorsTestCase(unittest.TestCase):

	def setUp(self):
		i18n.setup()

	def search(self, extractor_name, search_query="piano", skip_validation=False):
		""" Blank here"""
		# Test basic instance stuff.
		extractor_instance = getattr(extractors, extractor_name).interface()
		extractor_instance.search(search_query)
		self.assertIsInstance(extractor_instance.results, list)
		self.assertNotEqual(len(extractor_instance.results), 0)
		self.assertIsInstance(len(extractor_instance.results), int)
		# Take and test validity of the first item.
		item = extractor_instance.results[0]
		self.assertIsInstance(item, baseFile.song)
		self.assertIsInstance(item.title, strtype)
		self.assertNotEqual(item.title, "")
		if extractor_name == "youtube": # Duration is only available for youtube.
			self.assertIsInstance(item.duration, strtype)
			self.assertNotEqual(item.duration, "")
		self.assertIsInstance(item.url, strtype)
		self.assertNotEqual(item.url, "")
		if extractor_name == "youtube" and skip_validation == False:
			match = re.search("((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", item.url)
			self.assertNotEqual(match, None)
		formatted_track = item.format_track()
		self.assertIsInstance(formatted_track, strtype)
		self.assertNotEquals(formatted_track, "")
		item.get_download_url()
		self.assertIsInstance(item.download_url, strtype)
		self.assertNotEquals(item.download_url, "")

	def search_blank(self, extractor_name, search_query=""):
		extractor_instance = getattr(extractors, extractor_name).interface()
		self.assertRaises(ValueError, extractor_instance.search, search_query)

	def test_youtube_search(self):
		""" Testing a Youtube search. """
		self.search("youtube")

	def test_youtube_search_blank(self):
		""" Testing a youtube search when text is blank or not passed. """
		self.search_blank("youtube")

	def test_youtube_direct_link(self):
		self.search("youtube", "https://www.youtube.com/watch?v=hwDiI9p9L-g")

	def test_youtube_playlist(self):
		self.search("youtube", "https://www.youtube.com/playlist?list=PLqivnvaruBVH8fqI5JU9h5jZKV-32bbEn", skip_validation=True)

	def test_mailru_search(self):
		self.search("mailru")

	def test_mailru_search_blank(self):
		self.search_blank("mailru")

	def test_zaycev_search(self):
		self.search("zaycev")

	def test_zaycev_search_blank(self):
		self.search_blank("zaycev")

if __name__ == "__main__":
	unittest.main()