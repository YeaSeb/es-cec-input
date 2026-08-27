#!/usr/bin/env python3

"""
Name: es-cec-input.py
Version: 1.5
Description: cec remote control for emulation station in retrosmc, with improved sony tv compatibility. Adds media controls
Author: dillbyrne, yeaseb
Homepage: https://github.com/YeaSeb/es-cec-input
Licence: GPL3

It depends on python-uinput package which contains
the library and the udev rules at
/etc/udev/rules.d/40-uinput.rules

cec-utils also needs to be installed

to run the code as a non root user
sudo addgroup uinput
sudo adduser osmc uinput

to start on boot, add to user crontab. crontab -e
@reboot hohup ./home/pi/RetroPie/scripts/es-cec-input.py
"""

import subprocess
import uinput
import sys
import time


def get_keymap():
    """Map ES supported keys to python-uinput keys"""

    keymap = {
            'left': uinput.KEY_LEFT, 'right': uinput.KEY_RIGHT,
            ': up': uinput.KEY_UP, ': down': uinput.KEY_DOWN,
            'select': uinput.KEY_ENTER, 'kp_enter': uinput.KEY_KPENTER,
            'tab': uinput.KEY_TAB, 'insert': uinput.KEY_INSERT,
            'del': uinput.KEY_DELETE, 'end': uinput.KEY_END,
            'setup': uinput.KEY_HOME, 'rshift': uinput.KEY_RIGHTSHIFT,
            'shift': uinput.KEY_LEFTSHIFT, 'rctrl': uinput.KEY_RIGHTCTRL,
            'ctrl': uinput.KEY_LEFTCTRL, 'ralt': uinput.KEY_RIGHTALT,
            'alt': uinput.KEY_LEFTALT, 'enter': uinput.KEY_SPACE,
            'root': uinput.KEY_ESC, 'blue': uinput.KEY_KPMINUS,
            'yellow': uinput.KEY_KPPLUS, 'f1': uinput.KEY_F1,
            'f2': uinput.KEY_F2, 'f3': uinput.KEY_F3,
            'f4': uinput.KEY_F4, 'f5': uinput.KEY_F5,
            'f6': uinput.KEY_F6, 'f7': uinput.KEY_F7,
            'f8': uinput.KEY_F8, 'f9': uinput.KEY_F9,
            'f10': uinput.KEY_F10, 'f11': uinput.KEY_F11,
            'f12': uinput.KEY_F12, ' 1 ': uinput.KEY_1,
            ' 2 ': uinput.KEY_2, ' 3 ': uinput.KEY_3,
            ' 4 ': uinput.KEY_4, ' 5 ': uinput.KEY_5,
            ' 6 ': uinput.KEY_6, ' 7 ': uinput.KEY_7,
            ' 8 ': uinput.KEY_8, ' 9 ': uinput.KEY_9,
            ' 0 ': uinput.KEY_0, 'l up': uinput.KEY_PAGEUP,
            'l down': uinput.KEY_PAGEDOWN, 'keypad1': uinput.KEY_KP1,
            'keypad2': uinput.KEY_KP2, 'keypad3': uinput.KEY_KP3,
            'keypad4': uinput.KEY_KP4, 'keypad5': uinput.KEY_KP5,
            'keypad6': uinput.KEY_KP6, 'keypad7': uinput.KEY_KP7,
            'keypad8': uinput.KEY_KP8, 'keypad9': uinput.KEY_KP9,
            'keypad0': uinput.KEY_KP0, ' . ': uinput.KEY_DOT,
            'capslock': uinput.KEY_CAPSLOCK, 'numlock': uinput.KEY_NUMLOCK,
            'exit': uinput.KEY_BACKSPACE, 'pause': uinput.KEY_PAUSE,
            'scrolllock': uinput.KEY_SCROLLLOCK, 'backquote': uinput.KEY_GRAVE,
            'comma': uinput.KEY_COMMA, 'minus': uinput.KEY_MINUS,
            'slash': uinput.KEY_SLASH, 'semicolon': uinput.KEY_SEMICOLON,
            'equals': uinput.KEY_EQUAL, 'backslash': uinput.KEY_BACKSLASH,
            'kp_period': uinput.KEY_KPDOT, 'kp_equals': uinput.KEY_KPEQUAL,
            ': a ': uinput.KEY_A, ': b ': uinput.KEY_B, ': c ': uinput.KEY_C,
            ': d ': uinput.KEY_D, ': e ': uinput.KEY_E, ': f ': uinput.KEY_F,
            ': g ': uinput.KEY_G, ': h ': uinput.KEY_H, ': i ': uinput.KEY_I,
            ': j ': uinput.KEY_J, ': k ': uinput.KEY_K, ': l ': uinput.KEY_L,
            ': m ': uinput.KEY_M, '(red)': uinput.KEY_N, ': o ': uinput.KEY_O,
            ': p ': uinput.KEY_P, ': q ': uinput.KEY_Q, ': r ': uinput.KEY_R,
            ': s ': uinput.KEY_S, ': t ': uinput.KEY_T, ': u ': uinput.KEY_U,
            ': v ': uinput.KEY_V, ': w ': uinput.KEY_W, ': x ': uinput.KEY_X,
            'green': uinput.KEY_Y, ': z ': uinput.KEY_Z, 'Fast forward': uinput.KEY_FORWARD,
            'rewind': uinput.KEY_REWIND, 'stop': uinput.KEY_STOP, ': forward': uinput.KEY_NEXTSONG,
            'backward': uinput.KEY_PREVIOUSSONG, 'play': uinput.KEY_PLAYPAUSE
            }

    return keymap


