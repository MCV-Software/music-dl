# -*- coding: utf-8 -*-
import wx
import application

class contextMenu(wx.Menu):
	def __init__(self, *args, **kwargs):
		super(contextMenu, self).__init__(*args, **kwargs)
		self.play = wx.MenuItem(self, wx.NewId(), _(u"Play/Pause"))
		self.download = wx.MenuItem(self, wx.NewId(), _(u"Download"))
		if application.python_version == 3:
			self.Append(self.play)
			self.Append(self.download)
		else:
			self.AppendItem(self.play)
			self.AppendItem(self.download)
