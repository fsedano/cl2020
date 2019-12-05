#import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from netaddr import EUI, mac_cisco, mac_unix_expanded
import logging


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
        logging.info(f"Changing AP MAC {ap_info['MAC']} to have tag {inventory_info['tag']}")

        # Create site tag
        self.create_site_tag(inventory_info['tag'])
        payload = {"ap-tag": 
            {"ap-mac":ap_info['MAC'], 
            "site-tag":inventory_info['tag']}
        }
        logging.info(f"Sending payload to AP TAG url: {payload}")

        try:
            response = requests.request("PATCH",
                    self.ap_tag_url,
                    headers=self.headers,
                    verify=False,
                    auth=self.controller_auth,
                    json=payload)
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.exception(f'Other error occurred: {err}')
        else:
            logging.info(f"Success!")


    def create_site_tag(self, site_tag_name):
        logging.info(f"Creating site tag {site_tag_name}")
        payload = {"site-tag-config": {
                "site-tag-name":site_tag_name,
                "is-local-site":"false"
                }
        }
        url = self.baseurl + "Cisco-IOS-XE-wireless-site-cfg:site-cfg-data/site-tag-configs/site-tag-config/"
        logging.info(f"Sending payload to site tag config url: {payload}")

        try:
            response = requests.request("PATCH",
                    url,
                    headers=self.headers,
                    verify=False,
                    auth=self.controller_auth,
                    json=payload)
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.exception(f'Other error occurred: {err}')
        else:
            logging.info(f"Success!")

    def get_joined_aps(self):
        try:
            logging.info("Sending GET request for CAPWAP data")
            response = requests.request("GET",
                self.capwap_data_url,
                headers=self.headers,
                verify=False,
                auth=self.controller_auth)
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.exception(f'Other error occurred: {err}')
        else:
            logging.debug(f"Got data from controller {response.text}")
            try:
                json_payload = response.json()
                capwap_data = json_payload['Cisco-IOS-XE-wireless-access-point-oper:capwap-data']
                for entry in capwap_data:
                    ethernet_mac = entry["device-detail"]["static-info"]["board-data"]["wtp-enet-mac"]
                    serial = entry["device-detail"]["static-info"]["board-data"]["wtp-serial-num"]
                    MAC = EUI(ethernet_mac, dialect=mac_unix_expanded)
                    self.ap_list[serial] = {
                        "MAC":str(MAC)
                    }
            except ValueError as err:
                logging.info(f"No data was returned")
            except Exception as err:
                logging.exception(f"Other error: {err}")
            else:
                logging.info(f"Success!. {len(self.ap_list)} APs joined")

        return self.ap_list


