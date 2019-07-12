# -*- coding: utf-8 -*-
import wx
from pubsub import pub

class searchPanel(wx.Panel):

	def __init__(self, services=[], *args, **kwargs):
		super(searchPanel, self).__init__(*args, **kwargs)
		sizer = wx.BoxSizer(wx.VERTICAL)
		lbl2 = wx.StaticText(self, wx.NewId(), _("search"))
		self.text = wx.TextCtrl(self, wx.NewId())
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(lbl2, 0, wx.GROW)
		box.Add(self.text, 1, wx.GROW)
		box.Add(wx.StaticText(self, wx.NewId(), _(u"Search in")), 0, wx.GROW)
		self.service = wx.ComboBox(self, wx.NewId(), choices=services, value=services[0], style=wx.CB_READONLY)
		box.Add(self.service, 1, wx.GROW)
		self.search = wx.Button(self, wx.NewId(), _(u"Search"))
		self.search.SetDefault()
		self.search.Bind(wx.EVT_BUTTON, self.on_search)
		box.Add(self.search, 0, wx.GROW)
		sizer.Add(box, 0, wx.GROW)
		lbl = wx.StaticText(self, wx.NewId(), _(u"Results"))
		self.list = wx.ListBox(self, wx.NewId())
		sizer.Add(lbl, 0, wx.GROW)
		sizer.Add(self.list, 1, wx.GROW)
		self.SetSizer(sizer)

	def get_text(self):
		t = self.text.GetValue()
		self.text.ChangeValue("")
		return t

	def get_item(self):
		return self.list.GetSelection()

	def on_search(self, event, *args, **kwargs):
		text = self.get_text()
		service = self.service.GetValue()
		pub.sendMessage("search", service=service, text=text)
		event.Skip()