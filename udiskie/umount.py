import warnings
warnings.filterwarnings("ignore", ".*could not open display.*", Warning)
warnings.filterwarnings("ignore", ".*g_object_unref.*", Warning)

import logging
import optparse
import os

import dbus

import udiskie.device
import udiskie.notify

def unmount_device(device, notify):
    """Unmount a Device.

    Checks to make sure the device is unmountable and then unmounts."""

    logger = logging.getLogger('udiskie.umount.unmount_device')
    if device.is_handleable() and device.is_mounted():
        try:
            device.unmount()
            logger.info('unmounted device %s' % (device,))
        except dbus.exceptions.DBusException, dbus_err:
            logger.error('failed to unmount device %s: %s' % (device,
                                                              dbus_err))
            return

        notify(device.device_file())
    else:
        logger.debug('skipping unhandled device %s' % (device,))

def unmount(path, notify):
    """Unmount a filesystem

    The filesystem must match the criteria for a filesystem mountable by
    udiskie.  path is either the physical device node (e.g. /dev/sdb1) or the
    mount point (e.g. /media/Foo)."""

    logger = logging.getLogger('udiskie.umount.unmount')
    bus = dbus.SystemBus()
    for device in udiskie.device.get_all(bus):
        if path in device.mount_paths() or path == device.device_file():
            logger.debug('found device owning "%s": "%s"' % (path, device))
            unmount_device(device, notify)

def unmount_all(notify):
    """Unmount all filesystems handleable by udiskie."""

    bus = dbus.SystemBus()
    for device in udiskie.device.get_all(bus):
        unmount_device(device, notify)

def cli(args):
    logger = logging.getLogger('udiskie.umount.cli')
    parser = optparse.OptionParser()
    parser.add_option('-a', '--all', action='store_true',
                      dest='all', default=False,
                      help='all devices')
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
        notify = lambda *args: True
    else:
        notify = udiskie.notify.Notify('udiskie.umount').umount

    if options.all:
        unmount_all(notify)
    else:
        if len(args) == 0:
            logger.warn('No devices provided for unmount')
            return 1

        for path in args:
            unmount(os.path.normpath(path), notify)
