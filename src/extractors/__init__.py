#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import config
from . import youtube, zaycev
# conditional imports
if config.app != None and config.app["services"]["tidal"]["username"] != "" and config.app["services"]["tidal"]["password"] != "":
	from . import tidal
