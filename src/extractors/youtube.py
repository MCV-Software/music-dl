# -*- coding: utf-8 -*-
import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .import baseFile

DEVELOPER_KEY = "AIzaSyCU_hvZJEjLlAGAnlscquKEkE8l0lVOfn0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class interface(object):

	def __init__(self):
		self.results = []
		self.name = "youtube"
		self.needs_transcode = True

	def search(self, text, page=1):
		type = "video"
		max_results = 20
		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
		search_response = youtube.search().list(q=text, part="id,snippet", maxResults=max_results, type=type).execute()
		self.results = []
		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				s = baseFile.song(self)
				s.title = search_result["snippet"]["title"]
				s.url = "https://www.youtube.com/watch?v="+search_result["id"]["videoId"]
				self.results.append(s)

	def get_download_url(self, url):
		ydl = youtube_dl.YoutubeDL({'quiet': True, 'format': 'bestaudio/best', 'outtmpl': u'%(id)s%(ext)s'})
		with ydl:
			result = ydl.extract_info(url, download=False)
			if 'entries' in result:
				video = result['entries'][0]
			else:
				video = result
		return video["url"]
