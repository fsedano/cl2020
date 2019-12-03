#!/usr/bin/python3
"""
Code to provision APs based on spreadsheet data
"""
import csv
import json
import requests
import os
import urllib3
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from netaddr import EUI, mac_cisco, mac_unix_expanded

controller = {
    "ip":"35.180.30.10",
    "user":"lab",
    "password":"lab"
}


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WLC:
    def __init__(self, ip, user, password):
        self.controller_ip = ip
        self.controller_user = user
        self.controller_password = password
        self.controller_auth = HTTPBasicAuth(user, password)
        self.ap_list = {}
        self.headers = {
            'Accept': "application/yang-data+json",
            'Content-Type': "application/yang-data+json",
            'cache-control': "no-cache"
        }
        self.baseurl = f"https://{self.controller_ip}/restconf/data/"
        self.ap_tag_url = self.baseurl + \
            "/Cisco-IOS-XE-wireless-ap-cfg:ap-cfg-data/ap-tags/ap-tag/"
        self.capwap_data_url = self.baseurl + \
            "Cisco-IOS-XE-wireless-access-point-oper:access-point-oper-data/capwap-data"


    def process_ap(self, ap_info, inventory_info):
        print(f"Changing AP MAC {ap_info['MAC']} to have tag {inventory_info['tag']}")
        payload = {"ap-tag": 
            {"ap-mac":ap_info['MAC'], 
            "site-tag":inventory_info['tag']}
        }
        print(f"Sending payload to AP TAG url: {json.dumps(payload)}")

        try:
            response = requests.request("PATCH",
                    self.ap_tag_url,
                    headers=self.headers,
                    verify=False,
                    auth=self.controller_auth,
                    data=json.dumps(payload))
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print(f"Success!")



    def get_joined_aps(self):
        try:
            print("Sending GET request for CAPWAP data")
            response = requests.request("GET",
                self.capwap_data_url,
                headers=self.headers,
                verify=False,
                auth=self.controller_auth)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print("Success!")
            #print(f"Got data from controller {response.text}")
            payload = response.json()['Cisco-IOS-XE-wireless-access-point-oper:capwap-data']
            for entry in payload:
                ethernet_mac = entry["device-detail"]["static-info"]["board-data"]["wtp-enet-mac"]
                serial = entry["device-detail"]["static-info"]["board-data"]["wtp-serial-num"]
                MAC = EUI(ethernet_mac, dialect=mac_unix_expanded)
                self.ap_list[serial] = {
                    "name":entry["name"],
                    "MAC":str(MAC)
                }
        return self.ap_list

class Inventory:
    def __init__(self, filename):
        self.filename = filename
        self.inventory_data = {}
    def read(self):
        with open("AP_Inventory.csv", encoding='utf-8') as f:
            data = csv.reader(f, delimiter=',')
            next(data, None)
            for row in data:
                print(row)
                if len(row) > 1:
                    serial = row[0]
                    name = row[1]
                    tag = row[2]
                    self.inventory_data[serial] = {
                        "name":name,
                        "tag":tag
                    }
            return self.inventory_data





wlc = WLC(controller["ip"],
    controller["user"],
    controller["password"])

aps = wlc.get_joined_aps()
inventory = Inventory('AP_Inventory.csv').read()

for ap_serial in aps:
    if ap_serial in inventory:
        wlc.process_ap(aps[ap_serial], inventory[ap_serial])
