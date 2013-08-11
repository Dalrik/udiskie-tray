#!/usr/bin/python2
from gi.repository import Gtk
import sys
import dbus
import udiskie.device
import notify

class RemoveTrayIcon(Gtk.StatusIcon):
    def __init__(self, bus, notify):
        Gtk.StatusIcon.__init__(self)
        self.bus = bus
        self.notify = notify
        self.items = []

        self.set_from_icon_name("media-eject")
        self.set_visible(True)
        self.set_tooltip_text("Unmount removable device")
        self.connect("activate", self.on_activate)
        self.connect("popup-menu", self.show_menu)

        menu = """
            <ui>
                <menubar name="MenuBar">
                    <menu action="Menu">
                        <separator />
                        <menuitem action="Quit" />
                    </menu>
                </menubar>
            </ui>
        """
        actions = [ 
                ('Menu', None, 'Menu'),
                ('Quit', Gtk.STOCK_QUIT,'Quit',None,'Quit udiskie-tray',self.on_quit)
                ]
        actg = Gtk.ActionGroup('Actions')
        actg.add_actions(actions)
        self.manager = Gtk.UIManager()
        self.manager.insert_action_group(actg,0)
        self.manager.add_ui_from_string(menu)
        self.menu = self.manager.get_widget('/MenuBar/Menu/Quit').props.parent

    def on_quit(self, widget=None):
        Gtk.main_quit()

    def _clear_menu(self):
        for item in self.items:
            self.menu.remove(item)
        
        self.items = []

    def _add_menu_item(self, device):
        item = Gtk.MenuItem()
        title = device.device_file() + " at " + device.mount_paths()[0]
        item.set_label(title)
        item.set_visible(True)
        item.connect("activate", self.on_select_unmount, device)
        self.menu.prepend(item)
        self.items.append(item)

    def _build_menu(self):
        for device in udiskie.device.get_all(self.bus):
            if device.is_handleable() and device.is_mounted():
                self._add_menu_item(device)

    def show_menu(self, status, button, timestamp):
        self._clear_menu()
        self._build_menu()
        self.menu.popup(None, None, None, None, button, timestamp)

    def on_activate(self, data):
        self.show_menu(None, 1, Gtk.get_current_event_time())

    def on_select_unmount(self, widget, device):
        self.notify(device.device_file())
        device.unmount()

bus = dbus.SystemBus()
notify = notify.Notifier("udiskie-tray").unmount
icon = RemoveTrayIcon(bus, notify)
Gtk.main()
