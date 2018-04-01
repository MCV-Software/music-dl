# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
from platform_utils import paths
import os
import glob

data_directory = None

def setup():
	global data_directory
	if len(glob.glob("Uninstall.exe")) > 0: # installed copy
		if os.path.exists(paths.app_data_path("musicDL")) == False:
			paths.prepare_app_data_path("musicDL")
			data_directory = paths.app_data_path("musicDL")
	else:
		data_directory = os.path.join(paths.app_path(), "data")
		if os.path.exists(data_directory) == False:
			os.mkdir(data_directory)