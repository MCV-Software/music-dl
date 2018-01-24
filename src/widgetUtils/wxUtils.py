import wx

toolkit = "wx"

### Code responses for WX dialogs.

# this is when an user presses OK on a dialogue.
OK = wx.ID_OK

# This is when an user presses cancel on a dialogue.
CANCEL = wx.ID_CANCEL

# This is when an user closes the dialogue or an id to create the close button.
CLOSE = wx.ID_CLOSE

# The response for a "yes" Button pressed on a dialogue.
YES = wx.ID_YES

# This is when the user presses No on a default dialogue.
NO = wx.ID_NO

###events

# This is raised when the application must be closed.
CLOSE_EVENT = wx.EVT_CLOSE

# This is activated when a button  is pressed.
BUTTON_PRESSED = wx.EVT_BUTTON

# This is raised when a checkbox changes its status.
CHECKBOX = wx.EVT_CHECKBOX

# This is activated when an user enter text on an edit box.
ENTERED_TEXT = wx.EVT_TEXT

# This is raised when a user activates a menu.
MENU = wx.EVT_MENU

# This is raised when a user presses any key in the control.
KEYPRESS = wx.EVT_CHAR_HOOK

# This is raised when a user releases a key in the control.
KEYUP = wx.EVT_KEY_UP

# This happens when a notebook tab is changed, It is used in Treebooks too.
NOTEBOOK_PAGE_CHANGED = wx.EVT_TREEBOOK_PAGE_CHANGED

# This happens when a radiobutton group changes its status.
RADIOBUTTON = wx.EVT_RADIOBUTTON

# Taskbar mouse clicks.
#TASKBAR_RIGHT_CLICK = wx.EVT_TASKBAR_RIGHT_DOWN
#TASKBAR_LEFT_CLICK = wx.EVT_TASKBAR_LEFT_DOWN
LISTBOX_CHANGED = wx.EVT_LISTBOX
LISTBOX_ITEM_ACTIVATED = wx.EVT_LIST_ITEM_ACTIVATED

def exit_application():
	""" Closes the current window cleanly. """
	wx.GetApp().ExitMainLoop()

def connect_event(parent, event, func, menuitem=None, *args, **kwargs):
	""" Connects an event to a function.
	parent wx.window: The widget that will listen for the event.
	event widgetUtils.event: The event that will be listened for the parent. The event should be one of the widgetUtils events.
	function func: The function that will be connected to the event."""
	if menuitem == None:
		return getattr(parent, "Bind")(event, func, *args, **kwargs)
	else:
		return getattr(parent, "Bind")(event, func, menuitem, *args, **kwargs)

def connectExitFunction(exitFunction):
	""" This connect the events in WX when an user is  turning off the machine."""
	wx.GetApp().Bind(wx.EVT_QUERY_END_SESSION, exitFunction)
	wx.GetApp().Bind(wx.EVT_END_SESSION, exitFunction)

class BaseDialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		super(BaseDialog, self).__init__(*args, **kwargs)

	def get_response(self):
		return self.ShowModal()

	def get(self, control):
		if hasattr(self, control):
			control = getattr(self, control)
			if hasattr(control, "GetValue"): return getattr(control, "GetValue")()
			elif hasattr(control, "GetLabel"): return getattr(control, "GetLabel")()
			else: return -1
		else: return 0

	def set(self, control, text):
		if hasattr(self, control):
			control = getattr(self, control)
			if hasattr(control, "SetValue"): return getattr(control, "SetValue")(text)
			elif hasattr(control, "SetLabel"): return getattr(control, "SetLabel")(text)
			elif hasattr(control, "ChangeValue"): return getattr(control, "ChangeValue")(text)
			else: return -1
		else: return 0

	def destroy(self):
		self.Destroy()

	def set_title(self, title):
		self.SetTitle(title)

	def get_title(self):
		return self.GetTitle()

	def enable(self, control):
		getattr(self, control).Enable(True)

	def disable(self, control):
		getattr(self, control).Enable(False)

class mainLoopObject(wx.App):

	def __init__(self):
		self.app = wx.App()
#		self.lc = wx.Locale()
#		lang=languageHandler.getLanguage()
#		wxLang=self.lc.FindLanguageInfo(lang)
#		if not wxLang and '_' in lang:
#			wxLang=self.lc.FindLanguageInfo(lang.split('_')[0])
#		if hasattr(sys,'frozen'):
#			self.lc.AddCatalogLookupPathPrefix(paths.app_path("locales"))
#		if wxLang:
#			self.lc.Init(wxLang.Language)

	def run(self):
		self.app.MainLoop()

class list(object):
 def __init__(self, parent, *columns, **listArguments):
  self.columns = columns
  self.listArguments = listArguments
  self.create_list(parent)

 def set_windows_size(self, column, characters_max):
  self.list.SetColumnWidth(column, characters_max*2)

 def set_size(self):
  self.list.SetSize((self.list.GetBestSize()[0], 1000))

 def create_list(self, parent):
  self.list = wx.ListCtrl(parent, -1, **self.listArguments)
  for i in range(0, len(self.columns)):
   self.list.InsertColumn(i, u"%s" % (self.columns[i]))

 def insert_item(self, reversed, *item):
  """ Inserts an item on the list."""
  if reversed == False: items = self.list.GetItemCount()
  else: items = 0
  self.list.InsertItem(items, item[0])
  for i in range(1, len(self.columns)):
   self.list.SetItem(items, i, item[i])

 def remove_item(self, pos):
  """ Deletes an item from the list."""
  if pos > 0: self.list.Focus(pos-1)
  self.list.DeleteItem(pos)

 def clear(self):
  self.list.DeleteAllItems()

 def get_selected(self):
  return self.list.GetFocusedItem()

 def select_item(self, pos):
  self.list.Focus(pos)

 def get_count(self):
  selected = self.list.GetItemCount()
  if selected == -1:
   return 0
  else:
   return selected
