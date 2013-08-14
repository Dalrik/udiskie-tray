from gi.repository import Notify as GNotify
from gi.repository import Gio

class Notify:
    def __init__(self, name):
        GNotify.init(name)

    def mount(self, device, path):
        try:
            GNotify.Notification.new('Device mounted',
                                  '%s mounted on %s' % (device, path),
                                  'drive-removable-media').show()
        except Gio.Error:
            pass

    def umount(self, device):
        try:
            GNotify.Notification.new('Device unmounted',
                                  '%s unmounted' % (device,),
                                  'drive-removable-media').show()
        except Gio.Error:
            pass
