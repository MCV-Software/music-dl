# -*- coding: utf-8 -*-
import i18n
import widgetUtils
import logging
import application
from platform_utils import paths

logging.basicConfig()
log = logging.getLogger("main")

def setup():
	log.debug("Starting music-dl %s" % (application.version,))
	log.debug("Application path is %s" % (paths.app_path(),))
	i18n.setup()
	from controller import mainController
	app = widgetUtils.mainLoopObject()
	log.debug("Created Application mainloop object")
	r = mainController.Controller()
	app.run()

setup()
