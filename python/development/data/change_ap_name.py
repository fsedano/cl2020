#!/usr/bin/python3
"""
Code to provision APs based on spreadsheet data
"""
import csv
import json
import requests
import os
import urllib3
import base64
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from netaddr import EUI, mac_cisco

controller = {
    "ip":"35.180.30.10",
    "user":"lab",
    "password":"lab"
}


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WLC:
    def __init__(self, ip, user, password):
        print("Doing init")
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
        self.url = f"https://{self.controller_ip}/restconf/data/Cisco-IOS-XE-wireless-ap-cfg:ap-cfg-data/ap-tags/ap-tag/"

        #self.url =  f"https://{self.controller_ip}/restconf/data/Cisco-IOS-XE-wireless-access-point-oper:access-point-oper-data/capwap-data"
                               #https://35.180.30.10/restconf/data/Cisco-IOS-XE-wireless-access-point-oper:access-point-oper-data/radio-oper-data/wtp-mac
        print(f"I have been born and url is {self.url}")

    def _change_policy_tag_payload(self, payload, mac, new_policy_tag):
        _payload = json.loads(payload.text)
        print(_payload)
        for entry in _payload['Cisco-IOS-XE-wireless-ap-cfg:ap-tag']:
            if entry['ap-mac'] == mac:
                entry['policy-tag'] = new_policy_tag
        return json.dumps(_payload)

    def get_joined_aps(self):
        try:
            url = self.baseurl + "Cisco-IOS-XE-wireless-access-point-oper:access-point-oper-data/capwap-data"
            response = requests.request("GET",
                url,
                headers=self.headers,
                verify=False,
                auth=self.controller_auth)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print(f"Success!")
            #print(f"Data; {response.text}")
            payload = response.json()['Cisco-IOS-XE-wireless-access-point-oper:capwap-data']
            for entry in payload:
                MAC = EUI(entry['wtp-mac'], dialect=mac_cisco)
                serial = entry["device-detail"]["static-info"]["board-data"]["wtp-serial-num"]
                self.ap_list[serial] = {
                    "name":entry["name"],
                    "MAC":str(MAC)
                }
            print(self.ap_list)

    def get_ap_sn(self, mac):
        try:
            response = requests.request("GET",
                self.url,
                headers=self.headers,
                verify=False,
                auth=HTTPBasicAuth('lab', 'lab'))
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print(f"Success!. Data is {response.text}")
        #d = payload.json()['Cisco-IOS-XE-wireless-access-point-oper:capwap-data']
        #for ap in d:
        #    serial_number = ap['device-detail']['static-info']['board-data']['wtp-serial-num']
        #    print(serial_number)

def readcsv():
    with open("AP_Inventory.csv", encoding='utf-8') as f:
        data = csv.reader(f, delimiter=',')
        next(data, None)
        for row in data:
            print(row)




wlc = WLC(controller["ip"],
    controller["user"],
    controller["password"])
#wlc.get_ap_sn(ap)
wlc.get_joined_aps()