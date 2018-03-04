# -*- coding: utf-8 -*-
import requests
import os
import logging
from platform_utils import paths

log = logging.getLogger("fixes.fix_requests")

def fix():
	log.debug("Applying fix for requests...")
	os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(paths.app_path(), "cacert.pem")
	log.debug("Changed CA path to %s" % (os.environ["REQUESTS_CA_BUNDLE"],))