""" Python wrapper for the PostNL API """

import logging
from datetime import datetime
import requests

_LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://jouw.postnl.nl'

AUTHENTICATE_URL = BASE_URL + '/mobile/token'
SHIPMENTS_URL = BASE_URL + '/mobile/api/shipments'
PROFILE_URL = BASE_URL + '/mobile/api/profile'
LETTERS_URL = BASE_URL + '/mobile/api/letters'

class PostNL_API(object):
    """ Interface class for the PostNL API """

    def __init__(self, user, password):
        """ Constructor """

        self._user = user
        self._password = password

        payload = {
            'grant_type': 'password',
            'client_id': 'pwIOSApp',
            'username': self._user,
            'password': self._password
        }

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'content-type': "application/x-www-form-urlencoded",
        }

        try:
            response = requests.request(
                'POST', AUTHENTICATE_URL, data=payload, headers=headers)

            data = response.json()

        except Exception:
            _LOGGER.exception('Credentials are wrong')

        # if response['error']:
        #     raise Exception(response['error']['error_description'])

        self._access_token = data['access_token']
        self._refresh_token = data['refresh_token']
        # TODO Add logic to refresh on invalidate
        self._token_expires_in = data['expires_in']

    def refresh_token(self):
        """ Refresh access_token """

        payload = {
            'grant_type': 'refresh_token',
            'client_id': 'pwIOSApp',
            'refresh_token': self._refresh_token
        }

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'content-type': "application/x-www-form-urlencoded",
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload, headers=headers)

        data = response.json()

        self._access_token = data['access_token']

    def get_shipments(self):
        """ Retrieve shipments """

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', SHIPMENTS_URL, headers=headers)

        if response.status_code == 401:
            self.refresh_token()
            shipments = self.get_shipments()
        else:
            shipments = response.json()

        return shipments

    def get_shipment(self, shipment_id):
        """ Retrieve single shipment by id """

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', SHIPMENTS_URL + '/' + shipment_id, headers=headers)

        if response.status_code == 401:
            self.refresh_token()
            shipments = self.get_shipment(shipment_id)
        else:
            shipments = response.json()

        return shipments

    def get_profile(self):
        """ Retrieve profile """

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', PROFILE_URL, headers=headers)

        if response.status_code == 401:
            self.refresh_token()
            profile = self.get_profile()
        else:
            profile = response.json()

        return profile

    def get_letters(self):
        """ Retrieve letters """

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', LETTERS_URL, headers=headers)

        if response.status_code == 401:
            self.refresh_token()
            letters = self.get_letters()
        else:
            letters = response.json()

        # TODO Add validation / exception handling
        # if letters['type'] == 'ProfileValidationFeatureMissing':
        #     _LOGGER.error(letters['message'])
        #     return []

        return letters

    def get_letter(self, letter_id):
        """ Retrieve single letter by id """

        headers = {
            'api-version': '4.7',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', LETTERS_URL + '/' + letter_id, headers=headers)

        if response.status_code == 401:
            self.refresh_token()
            letter = self.get_letter(letter_id)
        else:
            letter = response.json()

        return letter

    def get_relevant_shipments(self):
        """ Retrieve not delivered shipments and shipments delivered today """

        shipments = self.get_shipments()
        relevant_shipments = []

        for shipment in shipments:

            # Check if package is not delivered yet
            if not shipment['status']['isDelivered']:
                relevant_shipments.append(shipment)
                continue

            # Check if package has been delivered today
            if shipment['status']['delivery']:
                delivery_date = datetime.strptime(
                    shipment['status']['delivery']['deliveryDate'][:19], "%Y-%m-%dT%H:%M:%S")

                if delivery_date.date() == datetime.today().date():
                    relevant_shipments.append(shipment)

        return relevant_shipments

    def get_relevant_letters(self):
        """ Retrieve letters with a future delivery date """

        letters = self.get_letters()
        relevant_letters = []

        for letter in letters:
            
            # Check if letter is scheduled for delivery in the future
            if letter['expectedDeliveryDate']:
                expected_delivery_date = datetime.strptime(
                    letter['expectedDeliveryDate'][:19], "%Y-%m-%dT%H:%M:%S")

                if expected_delivery_date.date() == datetime.today().date():
                    relevant_letters.append(letter)

        return relevant_letters