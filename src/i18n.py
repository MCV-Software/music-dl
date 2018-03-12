# -*- coding: utf-8 -*-
import os
import gettext
import locale
import sys
import logging
from platform_utils import paths

log = logging.getLogger("i18n")

def setup():
	lang = locale.getdefaultlocale()[0]
	os.environ["lang"] = lang
	log.debug("System detected language: {0}".format(lang,))
	if sys.version[0] == "3":
		gettext.install("musicdl", localedir=os.path.join(paths.app_path(), "locales"))
	else:
		gettext.install("musicdl", localedir=os.path.join(paths.app_path(), "locales"), unicode=True)