# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import sys
if sys.version[0] == "2":
	if hasattr(sys, "frozen"):
		import fixes
		fixes.setup()
import i18n
i18n.setup()
import widgetUtils
import logging
import application
from platform_utils import paths

logging.basicConfig()
log = logging.getLogger("main")

def setup():
	log.debug("Starting music-dl %s" % (application.version,))
	log.debug("Application path is %s" % (paths.app_path(),))
	from controller import mainController
	app = widgetUtils.mainLoopObject()
	log.debug("Created Application mainloop object")
	r = mainController.Controller()
	app.run()

setup()
