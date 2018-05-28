""" Python wrapper for the PostNL API """

from datetime import datetime, timedelta
import re

import requests

BASE_URL = 'https://jouw.postnl.nl'

AUTHENTICATE_URL = BASE_URL + '/mobile/token'
SHIPMENTS_URL = BASE_URL + '/mobile/api/shipments'
PROFILE_URL = BASE_URL + '/mobile/api/profile'
LETTERS_URL = BASE_URL + '/mobile/api/letters'
VALIDATE_LETTERS_URL = BASE_URL + '/mobile/api/letters/validation'

DEFAULT_HEADER = {
    'api-version': '4.7',
    'user-agent': 'PostNL/1 CFNetwork/889.3 Darwin/17.2.0',
}


class UnauthorizedException(Exception):
    pass


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

        try:
            response = requests.request(
                'POST', AUTHENTICATE_URL, data=payload, headers=DEFAULT_HEADER)
            data = response.json()

        except Exception:
            raise(UnauthorizedException())

        if 'error' in data:
            raise UnauthorizedException(data['error'])

        self._access_token = data['access_token']
        self._refresh_token = data['refresh_token']
        self._token_expires_in = data['expires_in']
        self._token_expires_at = datetime.now(
        ) + timedelta(0, data['expires_in'])

    def _is_token_expired(self):
        """ Check if access token is expired """
        if (datetime.now() > self._token_expires_at):
            self._refresh_access_token()
            return True

        return False

    def _refresh_access_token(self):
        """ Refresh access_token """

        payload = {
            'grant_type': 'refresh_token',
            'client_id': 'pwIOSApp',
            'refresh_token': self._refresh_token
        }

        response = requests.request(
            'POST', AUTHENTICATE_URL, data=payload, headers=DEFAULT_HEADER)

        data = response.json()

        self._access_token = data['access_token']

    def parse_datetime(self, text, dateFormat='%d-%m-%Y', timeFormat='%H:%M'):

        def parse_date(date):
            return datetime.strptime(date.group(1)
                                     .replace(' ', '')[:-6], '%Y-%m-%dT%H:%M:%S').strftime(dateFormat)

        def parse_time(date):
            return datetime.strptime(date.group(1)
                                     .replace(' ', '')[:-6], '%Y-%m-%dT%H:%M:%S').strftime(timeFormat)

        text = re.sub(r'{(?:Date|dateAbs):(.*?)}', parse_date, text)
        text = re.sub(r'{(?:time):(.*?)}', parse_time, text)

        return text

    def get_shipments(self):
        """ Retrieve shipments """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', SHIPMENTS_URL, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 401:
            self._refresh_access_token()
            shipments = self.get_shipments()
        else:
            shipments = response.json()

        return shipments

    def get_shipment(self, shipment_id):
        """ Retrieve single shipment by id """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', SHIPMENTS_URL + '/' + shipment_id, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 401:
            self._refresh_access_token()
            shipments = self.get_shipment(shipment_id)
        else:
            shipments = response.json()

        return shipments

    def get_profile(self):
        """ Retrieve profile """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', PROFILE_URL, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 401:
            self._refresh_access_token()
            profile = self.get_profile()
        else:
            profile = response.json()

        return profile

    def validate_letters(self):
        """ Retrieve letter validation status """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', VALIDATE_LETTERS_URL, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 401:
            self._refresh_access_token()
            validation = self.validate_letters()
        else:
            validation = response.json()

        return validation

    def get_letters(self):
        """ Retrieve letters """

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', LETTERS_URL, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 401:
            self._refresh_access_token()
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

        self._is_token_expired()

        headers = {
            'authorization': 'Bearer ' + self._access_token
        }

        response = requests.request(
            'GET', LETTERS_URL + '/' + letter_id, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 200:
            letter = response.json()
        elif response.status_code == 401:
            self._refresh_access_token()
            letter = self.get_letter(letter_id)
        else:
            raise Exception('Unknown Error')

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
            if shipment['status']['delivery'] and \
               shipment['status']['delivery']['deliveryDate']:
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

                if expected_delivery_date.date() >= datetime.today().date():
                    relevant_letters.append(letter)

        return relevant_letters
