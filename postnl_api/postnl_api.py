"""
Python wrapper for the PostNL API
"""

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

    """
    Interface class for the PostNL API
    """

    def __init__(self, user, password):

        self._user = user
        self._password = password

        payload = {
            'grant_type': 'password',
            'client_id': 'pwIOSApp',
            'username': self._user,
            'password': self._password
        }

        headers = {
            'api-version': '4.6',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'content-type': "application/x-www-form-urlencoded",
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload, headers=headers)

        data = response.json()

        self._access_token = data['access_token']
        self._refresh_token = data['refresh_token']
        self._token_expires_in = data['expires_in']  # TODO Add logic to refresh on invalidate

    """
    Refresh access_token
    """
    def refresh_token(self):

        payload = {
            'grant_type': 'refresh_token',
            'client_id': 'pwIOSApp',
            'refresh_token': self._refresh_token
        }

        headers = {
            'api-version': '4.6',
            'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
            'content-type': "application/x-www-form-urlencoded",
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload, headers=headers)

        data = response.json()

        self._access_token = data['access_token']

    """
    Retrieve shipments
    """
    def get_shipments(self):

        headers = {
            'api-version': '4.6',
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

    """
    Retrieve profile
    """
    def get_profile(self):

        headers = {
            'api-version': '4.6',
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

    """
    Retrieve letters
    """
    def get_letters(self):

        headers = {
            'api-version': '4.6',
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

        if letters['type'] == 'ProfileValidationFeatureMissing':
            _LOGGER.error(letters['message'])
            return []

        return letters

    """
    Retrieve relevant shipments
    """
    def get_relevant_shipments(self):

        shipments = self.get_shipments()
        relevant_shipments = []

        for shipment in shipments:

            # Check if package is not delivered yet
            if not shipment['status']['isDelivered']:
                relevant_shipments.append(shipment)
                continue

            # Check if package has been delivered today
            if shipment['status']['delivery']:
                delivery_date = datetime.strptime( shipment['status']['delivery']['deliveryDate'][:19], "%Y-%m-%dT%H:%M:%S" )

                if delivery_date.date() == datetime.today().date():
                    relevant_shipments.append(shipment)
                    continue

        return relevant_shipments