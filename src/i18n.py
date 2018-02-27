# -*- coding: utf-8 -*-
import os
import gettext
import locale
from platform_utils import paths

def setup():
	lang = locale.getdefaultlocale()[0]
	os.environ["lang"] = lang
	gettext.install("musicdl", localedir=os.path.join(paths.app_path(), "locales"))