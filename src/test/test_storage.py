""" Unittests for Path generation stuff. """
from __future__ import unicode_literals
import os
import sys
import shutil
import unittest
import tempfile
import storage
import paths
from fixes import fix_winpaths

class storageTestCase(unittest.TestCase):

	def test_portable_path(self):
		""" Testing if paths are generated appropiately. """
		storage.setup()
		self.assertEquals(storage.app_type, "portable")
		self.assertTrue(os.path.exists(storage.data_directory))
		self.assertEquals(storage.data_directory, os.path.join(paths.app_path(), "data"))

	def test_installer_path(self):
		""" Testing if paths are generated appropiately. """
		# this is a temporary fix for winpaths.
		fake_installer_file = open(os.path.join(paths.app_path(), "uninstall.exe"), "w")
		fake_installer_file.close()
		fix_winpaths.fix()
		storage.setup()
		self.assertEquals(storage.app_type, "installed")
		self.assertTrue(os.path.exists(storage.data_directory))
		self.assertEquals(storage.data_directory, paths.app_data_path("musicDL"))

	def tearDown(self):
		""" Removes uninstall.exe created for tests and data path."""
		fix_winpaths.fix()
		if os.path.exists(paths.app_data_path("musicDL")):
			shutil.rmtree(paths.app_data_path("musicDL"))
		if os.path.exists(os.path.join(paths.app_path(), "uninstall.exe")):
			os.remove(os.path.join(paths.app_path(), "uninstall.exe"))

if __name__ == "__main__":
	unittest.main()