## Changelog

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