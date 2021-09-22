# -*- coding: utf-8 -*-
import config
from utils import get_services
from wxUI.configuration import configurationDialog
from . import player

class configuration(object):

    def __init__(self):
        self.view = configurationDialog(_("Settings"))
        self.create_config()
        self.view.get_response()
        self.save()

    def create_config(self):
        self.output_devices = player.player.get_output_devices()
        self.view.create_general(output_devices=[i for i in self.output_devices])
        current_output_device = config.app["main"]["output_device"]
        for i in self.output_devices:
            # here we must compare against the str version of the vlc's device identifier.
            if i == current_output_device:
                self.view.set_value("general", "output_device", i)
                break
        self.view.realize()
        extractors = get_services(import_all=True)
        for i in extractors:
            if hasattr(i, "settings"):
                panel = getattr(i, "settings")(self.view.notebook)
                self.view.notebook.InsertSubPage(1, panel, panel.name)
                panel.load()
                if hasattr(panel, "on_enabled"):
                    panel.on_enabled()


    def save(self):
        selected_output_device = self.view.get_value("general", "output_device")
        if config.app["main"]["output_device"] != selected_output_device:
            config.app["main"]["output_device"] = selected_output_device
            player.player.set_output_device(config.app["main"]["output_device"])
        for i in range(0, self.view.notebook.GetPageCount()):
            page = self.view.notebook.GetPage(i)
            if hasattr(page, "save"):
                page.save()
        config.app.write()
