# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
# this is the first fix we have to import just before the paths module would.
# it changes a call from wintypes to ctypes.
from fixes import fix_winpaths
fix_winpaths.fix()
import os
import logging
import storage
import traceback
import sys
storage.setup()
# Let's import config module here as it is dependent on storage being setup.
import config
logging.basicConfig(handlers=[logging.FileHandler(os.path.join(storage.data_directory, "info.log"), "w", "utf-8")], level=logging.DEBUG)
# Let's capture all exceptions raised in our log file (especially useful for pyinstaller builds).
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
config.setup()
import application
import widgetUtils
import paths

def setup():
    log.debug("Starting music-dl %s" % (application.version,))
    log.debug("Application path is %s" % (paths.app_path(),))
    from controller import mainController
    app = widgetUtils.mainLoopObject()
    log.debug("Created Application mainloop object")
    r = mainController.Controller()
    app.run()

setup()
