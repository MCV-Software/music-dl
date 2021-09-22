# -*- coding: utf-8 -*-
""" Unittests for fixers applied in some cases. """
from __future__ import unicode_literals
import os
import sys
import unittest
import winpaths
from fixes import fix_requests

# Let's import the reload function
if sys.version[0] == "3":
    from imp import reload

class fixesTestCase(unittest.TestCase):

#       def test_winpaths_error_in_python3(self):
#               """ Testing the winpaths error happening only in Python 3 due to changes introduced to ctypes. """
#               # If this test fails, it means winpaths has been updated to fix the ctypes issue already.
#               # Therefore this test and the corresponding issue should be removed.
#               if sys.version[0] != "3":
#                       return
#               # A reload of winpaths is needed to rever the fix of winpaths, if has been applied before
#               reload(winpaths)
#               self.assertRaises(AttributeError, winpaths.get_appdata)

    def test_requests_fix(self):
        """ Testing the requests fix and check if the certificates file exists in the provided path. """
        fix_requests.fix()
        self.assertTrue(os.path.exists(os.environ["REQUESTS_CA_BUNDLE"]))

if __name__ == "__main__":
    unittest.main()
