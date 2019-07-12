# -*- coding: utf-8 -*-
import widgetUtils
from pubsub import pub
from . import player

class search(object):

	def __init__(self, view):
		super(search, self).__init__()
		self.name = "search"
		self.items = []
		self.view = view
		print(self.view)
		self.connect_events()

	def connect_events(self):
		widgetUtils.connect_event(self.view.list, widgetUtils.LISTBOX_ITEM_ACTIVATED, self.on_activated)
		pub.subscribe(self.search, "search")
		widgetUtils.connect_event(self.view.list, widgetUtils.KEYPRESS, self.on_keypress)

	def create_queue(self, parent):
		pass

	def search(self, text, service):
		print("Clocked me")
