=======
udiskie
=======

udiskie is a simple daemon that uses udisks_ to automatically mount removable
storage devices.

.. _udisks: http://www.freedesktop.org/wiki/Software/udisks

Original version
----------------

This is a fork of udiskie by Byron Clark (http://bitbucket.org/byronclark/udiskie)
enhanced to provide a system tray icon for removing devices, as well as
upgrading to newer APIs 

Dependencies
------------

- dbus-python_
- pygobject_
- libnotify_
- gtk3_

.. _dbus-python: http://dbus.freedesktop.org/releases/dbus-python/
.. _pygobject: http://ftp.gnome.org/pub/gnome/sources/pygobject/
.. _libnotify: http://ftp.gnome.org/pub/gnome/sources/libnotify/
.. _gtk3: http://ftp.gnome.org/pub/gnome/sources/gtk+/

Permissions
-----------

udiskie requires permission for the ``org.freedesktop.udisks.filesystem-mount``
action.  This is usually granted in sessions launched with ConsoleKit_ support.
If run outside a desktop manager with ConsoleKit_ support, the permission can be
granted using PolicyKit_ by creating a file called ``10-udiskie.pkla`` in
``/etc/polkit-1/localauthority/50-local.d`` with these contents:

.. _ConsoleKit: http://www.freedesktop.org/wiki/Software/ConsoleKit
.. _PolicyKit: http://www.freedesktop.org/wiki/Software/PolicyKit

::

    [udiskie]
    Identity=unix-group:storage
    Action=org.freedesktop.udisks.filesystem-mount
    ResultAny=yes

This configuration allows all members of the storage group to run udiskie.
