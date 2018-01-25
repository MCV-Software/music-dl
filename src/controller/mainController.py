# -*- coding: utf-8 -*-
""" main controller for MusicDL"""
import wx
import logging
import widgetUtils
import utils
from pubsub import pub
from wxUI import mainWindow
from extractors import zaycev
from . import player

log = logging.getLogger("controller.main")

class Controller(object):

	def __init__(self):
		super(Controller, self).__init__()
		log.debug("Starting main controller...")
		# Setting up the player object
		player.setup()
		# Instantiate the only available extractor for now.
		self.extractor = zaycev.interface()
		# Get main window
		self.window = mainWindow.mainWindow()
		log.debug("Main window created")
		self.window.change_status(_("Ready"))
		# Here we will save results for searches as song objects.
		self.results = []
		self.connect_events()
		# Shows window.
		self.window.Show()

	def get_status_info(self):
		""" Formatting string for status bar messages """
		if len(self.results) > 0:
			results = _("Showing {0} results.").format(len(self.results))
		else:
			results = ""
		final = results+" "
		return final

	def connect_events(self):
		""" connects all widgets to their corresponding events."""
		widgetUtils.connect_event(self.window.search, widgetUtils.BUTTON_PRESSED, self.on_search)
		widgetUtils.connect_event(self.window.list, widgetUtils.LISTBOX_ITEM_ACTIVATED, self.on_activated)
		widgetUtils.connect_event(self.window.list, widgetUtils.KEYPRESS, self.on_keypress)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_play_pause, menuitem=self.window.player_play)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_next, menuitem=self.window.player_next)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_previous, menuitem=self.window.player_previous)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_play_all, menuitem=self.window.player_play_all)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_stop, menuitem=self.window.player_stop)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_volume_down, menuitem=self.window.player_volume_down)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_volume_up, menuitem=self.window.player_volume_up)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_mute, menuitem=self.window.player_mute)
		pub.subscribe(self.change_status, "change_status")

	# Event functions. These functions will call other functions in a thread and are bound to widget events.
	def on_search(self, *args, **kwargs):
		utils.call_threaded(self.search)

	def on_activated(self, *args, **kwargs):
		utils.call_threaded(self.play)

	def on_keypress(self, ev):
		if ev.GetKeyCode() == wx.WXK_RETURN:
			utils.call_threaded(self.play)
		ev.Skip()

	def on_play_pause(self, *args, **kwargs):
		if player.player.check_is_playing() != False:
			return player.player.pause()
		return utils.call_threaded(self.play)

	def on_next(self, *args, **kwargs):
		item = self.window.get_item()
		if item <= len(self.results):
			self.window.list.SetSelection(item+1)
		else:
			self.window.list.SetSelection(0)
		return utils.call_threaded(self.play)

	def on_previous(self, *args, **kwargs):
		item = self.window.get_item()
		if item > 0:
			self.window.list.SetSelection(item-1)
		else:
			self.window.list.SetSelection(len(self.results)-1)
		return utils.call_threaded(self.play)

	def on_play_all(self, *args, **kwargs):
		pass

	def on_stop(self, *args, **kwargs):
		player.player.stop()

	def on_volume_down(self, *args, **kwargs):
		player.player.volume = player.player.volume-5

	def on_volume_up(self, *args, **kwargs):
		player.player.volume = player.player.volume+5

	def on_mute(self, *args, **kwargs):
		player.player.volume = 0

	def change_status(self, status):
		""" Function used for changing the status bar from outside the main controller module."""
		self.window.change_status("{0} {1}".format(status, self.get_status_info()))

	# real functions. These functions really are doing the work.
	def search(self, *args, **kwargs):
		text = self.window.get_text()
		if text == "":
			return
		self.window.list.Clear()
		self.change_status(_("Searching {0}... ").format(text,))
		self.extractor.search(text)
		self.results = self.extractor.results
		for i in self.results:
			self.window.list.Append(i.format_track())
		self.change_status("")

	def play(self):
		self.change_status(_("Loading song..."))
		url = self.extractor.get_download_url(self.results[self.window.get_item()].url)
		player.player.play(url)

	def play_audios(self, audios):
		player.player.play_all(audios, shuffle=self.window.player_shuffle.IsChecked())
