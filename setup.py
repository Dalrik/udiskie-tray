from distutils.core import setup

setup(
    name='udiskie-tray',
    version='0.1.0',
    description='Removable disk automounter for udisks',
    author='Ian Thompson',
    author_email='dalrik370@gmail.com',
    url='http://github.com/Dalrik/udiskie-tray',
    license='MIT',
    packages=[
        'udiskie',
    ],
    scripts=[
        'bin/udiskie',
        'bin/udiskie-umount',
        'bin/udiskie-tray',
    ],
)
