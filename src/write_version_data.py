#! /usr/bin/env python# -*- coding: iso-8859-1 -*-
""" Write version info (taken from the last commit) to application.py. This method has been implemented this way for running the alpha channel updates.
This file is not intended to be called by the user. It will be used only by the Gitlab CI runner."""
import datetime
import requests
from codecs import open

print("Writing version data for alpha update...")
commit_info = requests.get("https://gitlab.mcvsoftware.com/api/v4/projects/32/repository/commits/master")
commit_info = commit_info.json()
commit = commit_info["short_id"]
print("Got new version info: {commit}".format(commit=commit,))
file = open("application.py", "r", encoding="utf-8")
lines = file.readlines()
version = datetime.datetime.now().strftime("%Y.%m.%d")
lines[-1] = 'version = "{}"\n'.format(version)
file.close()
file2 = open("application.py", "w", encoding="utf-8")
file2.writelines(lines)
file2.close()
print("Wrote application.py with the new version info.")

print("Updating next version on installer setup...")
file = open("installer.nsi", "r", encoding="utf-8")
contents = file.read()
contents = contents.replace("0.7", version)
file.close()
file2 = open("installer.nsi", "w", encoding="utf-8")
file2.write(contents)
file2.close()
print("done")
