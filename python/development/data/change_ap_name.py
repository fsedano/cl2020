#!/usr/bin/python3

import csv
import json
import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WLC:
    def __init__(self, controller_ip):
        print("Doing init")
        self.controller_ip = controller_ip
        self.headers = {
            'Accept': "application/yang-data+json",
            'Content-Type': "application/yang-data+json",
            'Authorization': "Basic Y2lzY286Y2lzY28=",
            'cache-control': "no-cache"
        }
        #self.url = f"https://{self.controller_ip}/restconf/data/Cisco-IOS-XE-wireless-ap-cfg:ap-cfg-data/ap-tags/ap-tag/"
        self.url =  f"https://{self.controller_ip}/restconf/data/Cisco-IOS-XE-wireless-access-point-oper:access-point-oper-data/capwap-data"
        print(f"I have been born and url is {self.url}")

    def _change_policy_tag_payload(self, payload, mac, new_policy_tag):
        _payload = json.loads(payload.text)
        print(_payload)
        for entry in _payload['Cisco-IOS-XE-wireless-ap-cfg:ap-tag']:
            if entry['ap-mac'] == mac:
                entry['policy-tag'] = new_policy_tag
        return json.dumps(_payload)

    def get_ap_sn(self, mac):
        payload = requests.request("GET", self.url, headers=self.headers, verify=False)
        d = payload.json()['Cisco-IOS-XE-wireless-access-point-oper:capwap-data']
        for ap in d:
            serial_number = ap['device-detail']['static-info']['board-data']['wtp-serial-num']
            print(serial_number)

def readcsv():
    with open("AP_Inventory.csv", encoding='utf-8') as f:
        data = csv.reader(f, delimiter=',')
        next(data, None)
        for row in data:
            print(row)


def remove_from_env(var):
    if var in os.environ:
        os.environ.pop(var)

remove_from_env('HTTP_PROXY')
remove_from_env('HTTPS_PROXY')
remove_from_env('http_proxy')
remove_from_env('https_proxy')





ap = "58:ac:78:de:8b:68"

wlc = WLC("10.51.65.10")
wlc.get_ap_sn(ap)