#!/usr/bin/python3
"""
Code to provision APs based on spreadsheet data
"""

import json
import requests
import os
import urllib3
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from netaddr import EUI, mac_cisco, mac_unix_expanded
import logging
from readinventory import Inventory
from wirelesscontroller import WLC

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s (%(levelname)s) %(message)s")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
