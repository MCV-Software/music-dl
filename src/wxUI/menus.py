# -*- coding: utf-8 -*-
import wx

class contextMenu(wx.Menu):
	def __init__(self, *args, **kwargs):
		super(contextMenu, self).__init__(*args, **kwargs)
		self.play = wx.MenuItem(self, wx.NewId(), _("Play/Pause"))
		self.Append(self.play)
		self.download = wx.MenuItem(self, wx.NewId(), _("Download"))
		self.Append(self.download)
