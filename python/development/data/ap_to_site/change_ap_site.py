#!/usr/bin/python3
"""
Code to provision APs based on spreadsheet data
"""

import logging
from readinventory import Inventory
from wirelesscontroller import WLC

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s (%(levelname)s) %(message)s")


controller = {
    "ip":"35.180.30.10",
    "user":"lab",
    "password":"lab"
}

wlc = WLC(controller["ip"],
    controller["user"],
    controller["password"])

aps = wlc.get_joined_aps()
inventory = Inventory('AP_Inventory.csv').read()

for ap_serial in aps:
    if ap_serial in inventory:
        wlc.process_ap(aps[ap_serial], inventory[ap_serial])
