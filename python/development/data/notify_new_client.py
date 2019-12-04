#!/usr/bin/python3

from lxml import etree
import lxml.etree as ET
from ncclient import manager
from ncclient.xml_ import to_ele
import requests
import json
import logging
import urllib3
from requests.exceptions import HTTPError
from phone_caller import PhoneCaller

controller = {
    "ip":"35.180.30.10",
    "user":"lab",
    "password":"lab"
}

rpc = """
<establish-subscription xmlns="urn:ietf:params:xml:ns:yang:ietf-event-notifications" xmlns:yp="urn:ietf:params:xml:ns:yang:ietf-yang-push">
    <stream>yp:yang-push</stream>
    <yp:xpath-filter>%s</yp:xpath-filter>
    <yp:dampening-period>0</yp:dampening-period>
</establish-subscription>
"""
filter = "/wireless-client-oper:client-oper-data/sisf-db-mac/ipv4-binding"

rpc = rpc % (filter)

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s (%(levelname)s) %(message)s")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def is_delete(root):
    for x in root.iter('{urn:ietf:params:xml:ns:yang:ietf-yang-patch}operation'):
        if x.text == 'delete':
            return True
    return False

currentaps = set()
last_notified_aps = set()

#phone = PhoneCaller('+34671167751')
phone = PhoneCaller('')

if __name__ == '__main__':
    with manager.connect(host=controller['ip'],
                         port=830,
                         username=controller['user'],
                         password=controller['password'],
                         hostkey_verify=False) as m:

        response = m.dispatch(to_ele(rpc))
        logging.info("Waiting for notifications")
        while True:
            n = m.take_notification()
            root = ET.fromstring(n.notification_xml.encode("utf-8"))
            delete = is_delete(root)
            for x in root.iter('{http://cisco.com/ns/yang/Cisco-IOS-XE-wireless-client-oper}ip-addr'):
                if not delete:
                    currentaps.add(x.text)
                else:
                    currentaps.discard(x.text)
            phone.notify_changes(currentaps)
