# -*- coding: utf-8 -*-
""" main controller for MusicDL"""
import wx
import logging
import widgetUtils
import utils
from pubsub import pub
from wxUI import mainWindow, menus
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
		if player.player.shuffle:
			shuffle = _("Shuffle on")
		else:
			shuffle = ""
		final = "{0} {1}".format(results, shuffle)
		return final

	def connect_events(self):
		""" connects all widgets to their corresponding events."""
		widgetUtils.connect_event(self.window.search, widgetUtils.BUTTON_PRESSED, self.on_search)
		widgetUtils.connect_event(self.window.list, widgetUtils.LISTBOX_ITEM_ACTIVATED, self.on_activated)
		widgetUtils.connect_event(self.window.list, widgetUtils.KEYPRESS, self.on_keypress)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_play, menuitem=self.window.player_play)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_next, menuitem=self.window.player_next)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_previous, menuitem=self.window.player_previous)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_stop, menuitem=self.window.player_stop)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_volume_down, menuitem=self.window.player_volume_down)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_volume_up, menuitem=self.window.player_volume_up)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_mute, menuitem=self.window.player_mute)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_shuffle, menuitem=self.window.player_shuffle)
		self.window.list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_play)
		self.window.list.Bind(wx.EVT_CONTEXT_MENU, self.on_context)

		pub.subscribe(self.change_status, "change_status")

	# Event functions. These functions will call other functions in a thread and are bound to widget events.
	def on_search(self, *args, **kwargs):
		utils.call_threaded(self.search)

	def on_activated(self, *args, **kwargs):
		self.on_play()

	def on_keypress(self, ev):
		if ev.GetKeyCode() == wx.WXK_RETURN:
			return self.on_play()
		elif ev.GetKeyCode() == wx.WXK_SPACE:
			return self.on_play_pause()
		elif ev.GetKeyCode() == wx.WXK_UP and ev.ControlDown():
			return self.on_volume_up()
		elif ev.GetKeyCode() == wx.WXK_DOWN and ev.ControlDown():
			return self.on_volume_down()
		elif ev.GetKeyCode() == wx.WXK_LEFT and ev.AltDown():
			return self.on_previous()
		elif ev.GetKeyCode() == wx.WXK_RIGHT and ev.AltDown():
			return self.on_next()
		ev.Skip()

	def on_play_pause(self, *args, **kwargs):
		if player.player.player.is_playing() == 1:
			return player.player.pause()
		else:
			player.player.player.play()

	def on_next(self, *args, **kwargs):
		return utils.call_threaded(player.player.next)

	def on_previous(self, *args, **kwargs):
		return utils.call_threaded(player.player.previous)

	def on_play(self, *args, **kwargs):
		items = self.results[::]
		playing_item = self.window.get_item()
		return utils.call_threaded(player.player.play_all, items, playing=playing_item, shuffle=self.window.player_shuffle.IsChecked())

	def on_stop(self, *args, **kwargs):
		player.player.stop()

	def on_volume_down(self, *args, **kwargs):
		player.player.volume = player.player.volume-5

	def on_volume_up(self, *args, **kwargs):
		player.player.volume = player.player.volume+5

	def on_mute(self, *args, **kwargs):
		player.player.volume = 0

	def on_shuffle(self, *args, **kwargs):
		player.player.shuffle = self.window.player_shuffle.IsChecked()

	def on_context(self, *args, **kwargs):
		item = self.window.get_item()
		if item == -1:
			return wx.Bell()
		menu = menus.contextMenu()
		widgetUtils.connect_event(menu, widgetUtils.MENU, self.on_play, menuitem=menu.play)
		widgetUtils.connect_event(menu, widgetUtils.MENU, self.on_download, menuitem=menu.download)
		self.window.PopupMenu(menu, wx.GetMousePosition())
		menu.Destroy()

	def on_download(self, *args, **kwargs):
		item = self.results[self.window.get_item()]
		f = "{0}.mp3".format(item.title)
		if item.download_url == "":
			item.get_download_url()
		path = self.window.get_destination_path(f)
		if path != None:
			log.debug("downloading %s URL to %s filename" % (item.download_url, path,))
			utils.call_threaded(utils.download_file, item.download_url, path)

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

