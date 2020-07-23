# music-dl

[![pipeline status](https://code.manuelcortez.net/manuelcortez/music-dl/badges/master/pipeline.svg)](https://code.manuelcortez.net/manuelcortez/music-dl/commits/master)

[![coverage report](https://code.manuelcortez.net/manuelcortez/music-dl/badges/master/coverage.svg)](https://code.manuelcortez.net/manuelcortez/music-dl/commits/master)

MusicDL is an app for downloading music directly from services like Youtube, zaycev.net, mail.ru and others. I made it for practicing a few skills I have learnt about scraping the web and tools like python's beautifulsoup library, plus all of the new stuff provided with Python 3. More info in this [blog post](https://manuelcortez.net/blog/post/my-new-project-musicdl-simple-music-downloader.html)

[Visit the project's website](https://manuelcortez.net/music_dl)

## Requirements

See the requirements.txt, located in the root of this repository. Additionally, take into account the following.

## running

Run the file main.py, located in the src directory.

## Building

I have provided a setup.py file for cx_freeze, so you should be able to do something like:

> python setup.py build

And start building. Check the dist folder for results.

## Updating translation catalog

Every time there are new strings in the application a translations catalog update must be performed with the following commands in the src directory:

> python setup.py extract_messages -o musicdl.pot --msgid-bugs-address "manuel@manuelcortez.net" --copyright-holder "Manuel Cortez" --input-dirs .
> python setup.py update_catalog --input-file musicdl.pot --domain musicdl --output-dir locales --ignore-obsolete true

And after updating translations they should be compiled with:

> python setup.py compile_catalog --statistics -d locales --domain musicdl

## Adding new translations

The procedure for adding new translations is also easy, thanks to the following command. Just replace xx for the new locale name to add:

> python setup.py extract_messages -o musicdl.pot --msgid-bugs-address "manuel@manuelcortez.net" --copyright-holder "Copyright (C) 2019, 2020 Manuel Cortez" --input-dirs .  
> python setup.py init_catalog --domain musicdl --input-file musicdl.pot -d locales --locale xx