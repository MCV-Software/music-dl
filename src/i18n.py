# -*- coding: utf-8 -*-
import os
import gettext
import locale
from platform_utils import paths

def setup():
	gettext.install("music-dl", localedir=os.path.join(paths.app_path(), "locales"))