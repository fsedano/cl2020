import requests
import json
import logging
import urllib3
from requests.exceptions import HTTPError

API_ENDPOINT = "https://mailb.inf-pronet.com:5000/call"

class PhoneCaller:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.notified_clients = set()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def notify_changes(self, current_clients):
        if current_clients == self.notified_clients:
            return
        self.notified_clients = current_clients.copy()
        logging.info(f"Notifying phone about {list(current_clients)}")
        text = f"There is a change on the connected clients. Now we have {len(current_clients)} clients."
        if len(current_clients) > 0:
            text = text + " The I P addresses of the clients are: "
            for client_ip in current_clients:
                text = text + client_ip.replace('.', ' ') + ", "

        data = {
            "text" : text,
            "phone":self.phone_number,
            "password":"ciscolive"
        }
        headers = {
            'Content-Type': "application/json"
        }

        try:
            response = requests.request("POST", url = API_ENDPOINT, data = json.dumps(data), verify=False, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f"Error scheduling call: {http_err}")
        else:
            logging.info("Sucessfully scheduled call")
