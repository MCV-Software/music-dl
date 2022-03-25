#! /usr/bin/env python
import os
import json
import datetime

print("Generating update files for Socializer...")# Determine if we are going to write stable or alpha update file.
version = datetime.datetime.now().strftime("%Y.%m.%d")
version_type = "latest"
print("Version detected: %s" % (version_type,))

# Read update description and URL'S
description = os.environ.get("CI_COMMIT_MESSAGE")
urls = dict(Windows32="https://files.mcvsoftware.com/music_dl/latest/music_dl_x86.zip", Windows64="https://files.mcvsoftware.com/music_dl/latest/music_dl_x64.zip")

# build the main dict object
data = dict(current_version=version, description=description, downloads=urls)
print("Generating file with the following arguments: %r" % (data,))
updatefile = "latest.json"
f = open(updatefile, "w")
json.dump(data, f, ensure_ascii=False)
f.close()
