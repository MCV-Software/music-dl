# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
import wx
import application
from . import utils

progress_dialog = None

def available_update_dialog(version, description):
    dialog = wx.MessageDialog(None, _("There's a new {app_name} version available. Would you like to download it now?\n\n {app_name} version: {app_version}\n\nChanges:\n{changes}").format(app_name=application.name, app_version=version, changes=description), _("New version for %s") % application.name, style=wx.YES|wx.NO|wx.ICON_WARNING)
    if dialog.ShowModal() == wx.ID_YES:
        return True
    else:
        return False

def create_progress_dialog():
    return wx.ProgressDialog(_("Download in Progress"), _("Downloading the new version..."),  parent=None, maximum=100)

def progress_callback(total_downloaded, total_size):
    wx.CallAfter(_progress_callback, total_downloaded, total_size)

def _progress_callback(total_downloaded, total_size):
    global progress_dialog
    if progress_dialog == None:
        progress_dialog = create_progress_dialog()
        progress_dialog.Show()
    if total_downloaded == total_size:
        progress_dialog.Destroy()
    else:
        progress_dialog.Update((total_downloaded*100)/total_size, _("Updating... {total_transferred} of {total_size}").format(total_transferred=utils.convert_bytes(total_downloaded), total_size=utils.convert_bytes(total_size)))

def update_finished():
    return wx.MessageDialog(None, _("The update has been downloaded and installed successfully. Press OK to continue."), _("Done!")).ShowModal()
