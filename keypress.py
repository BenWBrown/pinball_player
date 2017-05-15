"""
file: keypress.py
description: module that defines abstractions for the keys the player can press
"""

DEFAULT_TAP_TIME = 0.1

from threading import Timer
import autopy
"""
install autopy using:
$ git clone https://github.com/octalmage/autopy.git
$ cd autopy
$ python setup.py build
$ python setup.py install
"""

pressed_keys = {}

def untoggle(key):
    autopy.key.toggle(key, False)
    pressed_keys[key] = False

def tap(key, tap_time=DEFAULT_TAP_TIME):
    try:
        pressed_keys[key]
    except KeyError:
        pressed_keys[key] = False
    if not pressed_keys[key]:
        pressed_keys[key] = True
        autopy.key.toggle(key, True)
        t = Timer(tap_time, untoggle, [key])
        t.start()

if __name__ == '__main__': #do some simple tests
    import time
    time.sleep(1)
    tap('z')
    time.sleep(1)
    tap('x')
    time.sleep(1)
    tap('.')
    time.sleep(1)
    tap('/')
    time.sleep(1)
    tap(' ')
    time.sleep(1)
