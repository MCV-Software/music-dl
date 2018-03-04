# -*- coding: utf-8 -*-
""" Setup file to create executables and distribute the source code of this application. Don't forget this file! """
############################################################
#    Copyright (c) 2016 Manuel Eduardo Cortéz Vallejo <manuel@manuelcortez.net>
#       
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################
from setuptools import setup, find_packages
import py2exe
import os
import platform
from glob import glob
from requests import certs

def get_data():
	return [("", ["libvlccore.dll", "libvlc.dll", "cacerts.txt"]), ("", [certs.where()]),]+get_locales()

def get_locales():
	answer = []
	for root, dirs, files in os.walk('locales'):
		new = (root, glob(os.path.join(root, '*.mo')))
		answer.append(new)
	return answer


if __name__ == '__main__':
	import i18n
	i18n.setup()
	import application
	setup(
		name = application.name,
		author = application.author,
		author_email = application.authorEmail,
		version = application.version,
		url = application.url,
		packages= find_packages(),
		data_files = get_data(),
		options = {
			'py2exe': {   
				'optimize':2,
			'packages': ["pubsub", "pubsub.core", "pubsub.core.kwargs"],
				'dll_excludes': ["MPR.dll", "api-ms-win-core-apiquery-l1-1-0.dll", "api-ms-win-core-console-l1-1-0.dll", "api-ms-win-core-delayload-l1-1-1.dll", "api-ms-win-core-errorhandling-l1-1-1.dll", "api-ms-win-core-file-l1-2-0.dll", "api-ms-win-core-handle-l1-1-0.dll", "api-ms-win-core-heap-obsolete-l1-1-0.dll", "api-ms-win-core-libraryloader-l1-1-1.dll", "api-ms-win-core-localization-l1-2-0.dll", "api-ms-win-core-processenvironment-l1-2-0.dll", "api-ms-win-core-processthreads-l1-1-1.dll", "api-ms-win-core-profile-l1-1-0.dll", "api-ms-win-core-registry-l1-1-0.dll", "api-ms-win-core-synch-l1-2-0.dll", "api-ms-win-core-sysinfo-l1-2-0.dll", "api-ms-win-security-base-l1-2-0.dll", "api-ms-win-core-heap-l1-2-0.dll", "api-ms-win-core-interlocked-l1-2-0.dll", "api-ms-win-core-localization-obsolete-l1-1-0.dll", "api-ms-win-core-string-l1-1-0.dll", "api-ms-win-core-string-obsolete-l1-1-0.dll", "WLDAP32.dll", "MSVCP90.dll"],
#    'skip_archive': False
	},
	},
	windows = [
	{
		'script': 'main.py',
		'dest_base': 'MusicDL',
}
  ],
	install_requires = [
  ]
 )
