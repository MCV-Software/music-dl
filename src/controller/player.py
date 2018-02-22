# -*- coding: utf-8 -*-
import random
import vlc
import logging
from pubsub import pub
from utils import call_threaded

player = None
log = logging.getLogger("player")

def setup():
	global player
	if player == None:
		player = audioPlayer()

class audioPlayer(object):

	def __init__(self):
		self.is_playing = False
		self.vol = 50
		self.is_working = False
		self.queue = []
		self.stopped = True
		self.queue_pos = 0
		self.shuffle = False
		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()
		self.event_manager = self.player.event_manager()
		self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.end_callback)

	def play(self, item):
		self.stopped = True
		if self.is_working == False:
			self.is_working = True
			if item.download_url == "":
				item.get_download_url()
			self.stream_new = self.instance.media_new(item.download_url)
			self.player.set_media(self.stream_new)
			if self.player.play() == -1:
				log.debug("Error when playing the file {0}".format(item.title,))
				pub.sendMessage("change_status", status=_("Error playing {0}. {1}.").format(item.title, e.description))
				self.stopped = True
				self.is_working = False
				self.next()
				return
			self.player.audio_set_volume(self.vol)
			pub.sendMessage("change_status", status=_("Playing {0}.").format(item.title))
			self.stopped = False
			self.is_working = False

	def next(self):
		if len(self.queue) > 0:
			if self.shuffle:
				self.queue_pos = random.randint(0, len(self.queue)-1)
			else:
				if self.queue_pos < len(self.queue)-1:
					self.queue_pos += 1
				else:
					self.queue_pos = 0
			self.play(self.queue[self.queue_pos])

	def previous(self):
		if len(self.queue) > 0:
			if self.shuffle:
				self.queue_pos = random.randint(0, len(self.queue)-1)
			else:
				if self.queue_pos > 0:
					self.queue_pos -= 1
				else:
					self.queue_pos = len(self.queue)-1
			self.play(self.queue[self.queue_pos])

	def stop(self):
		self.player.stop()
		self.stopped = True

	def pause(self):
		self.player.pause()
		if self.stopped == True:
			self.stopped = False
		else:
			self.stopped = True

	@property
	def volume(self):
		return self.vol

	@volume.setter
	def volume(self, vol):
		if vol <= 100 and vol >= 0:
			self.vol = vol
		self.player.audio_set_volume(self.vol)

	def play_all(self, list_of_items, playing=0, shuffle=False):
		if list_of_items != self.queue:
			self.queue = list_of_items
		self.shuffle = shuffle
		self.queue_pos = playing
		self.play(self.queue[self.queue_pos])

	def end_callback(self, event, *args, **kwargs):
		#https://github.com/ZeBobo5/Vlc.DotNet/issues/4
		call_threaded(self.next)

	def __del__(self):
		self.event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)