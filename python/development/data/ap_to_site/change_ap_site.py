#!/usr/bin/python3
"""
Code to provision AP tags based on spreadsheet data
"""

import logging
from readinventory import Inventory
from wirelesscontroller import wirelesscontroller

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s (%(levelname)s) %(message)s")

### Replace IP with the one for your controller
controller = {
    "ip":"<your_controller_ip>",
    "user":"lab",
    "password":"lab"
}

