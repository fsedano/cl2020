import requests
import logging
import urllib3
from requests.exceptions import HTTPError

API_ENDPOINT = "https://mailb.inf-pronet.com:5000/call"

class PhoneCaller:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        logging.info(f"Phone number is {phone_number}")
        self.notified_clients = set()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __make_phone_call(self, text):
        """
        Make a phone call, doing text to speech from the passed text parameter
        """
        logging.info(f"Making a phone call to {self.phone_number}")
        return
        data = {
            "text" : text,
            "phone":self.phone_number,
            "password":"ciscolive"
        }
        headers = {
            'Content-Type': "application/json"
        }

        try:
            response = requests.request("POST",
                url=API_ENDPOINT,
                json=data,
                verify=False,
                headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f"Error scheduling call: {http_err}")
        except Exception as err:
            logging.error(f"An unexpected error happened: {err}")
        else:
            logging.info("Sucessfully scheduled call")


    def notify_changes(self, current_clients):
        """
        Compare the list of passed current clients against the last time we made a call.
        If the list is different, perform the call.
        """
        if current_clients == self.notified_clients:
            ## No need to notify since there was no change
            return

        self.notified_clients = current_clients.copy()
        logging.info(f"Notifying phone about {list(current_clients)}")

        text = f"There is a change on the connected clients. Now we have {len(current_clients)} clients."

        if len(current_clients) > 0:
            text = text + " The I P addresses of the clients are: "
            for client_ip in current_clients:
                text = text + client_ip.replace('.', ' ') + ", "

        self.__make_phone_call(text)
