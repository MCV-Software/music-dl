# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import isodate
import youtube_dl
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .import baseFile
from update.utils import seconds_to_string

DEVELOPER_KEY = "AIzaSyCU_hvZJEjLlAGAnlscquKEkE8l0lVOfn0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

log = logging.getLogger("extractors.youtube.com")

class interface(object):
	name = "youtube"

	def __init__(self):
		self.results = []
		self.needs_transcode = True
		log.debug("started extraction service for {0}".format(self.name,))

	def search(self, text, page=1):
		if text == "" or text == None:
			raise ValueError("Text must be passed and should not be blank.")
		if text.startswith("https") or text.startswith("http"):
			return self.search_from_url(text)
		type = "video"
		max_results = 20
		log.debug("Retrieving data from Youtube...")
		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
		search_response = youtube.search().list(q=text, part="id,snippet", maxResults=max_results, type=type).execute()
		self.results = []
		ids = []
		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				s = baseFile.song(self)
				s.title = search_result["snippet"]["title"]
				ids.append(search_result["id"]["videoId"])
				s.url = "https://www.youtube.com/watch?v="+search_result["id"]["videoId"]
				self.results.append(s)
		ssr = youtube.videos().list(id=",".join(ids), part="contentDetails", maxResults=1).execute()
		for i in range(len(self.results)):
			self.results[i].duration = seconds_to_string(isodate.parse_duration(ssr["items"][i]["contentDetails"]["duration"]).total_seconds())
		log.debug("{0} results found.".format(len(self.results)))

	def search_from_url(self, url):
		log.debug("Getting download URL for {0}".format(url,))
		if "playlist?list=" in url:
			return self.search_from_playlist(url)
		ydl = youtube_dl.YoutubeDL({'quiet': True, 'no_warnings': True, 'logger': log, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
		with ydl:
			result = ydl.extract_info(url, download=False)
			if 'entries' in result:
				videos = result['entries']
			else:
				videos = [result]
		for video in videos:
			s = baseFile.song(self)
			s.title = video["title"]
			s.url = video["webpage_url"] # Cannot use direct URL here cause Youtube URLS expire after a minute.
			s.duration = seconds_to_string(video["duration"])
			self.results.append(s)
		log.debug("{0} results found.".format(len(self.results)))

	def search_from_playlist(self, url):
		id = url.split("=")[1]
		max_results = 50
		log.debug("Retrieving data from Youtube...")
		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
		search_response = youtube.playlistItems().list(playlistId=id, part="id, status, snippet", maxResults=max_results).execute()
		self.results = []
		ids = []
		for search_result in search_response.get("items", []):
			if search_result["status"]["privacyStatus"] != "public":
				continue
			s = baseFile.song(self)
			s.title = search_result["snippet"]["title"]
			ids.append(search_result["snippet"]["resourceId"]["videoId"])
			s.url = "https://www.youtube.com/watch?v="+search_result["snippet"]["resourceId"]["videoId"]
			self.results.append(s)
		ssr = youtube.videos().list(id=",".join(ids), part="contentDetails", maxResults=50).execute()
		for i in range(len(self.results)):
			self.results[i].duration = seconds_to_string(isodate.parse_duration(ssr["items"][i]["contentDetails"]["duration"]).total_seconds())
		log.debug("{0} results found.".format(len(self.results)))

	def get_download_url(self, url):
		log.debug("Getting download URL for {0}".format(url,))
		ydl = youtube_dl.YoutubeDL({'quiet': True, 'no_warnings': True, 'logger': log, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
		with ydl:
			result = ydl.extract_info(url, download=False)
			if 'entries' in result:
				video = result['entries'][0]
			else:
				video = result
		log.debug("Download URL: {0}".format(video["url"],))
		return video["url"]

	def format_track(self, item):
		return "{0} {1}".format(item.title, item.duration)