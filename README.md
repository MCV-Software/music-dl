# music-dl

[![pipeline status](https://code.manuelcortez.net/manuelcortez/music-dl/badges/master/pipeline.svg)](https://code.manuelcortez.net/manuelcortez/music-dl/commits/master)

[![coverage report](https://code.manuelcortez.net/manuelcortez/music-dl/badges/master/coverage.svg)](https://code.manuelcortez.net/manuelcortez/music-dl/commits/master)

MusicDL is an app for downloading music directly from services like Youtube, zaycev.net, mail.ru and others. I made it for practicing a few skills I have learnt about scraping the web and tools like python's beautifulsoup library, plus all of the new stuff provided with Python 3. More info in this [blog post](https://manuelcortez.net/blog/post/my-new-project-musicdl-simple-music-downloader.html)

[Visit the project's website](https://manuelcortez.net/music_dl)

## Requirements

See the requirements.txt, located in the root of this repository. Additionally, take into account the following.

* In case you want to create your own distributable version with Python 2, you'll need py2exe.

## running

Run the file main.py, located in the src directory.

## Building

### Python 3

I have provided a main.spec file for pyinstaller, so you should be able to do something like:

> C:\python3\scripts\pyinstaller.exe main.spec

And start building. Check the dist folder for results.

### Python 2

If you are using Python 2.x and want to build MusicDL, there is a setup.py file made for pyinstaller aswell. Just run it the usual way:

> C:\python2\python.exe setup.py py2exe

And You will get a distributable version of MusicDL.