# -*- coding: utf-8 -*-
import sys
from . import fix_requests
from .import fix_winpaths

def setup():
	fix_requests.fix()