def generate_keylist():
    """generate a list of keys we actually need
    this will be stored in memory and will comprise of
    a,b,x,y,start,select,l,r,left,right,up,down,l2,r2,l3,r3
    keyboard corresponding values the user has chosen
    in the retroarch.cfg file"""

    keylist = []
#    key_bindings = get_key_bindings('/opt/retropie/configs/all/retroarch.cfg')
    keymap = get_keymap()
    errors = []

    for key in keymap:

        try:
            keylist.append(keymap[key])
        except KeyError as e:
            errors.append(e)

    if (len(errors) > 0):
        print('The %s keys in your retroarch.cfg are unsupported\
                by this script\n' % ', '.join(map(str, errors)))
        print('Supported keys are:\n')
        print(get_keymap().keys())
        sys.exit()

    return keylist

def register_device(keylist):
    return uinput.Device(keylist, "libcec Multimedia Remote to Keyboard")


def press_keys(line, device, keymap):
    """Emulate keyboard presses when a mapped button on the remote control
    has been pressed.

    To navigate ES, only a,b,start,select,up,down,left,and right are required
    """

    # check for key released as pressed was displaying duplicate
    # presses on the remote control used for development

    if "pressed:" in line and "current" in line:
        for binding in keymap:
            if binding in line:
                device.emit(keymap[binding], 1)
                break
        if "previous" in line or ": sub" in line:
            running_processes = subprocess.check_output(['ps', '-A'])
            running_processes = running_processes.decode('UTF-8')
            print(running_processes)
            if running_processes.find('moonl') != -1:
                device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_LEFTALT, uinput.KEY_LEFTSHIFT, uinput.KEY_Q])
                print("moonlight found")
            elif running_processes.find('retroarch') != -1:
                device.emit(uinput.KEY_1, 1)
                device.emit(uinput.KEY_ESC, 1)
                device.emit_combo([uinput.KEY_1, uinput.KEY_ESC])
                time.sleep(0.1)
                print("retroarch found")
            else:
                device.emit_combo([uinput.KEY_LEFTALT, uinput.KEY_F4])
        print(line)
    if "released" in line:
        for binding in keymap:
            if binding in line:
                device.emit(keymap[binding], 0)
                break
        if "previous" in line:
            device.emit(uinput.KEY_LEFTCTRL,0)
            device.emit(uinput.KEY_LEFTALT,0)
            device.emit(uinput.KEY_LEFTSHIFT,0)
            device.emit(uinput.KEY_Q,0)
            device.emit(uinput.KEY_LEFTALT,0)
            device.emit(uinput.KEY_F4,0)
            device.emit(uinput.KEY_LEFTALT,0)
            device.emit(uinput.KEY_F4,0)
            device.emit(uinput.KEY_ESC,0)
            device.emit(uinput.KEY_1,0)
        if 'unknown: released' in line:
            device.emit(uinput.KEY_STOP, 0) #fix for SONY TV
        print(line)


def main():
    time.sleep(1)
    keylist = generate_keylist()
    device = register_device(keylist)

    idle = True

    while True:

        # only apply key presses when emulation station is running,
        # not in emulators or kodi
        # kodi has its own built in support already

        running_processes = subprocess.check_output(['ps', '-A'])
        running_processes = running_processes.decode('UTF-8')
        if running_processes.find('mediacenter') == -1 and running_processes.find('kodi.bin') == -1:

            if idle:
                print("kodi closed or not opened, starting")
                # start cec-client to track pressed buttons on remote
                p = subprocess.Popen(
                        ["echo \"as\" | cec-client -t p -o retrosmc"], shell=True, stdout=subprocess.PIPE, bufsize=1)
                lines = iter(p.stdout.readline, b'')

                idle = False
            line = next(lines).decode('UTF-8')
            if "0f:a0:08:00:46:00:08:00:0" in line:
                print(line)
            press_keys(line, device, get_keymap())
        else:

            # stop cec-client when not in ES
            if not idle:
                print("kodi just opened, killing")
                p.kill()
                p.wait()  # avoid zombies
                running_processes = subprocess.check_output(['ps', '-A'])
                running_processes = running_processes.decode('UTF-8')
                if running_processes.find('cec-client') != -1 :
                    print("uh oh, can't close cec-client, force killing")
                    subprocess.Popen(["killall -s KILL cec-client"], shell=True , stdout=subprocess.PIPE, bufsize=1)
                idle = True

            time.sleep(1)


if __name__ == "__main__":
    main()
