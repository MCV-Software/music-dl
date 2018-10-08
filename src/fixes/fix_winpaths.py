# -*- coding: utf-8 -*-
import ctypes
import winpaths
from ctypes import wintypes

def _get_path_buf(csidl):
	path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
	result = winpaths._SHGetFolderPath(0, csidl, 0, 0, path_buf)
	return path_buf.value

def fix():
	winpaths._get_path_buf = _get_path_buf