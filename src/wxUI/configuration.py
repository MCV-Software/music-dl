# -*- coding: utf-8 -*-
import wx
import widgetUtils

class general(wx.Panel, widgetUtils.BaseDialog):
	def __init__(self, panel):
		super(general, self).__init__(panel)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)

class configurationDialog(widgetUtils.BaseDialog):

	def __init__(self, title):
		super(configurationDialog, self).__init__(None, -1, title=title)
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.notebook = wx.Treebook(self.panel)

	def create_general(self):
		self.general = general(self.notebook)
		self.notebook.AddPage(self.general, _("General"))
		self.general.SetFocus()

	def realize(self):
		self.sizer.Add(self.notebook, 0, wx.ALL, 5)
		ok_cancel_box = wx.BoxSizer(wx.HORIZONTAL)
		ok = wx.Button(self.panel, wx.ID_OK, _("Save"))
		ok.SetDefault()
		cancel = wx.Button(self.panel, wx.ID_CANCEL, _("Close"))
		self.SetEscapeId(cancel.GetId())
		ok_cancel_box.Add(ok, 0, wx.ALL, 5)
		ok_cancel_box.Add(cancel, 0, wx.ALL, 5)
		self.sizer.Add(ok_cancel_box, 0, wx.ALL, 5)
		self.panel.SetSizer(self.sizer)
		self.SetClientSize(self.sizer.CalcMin())

	def get_value(self, panel, key):
		p = getattr(self, panel)
		return getattr(p, key).GetValue()

	def set_value(self, panel, key, value):
		p = getattr(self, panel)
		control = getattr(p, key)
		getattr(control, "SetValue")(value)