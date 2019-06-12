#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import config
from . import mailru, youtube, zaycev
# conditional imports
if config.app["services"]["tidal"]["username"] != "" and config.app["services"]["tidal"]["password"] != "":
	from . import tidal