# -*- coding: utf-8 -*-
import logging
import tidalapi
import config
from .import baseFile
from update.utils import seconds_to_string
log = logging.getLogger("extractors.tidal.com")

class interface(object):
	name = "tidal"

	def __init__(self):
		self.results = []
		self.needs_transcode = False
		log.debug("started extraction service for {0}".format(self.name,))
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

	def search(self, text, page=1):
		if text == "" or text == None:
			raise ValueError("Text must be passed and should not be blank.")
		log.debug("Retrieving data from Tidal...")
		fieldtypes = ["artist", "album", "playlist"]
		for i in fieldtypes:
			if text.startswith(i+"://"):
				field = i
				text = text.replace(i+"://", "")
				log.debug("Searching for %s..." % (field))
		search_response = self.session.search(value=text, field=field)
		self.results = []
		if field == "tracks":
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
			s = baseFile.song(self)
			s.title = search_result.name
			s.artist = search_result.artist.name
			s.duration = seconds_to_string(search_result.duration)
			s.url = search_result.id
			self.results.append(s)

		log.debug("{0} results found.".format(len(self.results)))

	def get_download_url(self, url):
		url = self.session.get_media_url(url)
		if url.startswith("https://") or url.startswith("http://") == False:
			url = "rtmp://"+url
		return url

	def format_track(self, item):
		return "{title}. {artist}. {duration}".format(title=item.title, duration=item.duration, artist=item.artist)