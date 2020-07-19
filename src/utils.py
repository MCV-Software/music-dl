# -*- coding: utf-8 -*-
import os
import requests
import threading
import logging
import types
import services
from importlib import reload
from pubsub import pub

log = logging.getLogger("utils")

def call_threaded(func, *args, **kwargs):
	#Call the given function in a daemonized thread and return the thread.
	def new_func(*a, **k):
		func(*a, **k)
	thread = threading.Thread(target=new_func, args=args, kwargs=kwargs)
	thread.daemon = True
	thread.start()
	return thread

class RepeatingTimer(threading.Thread):
	"""Call a function after a specified number of seconds, it will then repeat again after the specified number of seconds
		Note: If the function provided takes time to execute, this time is NOT taken from the next wait period

	t = RepeatingTimer(30.0, f, args=[], kwargs={})
	t.start()
	t.cancel() # stop the timer's actions
	"""

	def __init__(self, interval, function, daemon=True, *args, **kwargs):
		threading.Thread.__init__(self)
		self.daemon = daemon
		self.interval = float(interval)
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.finished = threading.Event()

	def cancel(self):
		"""Stop the timer if it hasn't finished yet"""
		log.debug("Stopping repeater for %s" % (self.function,))
		self.finished.set()
	stop = cancel

	def run(self):
		while not self.finished.is_set():
			self.finished.wait(self.interval)
			if not self.finished.is_set():  #In case someone has canceled while waiting
				try:
					self.function(*self.args, **self.kwargs)
				except:
					log.exception("Execution failed. Function: %r args: %r and kwargs: %r" % (self.function, self.args, self.kwargs))

def download_file(url, local_filename, metadata=dict()):
	log.debug("Download started: filename={0}, url={1}".format(local_filename, url))
	r = requests.get(url, stream=True)
	pub.sendMessage("change_status", status=_(u"Downloading {0}.").format(local_filename,))
	total_length = r.headers.get("content-length")
	dl = 0
	total_length = int(total_length)
	log.debug("Downloading file of {0} bytes".format(total_length))
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=512*1024): 
			if chunk: # filter out keep-alive new chunks
				dl += len(chunk)
				f.write(chunk)
				done = int(100 * dl / total_length)
				msg = _(u"Downloading {0} ({1}%).").format(os.path.basename(local_filename), done)
				pub.sendMessage("change_status", status=msg)
				pub.sendMessage("update-progress", value=done)
	pub.sendMessage("download_finished", file=os.path.basename(local_filename))
	log.debug("Download finished successfully")
	apply_metadata(local_filename, metadata)
	return local_filename

def get_services(import_all=False):
	""" Function for importing everything wich is located in the services package and has a class named interface."""
	module_type = types.ModuleType
	# first of all, import all classes for the package so we can reload everything if they have changes in config.
	_classes = [m for m in services.__dict__.values() if type(m) == module_type and hasattr(m, 'interface')]
	for cls in _classes:
		reload(cls)
	if not import_all:
		classes = [m for m in services.__dict__.values() if type(m) == module_type and hasattr(m, 'interface') and m.interface.enabled != False]
	else:
		classes = [m for m in services.__dict__.values() if type(m) == module_type and hasattr(m, 'interface')]
	return classes

def apply_metadata(local_filename, metadata):
	if local_filename.endswith(".mp3"):
		from mutagen.easyid3 import EasyID3 as metadataeditor
	elif local_filename.endswith(".flac"):
		from mutagen.flac import FLAC as metadataeditor
	elif local_filename.endswith(".m4a"):
		from mutagen.mp4 import MP4 as metadataeditor
	audio = metadataeditor(local_filename)
	if local_filename.endswith(".m4a") == False:
		for k in metadata.keys():
			audio[k] = metadata[k]
	else:
		audio["\xa9nam"] = metadata["title"]
		audio["\xa9alb"] = metadata["album"]
		audio["\xa9ART"] = metadata["artist"]
	audio.save()

def safe_filename(filename):
	allowed_symbols = ["_", ".", ",", "-", "(", ")"]
	return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ' or c in allowed_symbols]).rstrip()