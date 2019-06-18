# -*- coding: utf-8 -*-
import config
from utils import get_extractors
from wxUI.configuration import configurationDialog

class configuration(object):

	def __init__(self):
		self.view = configurationDialog(_("Settings"))
		self.create_config()
		self.view.get_response()
		self.save()

	def create_config(self):
		self.view.create_general()
		extractors = get_extractors()
		for i in extractors:
			print(i)
			if hasattr(i, "settings"):
				panel = getattr(i, "settings")(self.view.notebook)
				self.view.notebook.AddPage(panel, panel.name)
				panel.load()
				if hasattr(panel, "on_enabled"):
					panel.on_enabled()
		self.view.realize()

	def save(self):
		for i in range(0, self.view.notebook.GetPageCount()):
			page = self.view.notebook.GetPage(i)
			if hasattr(page, "save"):
				page.save()
		config.app.write()