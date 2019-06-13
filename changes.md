## Changelog

## Version 0.6

* Updated VLC libraries and plugins to version 3.0.7.
* Added a new and experimental extractor for supporting tidal.
    * Take into account that this extractor requires you to have a paid account on tidal. Depending in the account level, you will be able to play and download music in high quality or lossless audio. MusicDL will handle both, though at the current moment, only downloading of lossless audio is implemented.
    * There is a new search mode supported in this service. You can retrieve all work for a certain artist by using the protocol artist://, plus the name of the artist you want to retrieve. For example, artist://The beatles will retrieve everything made by the beatles available in the service. The search results will be grouped by albums, compilations and singles, in this order.
* Due to recent problems with mail.ru and unavailable content in most cases, the service has been removed from MusicDL.
* YouTube:
    * Fixed a long standing issue with playback of some elements, due to Youtube sending encrypted versions of these videos. Now playback should be better.
    * Updated YoutubeDL to version 2019.6.7
* zaycev.net:
    * Fixed extractor for searching and playing music in zaycev.net.
    * Unfortunately, it seems this service works only in the russian Federation and some other CIS countries due to copyright reasons.

## Version 0.4

* Fixed an error when creating a directory located in %appdata%, when using MusicDL as an installed version. MusicDL should be able to work normally again.
* Removed VK from the list of supported services for now.
* MusicDL will no longer set volume at 50% when it starts. It will save the volume in a settings file, so it will remember volume settings across restarts.
* Added an option in the help menu to report an issue. You can use this feature for sending reports of problems you have encountered while using the application. You will need to provide your email address, though it will not be public anywhere. Your email address will be used only for contacting you if necessary.
* changes in Youtube module:
    * Updated YoutubeDL to latest version.

## Version 0.3

* MusicDL is built with two different Python versions, for supporting older operating systems. If the version 0.2 works for you, you don't need to do anything. If that version never worked for your system, you may try MusicDL built with Python 2.
* Added new translations: Russian and Serbian.
* Fixed a bug introduced by keystrokes for changing position while using MusicDL with NVDA.
* Included a logger system. Now everything will be recorded in a file called info.log, useful for reporting issues. Bear in mind that the file will be flushed every time MusicDL starts.
* If you're using an installed version, MusicDL will create a folder called MusicDL in %appdata%, for saving settings in future and logs for now. If you're using a portable version, the folder will be called data, and will be created in the application directory.
* Changes in VK.com module:
    * Fixed a bug that was making musicDL unable to search with spaces.
    * In results, artist name is also included whenever extraction of such information is possible.
* Changes in Youtube module:
    * Updated Youtube-dl to version 2018.3.26
    * You can paste a youtube link (link to video) and MusicDL will put the result in the list.
    * You can paste a playlist link and MusicDL will place the first 50 results of the playlist in the results.