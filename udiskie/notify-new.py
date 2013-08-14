from gi.repository import Notify

class Notifier(object):
    def __init__(self, name):
        Notify.init(name)

    def unmount(self, device):
        Notify.Notification.new("Device unmounted", "%s unmounted" % (device),
                "dialog-information").show()

