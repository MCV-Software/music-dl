# -*- coding: cp1252 -*-
import os
import config_utils
import paths
import storage
import logging

log = logging.getLogger("config")

MAINFILE = "settings.conf"
MAINSPEC = "app-configuration.defaults"

app = None
def setup ():
	global app
	log.debug("Loading global app settings...")
	app = config_utils.load_config(os.path.join(storage.data_directory, MAINFILE), os.path.join(paths.app_path(), MAINSPEC))
 