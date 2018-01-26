# -*- coding: utf-8 -*-
import wx
import application
import widgetUtils

class mainWindow(wx.Frame):
	def makeMenu(self):
		mb = wx.MenuBar()
		app_ = wx.Menu()
		mb.Append(app_, _(u"Application"))
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
		mb.Append(player, _(u"Player"))
		mb.Append(help_, _(u"Help"))
		self.SetMenuBar(mb)

	def __init__(self):
		super(mainWindow, self).__init__(parent=None, id=wx.NewId(), title=application.name)
		self.Maximize(True)
		self.makeMenu()
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sb = self.CreateStatusBar()
		lbl2 = wx.StaticText(self.panel, wx.NewId(), _(u"search"))
		self.text = wx.TextCtrl(self.panel, wx.NewId())
		self.search = wx.Button(self.panel, wx.NewId(), _("Search"))
		self.search.SetDefault()
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(lbl2, 0, wx.ALL, 20)
		box.Add(self.text, 0, wx.ALL, 5)
		box.Add(self.search, 0, wx.ALL, 5)
		self.sizer.Add(box, 0, wx.ALL, 5)
		lbl = wx.StaticText(self.panel, wx.NewId(), _("Results"))
		self.list = wx.ListBox(self.panel, wx.NewId())
		self.sizer.Add(lbl, 0, wx.ALL, 5)
		self.sizer.Add(self.list, 1, wx.EXPAND, 5)
		self.panel.SetSizer(self.sizer)
		self.SetClientSize(self.sizer.CalcMin())
		self.Layout()
		self.SetSize(self.GetBestSize())

	def change_status(self, status):
		self.sb.SetStatusText(status)

	def about_dialog(self, *args, **kwargs):
		info = wx.AboutDialogInfo()
		info.SetName(application.name)
		info.SetVersion(application.version)
		info.SetDescription(application.description)
		info.SetCopyright(application.copyright)
		info.SetTranslators(application.translators)
#  info.SetLicence(application.licence)
		info.AddDeveloper(application.author)
		wx.AboutBox(info)

	def get_text(self):
		t = self.text.GetValue()
		self.text.ChangeValue("")
		return t

	def get_item(self):
		return self.list.GetSelection()

	def get_destination_path(self, filename):
		saveFileDialog = wx.FileDialog(self, _(u"Save this file"), "", filename, _(u"Audio Files(*.mp3)|*.mp3"), wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if saveFileDialog.ShowModal() == wx.ID_OK:
			return saveFileDialog.GetPath()
		saveFileDialog.Destroy()