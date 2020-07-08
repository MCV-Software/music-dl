# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import paths
import os
import glob

data_directory = None
app_type = ""

def setup():
	global data_directory, app_type
	if len(glob.glob("Uninstall.exe")) > 0: # installed copy
		if os.path.exists(paths.data_path("musicDL")) == False:
			os.mkdir(paths.data_path("musicDL"))
		data_directory = paths.data_path("musicDL")
		app_type = "installed"
	else:
		app_type = "portable"
		data_directory = os.path.join(paths.app_path(), "data")
		if os.path.exists(data_directory) == False:
			os.mkdir(data_directory)