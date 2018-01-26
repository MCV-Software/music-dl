# -*- coding: utf-8 -*-
import random
import sound_lib
import logging
from sound_lib.stream import URLStream
from sound_lib.main import BassError
from sound_lib.output import Output
from pubsub import pub
from utils import RepeatingTimer

player = None
log = logging.getLogger("player")

def setup():
	global player
	if player == None:
		Output()
		player = audioPlayer()

class audioPlayer(object):

	def __init__(self):
		self.is_playing = False
		self.stream = None
		self.vol = 100
		self.is_working = False
		self.queue = []
		self.stopped = True
		self.queue_pos = 0
		self.shuffle = False

	def play(self, item):
		if self.stream != None and self.stream.is_playing == True:
			try:
				self.stream.stop()
			except BassError:
				log.exception("error when stopping the file")
			self.stopped = True
		# Make sure  there are no other sounds trying to be played.
		if self.is_working == False:
			self.is_working = True
			if item.download_url == "":
				item.get_download_url()
			try:
				self.stream = URLStream(url=item.download_url)
			except BassError as e:
				log.debug("Error when playing the file {0}".format(item.title,))
				pub.sendMessage("change_status", status=_("Error playing {0}. {1}.").format(item.title, e.description))
				self.stopped = True
				self.is_working = False
				self.next()
				return
			self.stream.volume = self.vol/100.0
			self.stream.play()
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
		if self.stream != None and self.stream.is_playing == True:
			self.stream.stop()
			self.stopped = True

	def pause(self):
		if self.stream != None:
			if self.stream.is_playing == True:
				self.stream.pause()
				self.stopped = True
			else:
				try:
					self.stream.play()
					self.stopped = False
				except BassError:
					pass

	@property
	def volume(self):
#		if self.stream != None:
		return self.vol

	@volume.setter
	def volume(self, vol):
		if vol <= 100 and vol >= 0:
			self.vol = vol
		if self.stream != None:
			self.stream.volume = self.vol/100.0

	def play_all(self, list_of_items, playing=0, shuffle=False):
		if list_of_items != self.queue:
			self.queue = list_of_items
		self.shuffle = shuffle
		self.queue_pos = playing
		self.play(self.queue[self.queue_pos])
		if not hasattr(self, "worker"):
			self.worker = RepeatingTimer(5, self.player_function)
			self.worker.start()

	def player_function(self):
		if self.stream != None and self.stream.is_playing == False and self.stopped == False and len(self.stream) == self.stream.position:
			if len(self.queue) == 0:
				return
			self.next()

	def check_is_playing(self):
		if self.stream == None:
			return False
		if self.stream != None and self.stream.is_playing == False:
			return False
		else:
			return True

