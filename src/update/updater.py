# -*- coding: utf-8 -*-
import sys
import application
import platform
import logging
from requests.exceptions import ConnectionError
from . import update
from .wxUpdater import *
logger = logging.getLogger("updater")

def do_update(update_type="alpha"):
 # Updates cannot be performed in the source code version.
 if hasattr(sys, "frozen") == False:
  return
 endpoint = application.update_url
 version = application.update_next_version
 try:
  return update.perform_update(endpoint=endpoint, current_version=version, app_name=application.name, update_type=update_type, update_available_callback=available_update_dialog, progress_callback=progress_callback, update_complete_callback=update_finished)
 except ConnectionError:
  logger.exception("Update failed.")