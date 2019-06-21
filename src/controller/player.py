# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import os
import random
import vlc
import logging
import config
import time
from pubsub import pub
from utils import call_threaded

player = None
log = logging.getLogger("controller.player")

def setup():
	global player
	if player == None:
		player = audioPlayer()

class audioPlayer(object):

	def __init__(self):
		self.is_playing = False
		self.vol = config.app["main"]["volume"]
		self.is_working = False
		self.queue = []
		self.stopped = True
		self.queue_pos = 0
		self.shuffle = False
		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()
		log.debug("Media player instantiated.")
		self.event_manager = self.player.event_manager()
		self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.end_callback)
		self.event_manager.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.playback_error)
		log.debug("Bound media playback events.")
		# configure output device
		self.set_output_device(config.app["main"]["output_device"])

	def get_output_devices(self):
		""" Retrieve enabled output devices so we can switch or use those later. """
		log.debug("Retrieving output devices...")
		devices = []
		mods = self.player.audio_output_device_enum()
		if mods:
			mod = mods
			while mod:
				mod = mod.contents
				devices.append(dict(id=mod.device, name=mod.description))
				mod = mod.next
		vlc.libvlc_audio_output_device_list_release(mods)
		return devices

	def set_output_device(self, device_id):
		""" Set Output device to be ued in LibVLC"""
		log.debug("Setting output audio device to {device}...".format(device=device_id,))
		self.player.audio_output_device_set(None, device_id)

	def play(self, item):
		self.stopped = True
		if self.is_working == False:
			self.is_working = True
			if item.download_url == "":
				item.get_download_url()
			log.debug("playing {0}...".format(item.download_url,))
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
			config.app["main"]["volume"] = vol
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

	def transcode_audio(self, item, path, _format="mp3", bitrate=320):
		""" Converts given item to mp3. This method will be available when needed automatically."""
		if item.download_url == "":
			item.get_download_url()
		log.debug("Download started: filename={0}, url={1}".format(path, item.download_url))
		temporary_filename = "chunk_{0}".format(random.randint(0,2000000))
		temporary_path = os.path.join(os.path.dirname(path), temporary_filename)
		# Let's get a new VLC instance for transcoding this file.
		transcoding_instance = vlc.Instance(*["--sout=#transcode{acodec=%s,ab=%d}:file{mux=raw,dst=\"%s\"}"% (_format, bitrate, temporary_path,)])
		transcoder = transcoding_instance.media_player_new()
		transcoder.set_mrl(item.download_url)
		pub.sendMessage("change_status", status=_(u"Downloading {0}.").format(item.title,))
		media = transcoder.get_media()
		transcoder.play()
		while True:
			state = media.get_state()
			pub.sendMessage("change_status", status=_("Downloading {0} ({1}%).").format(item.title, int(transcoder.get_position()*100)))
			if str(state) == 'State.Ended':
				break
			elif str(state) == 'state.error':
				os.remove(temporary_path)
				break
		transcoder.release()
		os.rename(temporary_path, path)
		log.debug("Download finished sucsessfully.")
		pub.sendMessage("download_finished", file=os.path.basename(path))

	def playback_error(self, event):
		pub.sendMessage("notify", title=_("Error"), message=_("There was an error while trying to access the file you have requested."))

	def __del__(self):
		self.event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)
		if hasattr(self, "event_manager"):
			self.event_manager.event_detach(vlc.EventType.MediaPlayerEncounteredError, self.playback_error)