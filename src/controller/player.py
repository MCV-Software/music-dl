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

	def play(self, url):
		if self.stream != None and self.stream.is_playing == True:
			try:
				self.stream.stop()
			except BassError:
				log.exception("error when stopping the file")
				self.stream = None
			self.stopped = True
			if hasattr(self, "worker") and self.worker != None:
				self.worker.cancel()
				self.worker = None
				self.queue = []
		# Make sure  there are no other sounds trying to be played.
		if self.is_working == False:
			self.is_working = True
			try:
				self.stream = URLStream(url=url)
			except BassError:
				log.debug("Error when playing the file {0}".format(url,))
				pub.sendMessage("change_status", status=_("Error playing last file"))
				return
			self.stream.volume = self.vol/100.0
			self.stream.play()
			self.stopped = False
			self.is_working = False

	def stop(self):
		if self.stream != None and self.stream.is_playing == True:
			self.stream.stop()
			self.stopped = True
		if hasattr(self, "worker") and self.worker != None:
			self.worker.cancel()
			self.worker = None
			self.queue = []

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
		if self.stream != None:
			return self.vol

	@volume.setter
	def volume(self, vol):
		if vol <= 100 and vol >= 0:
			self.vol = vol
		if self.stream != None:
			self.stream.volume = self.vol/100.0

	def play_all(self, list_of_urls, shuffle=False):
		self.stop()
		self.queue = list_of_urls
		if shuffle:
			random.shuffle(self.queue)
		self.play(self.queue[0])
		self.queue.remove(self.queue[0])
		self.worker = RepeatingTimer(5, self.player_function)
		self.worker.start()

	def player_function(self):
		if self.stream != None and self.stream.is_playing == False and self.stopped == False and len(self.stream) == self.stream.position:
			if len(self.queue) == 0:
				self.worker.cancel()
				return
			self.play(self.queue[0])
			self.queue.remove(self.queue[0])

	def check_is_playing(self):
		if self.stream == None:
			return False
		if self.stream != None and self.stream.is_playing == False:
			return False
		else:
			return True

