# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import os
import logging
import storage
storage.setup()
logging.basicConfig(filename=os.path.join(storage.data_directory, "info.log"), level=logging.DEBUG, filemode="w")
log = logging.getLogger("main")
log.debug("Logger initialized. Saving debug to {0}".format(storage.data_directory,))
log.debug("Starting music-dl %s" % (application.version,))
log.debug("Application path is %s" % (paths.app_path(),))
import sys
log.debug("Using Python version {0}".format(sys.version,))
if sys.version[0] == "2":
	if hasattr(sys, "frozen"):
		log.debug("Applying fixes for Python 2 frozen executables.")
		import fixes
		fixes.setup()
import i18n
i18n.setup()
import widgetUtils
import application
from platform_utils import paths

def setup():
	from controller import mainController
	app = widgetUtils.mainLoopObject()
	log.debug("Created Application mainloop object")
	r = mainController.Controller()
	app.run()

setup()
