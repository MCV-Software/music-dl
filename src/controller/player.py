# -*- coding: utf-8 -*-
import os
import random
import logging
import config
import time
import mpv
from pubsub import pub

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
        self.player = mpv.MPV()

        # Fires at the end of every file and attempts to play the next one.
        @self.player.event_callback('end-file')
        def handle_end_idle(event):
            if event.as_dict()["reason"] == b"aborted" or event.as_dict()["reason"] == b"stop":
                return
            log.debug("Reached end of file stream.")
            if len(self.queue) > 1:
                log.debug("Requesting next item...")
                self.next()

    def get_output_devices(self):
        """ Retrieve enabled output devices so we can switch or use those later. """
        return None

    def set_output_device(self, device_name):
        """ Set Output device to be used in LibVLC"""
        log.debug("Setting output audio device to {device}...".format(device=device_name,))
#            config.app["main"]["output_device"] = "Default"

    def play(self, item):
        self.stopped = True
        if self.is_working == False:
            self.is_working = True
            if item.download_url == "":
                item.get_download_url()
            log.debug("playing {0}...".format(item.download_url,))
            self.player.play(item.download_url)
            self.player.volume = self.vol
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
        self.player.pause = True
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
        if self.player != None:
            self.player.volume = self.vol

    def play_all(self, list_of_items, playing=0, shuffle=False):
        if list_of_items != self.queue:
            self.queue = list_of_items
        self.shuffle = shuffle
        self.queue_pos = playing
        self.play(self.queue[self.queue_pos])