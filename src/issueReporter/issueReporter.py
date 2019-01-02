# -*- coding: utf-8 -*-
############################################################
#    Copyright (c) 2018 Manuel Cortez <manuel@manuelcortez.net>
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
import platform
import requests
import widgetUtils
import application
import storage
from requests.auth import HTTPBasicAuth
from utils import call_threaded
from . import wx_ui

class reportBug(object):
	def __init__(self):
		self.dialog = wx_ui.reportBugDialog()
		widgetUtils.connect_event(self.dialog.ok, widgetUtils.BUTTON_PRESSED, self.send)
		self.dialog.get_response()

	def do_report(self, *args, **kwargs):
		r = requests.post(*args, **kwargs)
		if r.status_code > 300:
			wx.CallAfter(self.dialog.error)
		wx.CallAfter(self.dialog.progress.Destroy)
		wx.CallAfter(self.dialog.success, r.json()["data"]["issue"]["id"])

	def send(self, *args, **kwargs):
		if self.dialog.get("summary") == "" or self.dialog.get("description") == "" or self.dialog.get("first_name") == "" or self.dialog.get("last_name") == "":
			self.dialog.no_filled()
			return
		if self.dialog.get("agree") == False:
			self.dialog.no_checkbox()
			return
		title = self.dialog.get("summary")
		body = self.dialog.get("description")
		issue_type = "issue" # for now just have issue
		app_type = storage.app_type
		app_version = application.version
		reporter_name = "{first_name} {last_name}".format(first_name=self.dialog.get("first_name"), last_name=self.dialog.get("last_name"))
		reporter_contact_type = "email" # For now just email is supported in the issue reporter
		reporter_contact_handle = self.dialog.get("email")
		operating_system = platform.platform()
		json = dict(title=title, issue_type=issue_type, body=body, operating_system=operating_system, app_type=app_type, app_version=app_version, reporter_name=reporter_name, reporter_contact_handle=reporter_contact_handle, reporter_contact_type=reporter_contact_type)
		auth=HTTPBasicAuth(application.bts_name, application.bts_access_token)
		url = "{bts_url}/issue/new".format(bts_url=application.bts_url)
		call_threaded(self.do_report, url, json=json, auth=auth)
		self.dialog.show_progress()
		self.dialog.EndModal(wx.ID_OK)