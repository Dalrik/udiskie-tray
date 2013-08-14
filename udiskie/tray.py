#!/usr/bin/python2
from gi.repository import Gtk
import sys
import logging
import optparse
import dbus
import udiskie.device
import udiskie.notify

class RemoveTrayIcon(Gtk.StatusIcon):
    def __init__(self, bus, notify):
        Gtk.StatusIcon.__init__(self)
        self.bus = bus

        if not notify:
            self.notify = lambda *args: True
        else:
            self.notify = notify

        self.items = []

        self.log = logging.getLogger('udiskie.tray.RemoveTrayIcon')

        self.set_from_icon_name("media-eject")
        self.set_visible(True)
        self.set_tooltip_text("Unmount removable device")
        self.connect("activate", self.on_activate)
        self.connect("popup-menu", self.show_menu)

        menu = """
            <ui>
                <popup action="Menu">
                    <menuitem action="Quit" />
                </popup>
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
        self.menu = self.manager.get_widget('/Menu/Quit').props.parent

        self.log.debug('tray initialized')

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
        self.log.debug('added menu item for %s' % device.device_file())

    def _build_menu(self):
        try:
            for device in udiskie.device.get_all(self.bus):
                if device.is_handleable() and device.is_mounted():
                    self._add_menu_item(device)
        except dbus.exceptions.DBusException, dbus_err:
            self.log.error('failed to list devices: %s' % (dbus_err))

    def show_menu(self, status, button, timestamp):
        self._clear_menu()
        self._build_menu()
        self.menu.popup(None, None, self.position_menu, self, button, timestamp)
        self.log.debug('displayed menu')

    def on_activate(self, data):
        self.show_menu(None, 1, Gtk.get_current_event_time())

    def on_select_unmount(self, widget, device):
        try:
            device.unmount()
            self.log.info('unmounted device %s' % device)
        except dbus.exceptions.DBusException, dbus_err:
            self.log.error('failed to unmount device %s: %s' % (device,
                dbus_err))

        self.notify(device.device_file())

def cli(args):
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', default=False,
                      help='verbose output')
    parser.add_option('-s', '--suppress', action='store_true',
                      dest='suppress_notify', default=False,
                      help='suppress popup notifications')
    (options, args) = parser.parse_args(args)

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format='%(message)s')

    if options.suppress_notify:
        notify = None
    else:
        notify = udiskie.notify.Notify('udiskie.tray').umount

    bus = dbus.SystemBus()

    tray = RemoveTrayIcon(bus, notify)
    Gtk.main()
