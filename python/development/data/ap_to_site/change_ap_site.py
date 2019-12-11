#!/usr/bin/python3
"""
Code to provision AP tags based on spreadsheet data
"""

import logging
from readinventory import Inventory
from wirelesscontroller import C9800

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s (%(levelname)s) %(message)s")

### Replace IP with the one for your controller and username with your pod username.
controller = {
    "ip":"<your_controller_private_ip>",
    "user":"podx",
    "password":"Vimlab123@"
}

wlc = C9800(controller["ip"],
    controller["user"],
    controller["password"])

