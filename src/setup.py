# -*- coding: utf-8 -*-
import sys
import platform
import os
import i18n
from cx_Freeze import setup, Executable
from babel.messages import frontend as babel

i18n.setup()
import application

def find_accessible_output2_datafiles():
	import accessible_output2
	path = os.path.join(accessible_output2.__path__[0], 'lib')
	dest_dir = os.path.join('accessible_output2', 'lib')
	return (path, dest_dir)

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = dict(
	build_exe="dist",
	optimize=1,
	include_msvcr=True,
	zip_include_packages=["accessible_output2"],
	replace_paths = [("*", "")],
	include_files=["app-configuration.defaults", "cacerts.txt", "locales", "plugins", "libvlc.dll", "libvlccore.dll", find_accessible_output2_datafiles()],
	)

executables = [
    Executable('main.py', base=base, targetName="MusicDL")
]

setup(name='musicDL',
      version=application.version,
      description=application.description,
      # Register babel commands in setup file.
      cmdclass = {'compile_catalog': babel.compile_catalog,
                'extract_messages': babel.extract_messages,
                'init_catalog': babel.init_catalog,
                'update_catalog': babel.update_catalog},
      message_extractors = {"musicdl": [('**.py',                'python', None)]},
      options = {"build_exe": build_exe_options},
      executables=executables
      )
