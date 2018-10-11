# -*- coding: utf-8 -*-
############################################################
#    Copyright (c) 2018 Manuel cortez <manuel@manuelcortez.net>
#       
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################
import wx
import widgetUtils
import application

class reportBugDialog(widgetUtils.BaseDialog):
	def __init__(self):
		super(reportBugDialog, self).__init__(parent=None, id=wx.NewId())
		self.SetTitle(_(u"Report an error"))
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)

		summaryLabel = wx.StaticText(panel, -1, _(u"Briefly describe what happened. You will be able to thoroughly explain it later"), size=wx.DefaultSize)
		self.summary = wx.TextCtrl(panel, -1)
		dc = wx.WindowDC(self.summary)
		dc.SetFont(self.summary.GetFont())
		self.summary.SetSize(dc.GetTextExtent("a"*80))
		summaryB = wx.BoxSizer(wx.HORIZONTAL)
		summaryB.Add(summaryLabel, 0, wx.ALL, 5)
		summaryB.Add(self.summary, 0, wx.ALL, 5)
		sizer.Add(summaryB, 0, wx.ALL, 5)

		first_nameLabel = wx.StaticText(panel, -1, _(u"First Name"), size=wx.DefaultSize)
		self.first_name = wx.TextCtrl(panel, -1)
		dc = wx.WindowDC(self.first_name)
		dc.SetFont(self.first_name.GetFont())
		self.first_name.SetSize(dc.GetTextExtent("a"*40))
		first_nameB = wx.BoxSizer(wx.HORIZONTAL)
		first_nameB.Add(first_nameLabel, 0, wx.ALL, 5)
		first_nameB.Add(self.first_name, 0, wx.ALL, 5)
		sizer.Add(first_nameB, 0, wx.ALL, 5)

		last_nameLabel = wx.StaticText(panel, -1, _(u"Last Name"), size=wx.DefaultSize)
		self.last_name = wx.TextCtrl(panel, -1)
		dc = wx.WindowDC(self.last_name)
		dc.SetFont(self.last_name.GetFont())
		self.last_name.SetSize(dc.GetTextExtent("a"*40))
		last_nameB = wx.BoxSizer(wx.HORIZONTAL)
		last_nameB.Add(last_nameLabel, 0, wx.ALL, 5)
		last_nameB.Add(self.last_name, 0, wx.ALL, 5)
		sizer.Add(last_nameB, 0, wx.ALL, 5)

		emailLabel = wx.StaticText(panel, -1, _(u"Email address (Will not be public)"), size=wx.DefaultSize)
		self.email = wx.TextCtrl(panel, -1)
		dc = wx.WindowDC(self.email)
		dc.SetFont(self.email.GetFont())
		self.email.SetSize(dc.GetTextExtent("a"*30))
		emailB = wx.BoxSizer(wx.HORIZONTAL)
		emailB.Add(emailLabel, 0, wx.ALL, 5)
		emailB.Add(self.email, 0, wx.ALL, 5)
		sizer.Add(emailB, 0, wx.ALL, 5)

		descriptionLabel = wx.StaticText(panel, -1, _(u"Here, you can describe the bug in detail"), size=wx.DefaultSize)
		self.description = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
		dc = wx.WindowDC(self.description)
		dc.SetFont(self.description.GetFont())
		(x, y) = dc.GetMultiLineTextExtent("0"*2000)
		self.description.SetSize((x, y))
		descBox = wx.BoxSizer(wx.HORIZONTAL)
		descBox.Add(descriptionLabel, 0, wx.ALL, 5)
		descBox.Add(self.description, 0, wx.ALL, 5)
		sizer.Add(descBox, 0, wx.ALL, 5)
		self.agree = wx.CheckBox(panel, -1, _(u"I know that the {0} bug system will get my email address to contact me and fix the bug quickly").format(application.name,))
		self.agree.SetValue(False)
		sizer.Add(self.agree, 0, wx.ALL, 5)
		self.ok = wx.Button(panel, wx.ID_OK, _(u"Send report"))
		self.ok.SetDefault()
		cancel = wx.Button(panel, wx.ID_CANCEL, _(u"Cancel"))
		btnBox = wx.BoxSizer(wx.HORIZONTAL)
		btnBox.Add(self.ok, 0, wx.ALL, 5)
		btnBox.Add(cancel, 0, wx.ALL, 5)
		sizer.Add(btnBox, 0, wx.ALL, 5)
		panel.SetSizer(sizer)
		self.SetClientSize(sizer.CalcMin())

	def no_filled(self):
		wx.MessageDialog(self, _(u"You must fill out the following fields: first name, last name, email address and issue information."), _(u"Error"), wx.OK|wx.ICON_ERROR).ShowModal()

	def no_checkbox(self):
		wx.MessageDialog(self, _(u"You need to mark the checkbox to provide us your email address to contact you if it is necessary."), _(u"Error"), wx.ICON_ERROR).ShowModal()

	def success(self, id):
		wx.MessageDialog(self, _(u"Thanks for reporting this bug! In future versions, you may be able to find it in the changes list. You have received an email with more information regarding your report. You've reported the bug number %i") % (id), _(u"reported"), wx.OK).ShowModal()
		self.Destroy()

	def error(self):
		wx.MessageDialog(self, _(u"Something unexpected occurred while trying to report the bug. Please, try again later"), _(u"Error while reporting"), wx.ICON_ERROR|wx.OK).ShowModal()
		self.Destroy()

	def show_progress(self):
		self.progress = wx.ProgressDialog(title=_(u"Sending report..."), message=_(u"Please wait while your report is being send."), maximum=100, parent=self)
		self.progress.ShowModal()