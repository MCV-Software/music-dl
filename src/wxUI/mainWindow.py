# -*- coding: utf-8 -*-
from __future__ import unicode_literals    # at top of module
import wx
try:
	import wx.adv
except ImportError:
	pass
import application
import widgetUtils
from .search import searchPanel

class mainWindow(wx.Frame):
	def makeMenu(self):
		mb = wx.MenuBar()
		app_ = wx.Menu()
		self.settings = app_.Append(wx.NewId(), _("Settings"))
		mb.Append(app_, _("Application"))
		player = wx.Menu()
		self.player_play = player.Append(wx.NewId(), _(u"Play"))
		self.player_stop = player.Append(wx.NewId(), _(u"Stop"))
		self.player_previous = player.Append(wx.NewId(), _(u"Previous"))
		self.player_next = player.Append(wx.NewId(), _(u"Next"))
		self.player_shuffle = player.AppendCheckItem(wx.NewId(), _(u"Shuffle"))
		self.player_volume_down = player.Append(wx.NewId(), _(u"Volume down"))
		self.player_volume_up = player.Append(wx.NewId(), _(u"Volume up"))
		self.player_mute = player.Append(wx.NewId(), _(u"Mute"))
		help_ = wx.Menu()
		self.about = help_.Append(wx.NewId(), _(u"About {0}").format(application.name,))
		self.check_for_updates = help_.Append(wx.NewId(), _(u"Check for updates"))
		self.changelog = help_.Append(wx.NewId(), _(u"What's new in this version?"))
		self.website = help_.Append(wx.NewId(), _(u"Visit website"))
		self.report = help_.Append(wx.NewId(), _(u"Report an error"))
		mb.Append(player, _(u"Player"))
		mb.Append(help_, _(u"Help"))
		self.SetMenuBar(mb)

	def __init__(self, extractors=[]):
		super(mainWindow, self).__init__(parent=None, id=wx.NewId(), title=application.name)
		self.Maximize(True)
		self.makeMenu()
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sb = self.CreateStatusBar()
		self.tb = wx.Treebook(self.panel, -1)
		search = searchPanel(extractors, parent=self.tb)
		self.add_buffer(search, _("Search"))
		self.sizer.Add(self.tb, 1, wx.ALL|wx.EXPAND, 5)
		box1 = wx.BoxSizer(wx.HORIZONTAL)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		box1.Add(wx.StaticText(self.panel, wx.NewId(), _(u"Position")), 0, wx.GROW)
		self.time_slider = wx.Slider(self.panel, -1)
		box1.Add(self.time_slider, 1, wx.GROW)
		box1.Add(wx.StaticText(self.panel, wx.NewId(), _(u"Volume")), 0, wx.GROW)
		self.vol_slider = wx.Slider(self.panel, -1, 0, 0, 100, size=(100, -1))
		box1.Add(self.vol_slider, 1, wx.GROW)
		self.previous = wx.Button(self.panel, wx.NewId(), _(u"Previous"))
		self.play  = wx.Button(self.panel, wx.NewId(), _(u"Play"))
		self.stop   = wx.Button(self.panel, wx.NewId(), _(u"Stop"))
		self.next = wx.Button(self.panel, wx.NewId(), _(u"Next"))
		box2.Add(self.previous)
		box2.Add(self.play, flag=wx.RIGHT, border=5)
		box2.Add(self.stop)
		box2.Add(self.next)
		self.sizer.Add(box1, 0, wx.GROW)
		self.sizer.Add(box2, 1, wx.GROW)
		self.progressbar = wx.Gauge(self.panel, wx.NewId(), range=100, style=wx.GA_HORIZONTAL)
		self.sizer.Add(self.progressbar, 0, wx.ALL, 5)
		self.panel.SetSizerAndFit(self.sizer)

	def change_status(self, status):
		self.sb.SetStatusText(status)

	def about_dialog(self, *args, **kwargs):
		try:
			info = wx.adv.AboutDialogInfo()
		except:
			info = wx.AboutDialogInfo()
		info.SetName(application.name)
		info.SetVersion(application.version)
		info.SetDescription(application.description)
		info.SetCopyright(application.copyright)
		info.SetWebSite(application.url)
		info.SetTranslators(application.translators)
#  info.SetLicence(application.licence)
		info.AddDeveloper(application.author)
		try:
			wx.adv.AboutBox(info)
		except:
			wx.AboutBox(info)

	def get_destination_path(self, filename):
		saveFileDialog = wx.FileDialog(self, _(u"Save this file"), "", filename, _(u"Audio Files(*.mp3)|*.mp3"), wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if saveFileDialog.ShowModal() == wx.ID_OK:
			return saveFileDialog.GetPath()
		saveFileDialog.Destroy()

	def notify(self, title, text):
		try:
			self.notification = wx.adv.NotificationMessage(title, text, parent=self)
		except AttributeError:
			self.notification = wx.NotificationMessage(title, text)
		self.notification.Show()

	def get_buffer_count(self):
		return self.tb.GetPageCount()

	def add_buffer(self, buffer, name):
		self.tb.AddPage(buffer, name)

	def insert_buffer(self, buffer, name, pos):
		return self.tb.InsertSubPage(pos, buffer, name)

	def search(self, name_):
		for i in range(0, self.tb.GetPageCount()):
			if self.tb.GetPage(i).name == name_: return i

	def get_current_buffer(self):
		return self.tb.GetCurrentPage()

	def get_current_buffer_pos(self):
		return self.tb.GetSelection()

	def get_buffer(self, pos):
		return self.tb.GetPage(pos)

	def change_buffer(self, position):
		self.tb.ChangeSelection(position)

	def get_buffer_text(self, pos=None):
		if pos == None:
			pos = self.tb.GetSelection()
		return self.tb.GetPageText(pos)

	def get_buffer_by_id(self, id):
		return self.tb.FindWindowById(id)

	def advance_selection(self, forward):
		self.tb.AdvanceSelection(forward)

	def remove_buffer(self, pos):
		self.tb.DeletePage(pos)

	def remove_buffer_from_position(self, pos):
		return self.tb.RemovePage(pos)
