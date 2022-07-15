#!/usr/bin/env python3

# This is essentially OpenTCLRemote stripped down to bare essentials for the sake of efficiency and simplicity

# HDMI-CEC implementation between AppleTV and my TCL TV is broken for shutdown, need alternative
# I'm turning off TV with this script via Homekit/Homebridge integration, separate script wakes TV via AppleTV

# Should work with all TCL / Thomson TVs with SmartTV2 OS (AKA sitatvservice)

# TR_KEY_POWER is not listed but works as shutdown command

from socket import (socket, AF_INET, SOCK_STREAM)
import sys

args = sys.argv

keymap = {
    "1": "TR_KEY_1",
    "2": "TR_KEY_2",
    "3": "TR_KEY_3",
    "4": "TR_KEY_4",
    "5": "TR_KEY_5",
    "6": "TR_KEY_6",
    "7": "TR_KEY_7",
    "8": "TR_KEY_8",
    "9": "TR_KEY_9",
    "eco": "TR_KEY_ECO",
    "source": "TR_KEY_SOURCE",
    "vol_up": "TR_KEY_VOL_UP",
    "mute": "TR_KEY_MUTE",
    "ch_up": "TR_KEY_CH_UP",
    "vol_down": "TR_KEY_VOL_DOWN",
    "info": "TR_KEY_INFOWINDOW",
    "ch_down": "TR_KEY_CH_DOWN",
    "option": "TR_KEY_OPTION",
    "smart": "TR_KEY_SMARTTV",
    "guide": "TR_KEY_GUIDE",
    "menu": "TR_KEY_MAINMENU",
    "up": "TR_KEY_UP",
    "ok": "TR_KEY_OK",
    "left": "TR_KEY_LEFT",
    "right": "TR_KEY_RIGHT",
    "back": "TR_KEY_BACK",
    "down": "TR_KEY_DOWN",
    "exit": "TR_KEY_EXIT",
    "zoom_down": "TR_KEY_ZOOM_DOWN",
    "zoom_up": "TR_KEY_ZOOM_UP",
    "list": "TR_KEY_LIST",
    "sleep": "TR_KEY_SLEEP",
    "pre_ch": "TR_KEY_PRE_CH",
    "favorite": "TR_KEY_FAVORITE",
    "record": "TR_KEY_REC",
    "red": "TR_KEY_RED",
    "green": "TR_KEY_GREEN",
    "yellow": "TR_KEY_YELLOW",
    "blue": "TR_KEY_BLUE",
    "power": "TR_KEY_POWER"
}

try:
    tcl_command = keymap[args[1]]
except Exception as zonk:
    print("No key specified, defaulting to power off.")
    tcl_command = "TR_KEY_VOL_POWER"

try:
    tcl_host = args[2]
except Exception as zonk:
    print("No host specified, defaulting to predefined host.")
    tcl_host = "192.168.1.198"

def create_action(key_code):
    """Given a key_code, the create_action function generates the XML string
       in the correct format for the TV set.
    """
    message = ('<?xml version="1.0" encoding="utf-8"?>'
               '<root>'
               '<action name="setKey" eventAction="TR_DOWN" keyCode="{}" />'
               '</root>'
              )

    return message.format(key_code)

class RemoteController:
    """The RemoteController class handles communications between this program
       and the TV set on a local network.
    """
    def __init__(self, host):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((host, 4123))

    def press_key(self, key_code):
        """Emulates a key press by sending a message to the TV set.
        """
        # Messages will always be smaller than buffer size
        self.sock.send(create_action(key_code).encode('utf-8'))
        self.sock.recv(2048)

# It is possible to search for all TVs using UPNP and send command to the first one available
# This process takes time though and I want command to be sent instantly, hence manually added IP

try:
    print(f"Sending {tcl_command} to {tcl_host}.")
    remote_controller = RemoteController(tcl_host)
    remote_controller.press_key(tcl_command)

except Exception as zonk:
    print(f"{zonk}")