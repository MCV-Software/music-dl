# -*- coding: utf-8 -*-
""" Unittests for internationalization features. This test is here for avoiding breaking things between gettext for python 2 and 3. """
from __future__ import unicode_literals
import os
import unittest
import sys
import i18n

# Python 2/3 compat.
if sys.version[0] == "2":
	strtype = unicode
else:
	strtype = str

class i18nTestCase(unittest.TestCase):

	def test_i18n_unicode(self):
		""" Testing gettext function so it will generate only unicode strings both in python 2 and 3. """
		i18n.setup()
		# If something happened to i18n, it should raise a traceback in the next call
		translated_str = _("This is a string with no special characters.")
		self.assertIsInstance(translated_str, strtype)
		# Test something with a special character here.
		localized_fake_str = _("Привет всем")
		self.assertIsInstance(localized_fake_str, strtype)

if __name__ == "__main__":
	unittest.main()