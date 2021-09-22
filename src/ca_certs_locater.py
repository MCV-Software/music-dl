# -*- coding: utf-8 -*-
import sys
if sys.version[0] == "3":
    raise ImportError()
import os
import paths

def get():
    return os.path.join(paths.app_path(), "cacerts.txt")
