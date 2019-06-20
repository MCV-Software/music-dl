# -*- coding: utf-8 -*-
import logging
import tidalapi
import config
from update.utils import seconds_to_string
from .import base

log = logging.getLogger("extractors.tidal.com")

class interface(object):
	name = "tidal"
	enabled = config.app["services"]["tidal"].get("enabled")
	# This should not be enabled if credentials are not in config.
	if config.app["services"]["tidal"]["username"] == "" or config.app["services"]["tidal"]["password"] == "":
		enabled = False

	def __init__(self):
		self.results = []
		self.needs_transcode = False
		log.debug("started extraction service for {0}".format(self.name,))
		# Assign quality or switch to high if not specified/not found.
		if hasattr(tidalapi.Quality, config.app["services"]["tidal"]["quality"]):
			quality = getattr(tidalapi.Quality, config.app["services"]["tidal"]["quality"])
		else:
			quality = tidalapi.Quality.high
		_config = tidalapi.Config(quality=quality)
		username = config.app["services"]["tidal"]["username"]
		password = config.app["services"]["tidal"]["password"]
		log.debug("Using quality: %s" % (quality,))
		self.session = tidalapi.Session(config=_config)
		self.session.login(username=username, password=password)
		if config.app["services"]["tidal"]["quality"] == "lossless":
			self.file_extension = "flac"
		else:
			self.file_extension = "mp3"

	def search(self, text, page=1):
		if text == "" or text == None:
			raise ValueError("Text must be passed and should not be blank.")
		log.debug("Retrieving data from Tidal...")
		fieldtypes = ["artist", "album", "playlist"]
		field = "track"
		for i in fieldtypes:
			if text.startswith(i+"://"):
				field = i
				text = text.replace(i+"://", "")
				log.debug("Searching for %s..." % (field))
		search_response = self.session.search(value=text, field=field)
		self.results = []
		if field == "track":
			data = search_response.tracks
		elif field == "artist":
			data = []
			artist = search_response.artists[0].id
			albums = self.session.get_artist_albums(artist)
			for album in albums:
				tracks = self.session.get_album_tracks(album.id)
				for track in tracks:
					data.append(track)
			compilations = self.session.get_artist_albums_other(artist)
			for album in compilations:
				tracks = self.session.get_album_tracks(album.id)
				for track in tracks:
					data.append(track)
			singles = self.session.get_artist_albums_ep_singles(artist)
			for album in singles:
				tracks = self.session.get_album_tracks(album.id)
				for track in tracks:
					data.append(track)
		for search_result in data:
			s = base.song(self)
			s.title = search_result.name
			s.artist = search_result.artist.name
			s.duration = seconds_to_string(search_result.duration)
			s.url = search_result.id
			s.info = search_result
			self.results.append(s)
		log.debug("{0} results found.".format(len(self.results)))

	def get_download_url(self, url):
		url = self.session.get_media_url(url)
		if url.startswith("https://") or url.startswith("http://") == False:
			url = "rtmp://"+url
		return url

	def format_track(self, item):
		return "{title}. {artist}. {duration}".format(title=item.title, duration=item.duration, artist=item.artist)