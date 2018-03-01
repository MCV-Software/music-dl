# -*- coding: utf-8 -*-
""" main controller for MusicDL"""
import webbrowser
import wx
import logging
import widgetUtils
import utils
import application
from pubsub import pub
from wxUI import mainWindow, menus
from extractors import zaycev, youtube, vk
from update import updater
from . import player

log = logging.getLogger("controller.main")

class Controller(object):

	def __init__(self):
		super(Controller, self).__init__()
		log.debug("Starting main controller...")
		# Setting up the player object
		player.setup()
		# Get main window
		self.window = mainWindow.mainWindow()
		log.debug("Main window created")
		self.window.change_status(_("Ready"))
		# Here we will save results for searches as song objects.
		self.results = []
		self.connect_events()
		self.timer = wx.Timer(self.window)
		self.window.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
		self.timer.Start(75)
		self.window.vol_slider.SetValue(player.player.volume)
		# Shows window.
		utils.call_threaded(updater.do_update)
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
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.window.about_dialog, menuitem=self.window.about)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_check_for_updates, menuitem=self.window.check_for_updates)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_visit_changelog, menuitem=self.window.changelog)
		widgetUtils.connect_event(self.window, widgetUtils.MENU, self.on_visit_website, menuitem=self.window.website)
		widgetUtils.connect_event(self.window.previous, widgetUtils.BUTTON_PRESSED, self.on_previous)
		widgetUtils.connect_event(self.window.play, widgetUtils.BUTTON_PRESSED, self.on_play_pause)
		widgetUtils.connect_event(self.window.stop, widgetUtils.BUTTON_PRESSED, self.on_stop)
		widgetUtils.connect_event(self.window.next, widgetUtils.BUTTON_PRESSED, self.on_next)
		self.window.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_set_volume, self.window.vol_slider)
		self.window.Bind(wx.EVT_COMMAND_SCROLL_CHANGED, self.on_set_volume, self.window.vol_slider)
		self.window.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_time_change, self.window.time_slider)
		self.window.Bind(wx.EVT_COMMAND_SCROLL_CHANGED, self.on_time_change, self.window.time_slider)
		self.window.list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_play)
		self.window.list.Bind(wx.EVT_CONTEXT_MENU, self.on_context)
		self.window.Bind(wx.EVT_CLOSE, self.on_close)
		pub.subscribe(self.change_status, "change_status")
		pub.subscribe(self.on_download_finished, "download_finished")

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
		elif ev.GetKeyCode() == wx.WXK_LEFT and ev.ShiftDown():
			position = player.player.player.get_time()
			if position > 5000:
				player.player.player.set_time(position-5000)
			else:
				player.player.player.set_time(0)
		elif ev.GetKeyCode() == wx.WXK_RIGHT and ev.ShiftDown():
			position = player.player.player.get_time()
			player.player.player.set_time(position+5000)

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
			self.window.play.SetLabel(_("Play"))
			return player.player.pause()
		else:
			self.window.play.SetLabel(_("Pause"))
			return player.player.player.play()

	def on_next(self, *args, **kwargs):
		return utils.call_threaded(player.player.next)

	def on_previous(self, *args, **kwargs):
		return utils.call_threaded(player.player.previous)

	def on_play(self, *args, **kwargs):
		items = self.results[::]
		playing_item = self.window.get_item()
		self.window.play.SetLabel(_("Pause"))
		return utils.call_threaded(player.player.play_all, items, playing=playing_item, shuffle=self.window.player_shuffle.IsChecked())

	def on_stop(self, *args, **kwargs):
		player.player.stop()
		self.window.play.SetLabel(_("Play"))

	def on_volume_down(self, *args, **kwargs):
		self.window.vol_slider.SetValue(self.window.vol_slider.GetValue()-5)
		self.on_set_volume()

	def on_volume_up(self, *args, **kwargs):
		self.window.vol_slider.SetValue(self.window.vol_slider.GetValue()+5)
		self.on_set_volume()

	def on_mute(self, *args, **kwargs):
		self.window.vol_slider.SetValue(0)
		self.on_set_volume()

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
			if self.extractor.needs_transcode == True: # Send download to vlc based transcoder
				utils.call_threaded(player.player.transcode_audio, item, path)
			else:
				log.debug("downloading %s URL to %s filename" % (item.download_url, path,))
				utils.call_threaded(utils.download_file, item.download_url, path)

	def on_set_volume(self, *args, **kwargs):
		volume = self.window.vol_slider.GetValue()
		player.player.volume = volume

	def on_time_change(self, event, *args, **kwargs):
		p = event.GetPosition()
		player.player.player.set_position(p/100.0)
		event.Skip()

	def on_timer(self, *args, **kwargs):
		if not self.window.time_slider.HasFocus():
			progress = player.player.player.get_position()*100
			self.window.time_slider.SetValue(progress)

	def on_close(self, event):
		self.timer.Stop()
		pub.unsubscribe(self.on_download_finished, "download_finished")
		event.Skip()
		widgetUtils.exit_application()

	def change_status(self, status):
		""" Function used for changing the status bar from outside the main controller module."""
		self.window.change_status("{0} {1}".format(status, self.get_status_info()))

	def on_visit_website(self, *args, **kwargs):
		webbrowser.open_new_tab(application.url)

	def on_visit_changelog(self, *args, **kwargs):
		webbrowser.open_new_tab(application.url+"/news")

	def on_check_for_updates(self, *args, **kwargs):
		utils.call_threaded(updater.do_update)

	def on_download_finished(self, file):
		title = "MusicDL"
		msg = _("File downloaded: {0}").format(file,)
		self.window.notify(title, msg)

	# real functions. These functions really are doing the work.
	def search(self, *args, **kwargs):
		text = self.window.get_text()
		if text == "":
			return
		extractor = self.window.extractor.GetValue()
		if extractor == "youtube":
			self.extractor = youtube.interface()
		elif extractor == "vk":
			self.extractor = vk.interface()
		elif extractor == "zaycev.net":
			self.extractor = zaycev.interface()
		elif extractor == "":
			return
		self.window.list.Clear()
		self.change_status(_("Searching {0}... ").format(text,))
		self.extractor.search(text)
		self.results = self.extractor.results
		for i in self.results:
			self.window.list.Append(i.format_track())
		if len(self.results) == 0:
			self.change_status(_("No results found. "))
		else:
			self.change_status("")
			wx.CallAfter(self.window.list.SetFocus)