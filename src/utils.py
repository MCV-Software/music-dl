# -*- coding: utf-8 -*-
import os
import requests
import threading
import logging
import types
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

def download_file(url, local_filename):
	log.debug("Download started: filename={0}, url={1}".format(local_filename, url))
	r = requests.get(url, stream=True)
	pub.sendMessage("change_status", status=_(u"Downloading {0}.").format(local_filename,))
	total_length = r.headers.get("content-length")
	dl = 0
	total_length = int(total_length)
	log.debug("Downloading file of {0} bytes".format(total_length))
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=64): 
			if chunk: # filter out keep-alive new chunks
				dl += len(chunk)
				f.write(chunk)
				done = int(100 * dl / total_length)
				msg = _(u"Downloading {0} ({1}%).").format(os.path.basename(local_filename), done)
				pub.sendMessage("change_status", status=msg)
	pub.sendMessage("download_finished", file=os.path.basename(local_filename))
	log.debug("Download finished successfully")
	return local_filename

def get_extractors():
	""" Function for importing everything wich is located in the extractors package and has a class named interface."""
	import extractors
	module_type = types.ModuleType
	classes = [m for m in extractors.__dict__.values() if type(m) == module_type and hasattr(m, 'interface')]
	return classes#sorted(classes, key=lambda c: c.name)