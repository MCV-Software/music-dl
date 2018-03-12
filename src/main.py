# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import os
import logging
import storage
import traceback
import sys
storage.setup()
logging.basicConfig(filename=os.path.join(storage.data_directory, "info.log"), level=logging.DEBUG, filemode="w")
sys.excepthook = lambda x, y, z: logging.critical(''.join(traceback.format_exception(x, y, z)))
log = logging.getLogger("main")
log.debug("Logger initialized. Saving debug to {0}".format(storage.data_directory,))
log.debug("Using Python version {0}".format(sys.version,))
if sys.version[0] == "2":
	if hasattr(sys, "frozen"):
		log.debug("Applying fixes for Python 2 frozen executables.")
		import fixes
		fixes.setup()
import i18n
i18n.setup()
import application
import widgetUtils
from platform_utils import paths

def setup():
	log.debug("Starting music-dl %s" % (application.version,))
	log.debug("Application path is %s" % (paths.app_path(),))
	from controller import mainController
	app = widgetUtils.mainLoopObject()
	log.debug("Created Application mainloop object")
	r = mainController.Controller()
	app.run()

setup()
