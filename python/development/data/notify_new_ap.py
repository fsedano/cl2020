#!/usr/bin/python3

import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError
import xmltodict
import time
import requests
import os
import json


payload = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <access-point-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-wireless-access-point-oper"><capwap-data><ip-addr/></capwap-data></access-point-oper-data>
</filter>
"""
def remove_from_env(var):
    if var in os.environ:
        os.environ.pop(var)

def remove_proxy():
    remove_from_env('HTTP_PROXY')
    remove_from_env('HTTPS_PROXY')
    remove_from_env('http_proxy')
    remove_from_env('https_proxy')

def notify_changes(currentaps):
    text = f"There is a change on the access point list. Now we have {len(currentaps)} access points."
    if len(currentaps) > 0:
        text = text + " The I P addresses of the access points are: "
        for ap in currentaps:
            text = text + ap.replace('.', ' ') + ", "

    data = {
        "text" : text,
        "phone":"+34671167751",
        "password":"ciscolive"
    }
    headers = {
        'Content-Type': "application/json"
    }
    print(f"dats is {json.dumps(data)}")
    API_ENDPOINT = "https://mailb.inf-pronet.com:5000/call"
    r = requests.request("POST", url = API_ENDPOINT, data = json.dumps(data), verify=False, headers=headers)
    print(f"Post code is {r}")

host = "10.51.65.10"
port = "830"
username="lab"
password = "lab"
remove_proxy()

currentaps = []
skipnotify = True
while True:
    with manager.connect(host=host,
                            port=port,
                            username=username,
                            password=password,
                            hostkey_verify=False) as m:
        apcount = len(currentaps)
        response = m.get(payload).data_xml
        #print(f"resp={response}")
        root = ET.fromstring(response.encode())
        c = root[0]
        currentaps = []
        for child in c:
            #print(f"xx is {child[0].text}")
            currentaps.append(child[0].text)
        if len(currentaps) != apcount and not skipnotify:
            print(f"Changed!! list is {currentaps}")
            notify_changes(currentaps)
        skipnotify = False
        time.sleep(1)