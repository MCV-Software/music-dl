# -*- coding: utf-8 -*-
import application
import platform
import logging
from requests.exceptions import ConnectionError
from .import update
from .wxUpdater import *
logger = logging.getLogger("updater")

def do_update(endpoint=application.update_url):
	try:
		return update.perform_update(endpoint=endpoint, current_version=application.version, app_name=application.name, update_available_callback=available_update_dialog, progress_callback=progress_callback, update_complete_callback=update_finished)
	except ConnectionError:
		logger.exception("Update failed.")