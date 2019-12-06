#!/usr/bin/python3
"""
Code to provision AP tags based on spreadsheet data
"""

import logging
from readinventory import Inventory
from wirelesscontroller import C9800

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s (%(levelname)s) %(message)s")

### Replace IP with the one for your controller
controller = {
    "ip":"<your_ip_address>",
    "user":"admin",
    "password":"Vimlab123@"
}

wlc = C9800(controller["ip"],
    controller["user"],
    controller["password"])

