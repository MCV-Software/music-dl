# -*- coding: utf-8 -*-
import os
import random
import logging
import config
import time
from sound_lib import output, stream
from pubsub import pub
from utils import call_threaded, RepeatingTimer

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
        self.worker = RepeatingTimer(5, self.player_function)
        self.worker.start()
        self.output = output.Output()
        self.set_output_device(config.app["main"]["output_device"])
        self.player = None

    def get_output_devices(self):
        """ Retrieve enabled output devices so we can switch or use those later. """
        devices = output.Output.get_device_names()
        return devices

    def set_output_device(self, device_name):
        """ Set Output device to be used in LibVLC"""
        log.debug("Setting output audio device to {device}...".format(device=device_name,))
        try:
            self.output.set_device(self.output.find_device_by_name(device_name))
        except:
            log.error("Error in input or output devices, using defaults...")
            config.app["main"]["output_device"] = "Default"

    def play(self, item):
        self.stopped = True
        if self.is_working == False:
            self.is_working = True
            if item.download_url == "":
                item.get_download_url()
            log.debug("playing {0}...".format(item.download_url,))
            if hasattr(self, "player") and self.player != None and self.player.is_playing:
                self.player.stop()
            self.player = stream.URLStream(item.download_url)
            if self.player.play() == -1:
                log.debug("Error when playing the file {0}".format(item.title,))
                pub.sendMessage("change_status", status=_("Error playing {0}. {1}.").format(item.title, e.description))
                self.stopped = True
                self.is_working = False
                self.next()
                return
            self.player.volume = self.vol/100
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
        if self.player != None:
            self.player.volume = self.vol/100

    def play_all(self, list_of_items, playing=0, shuffle=False):
        if list_of_items != self.queue:
            self.queue = list_of_items
        self.shuffle = shuffle
        self.queue_pos = playing
        self.play(self.queue[self.queue_pos])

    def player_function(self):
        """ Check if the stream has reached the end of the file  so it will play the next song. """
        if self.player != None and self.player.is_playing == False and self.stopped == False and len(self.player)-self.player.position < 50000:

            if self.queue_pos >= len(self.queue):
                self.stopped = True
                return
            elif self.queue_pos < len(self.queue):
                self.queue_pos += 1
            self.play(self.queue[self.queue_pos])

    def playback_error(self, event):
        pub.sendMessage("notify", title=_("Error"), message=_("There was an error while trying to access the file you have requested."))
