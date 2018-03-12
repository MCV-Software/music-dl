# -*- coding: utf-8 -*-
import os
import gettext
import locale
import sys
from platform_utils import paths

def setup():
	lang = locale.getdefaultlocale()[0]
	os.environ["lang"] = lang
	if sys.version[0] == "3":
		gettext.install("musicdl", localedir=os.path.join(paths.app_path(), "locales"))
	else:
		gettext.install("musicdl", localedir=os.path.join(paths.app_path(), "locales"), unicode=True)