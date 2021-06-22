#!/usr/bin/env python3

# This is essentially OpenTCLRemote stripped down to bare essentials for the sake of efficiency and simplicity

# HDMI-CEC implementation between AppleTV and my TCL TV is broken for shutdown, need alternative
# I'm turning off TV with this script via Homekit/Homebridge integration, separate script wakes TV via AppleTV

# Should work with all TCL / Thomson TVs with SmartTV2 OS (AKA sitatvservice)

# list of possible button codes at https://github.com/Zigazou/opentclremote/blob/master/ui/opentclremote.glade
# TR_KEY_POWER is not listed but works as shutdown command

from socket import (socket, AF_INET, SOCK_STREAM)

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

tcl_host = "192.168.1.198"

try:
    remote_controller = RemoteController(tcl_host)
    remote_controller.press_key("TR_KEY_POWER")

except Exception as zonk:
    print(f"{zonk}")