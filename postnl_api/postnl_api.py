""" Python wrapper for the PostNL API """

import logging
import time
from datetime import datetime, timedelta
from urllib.parse import unquote

import requests

from postnl_api.items.package import Package
from postnl_api.items.letter import Letter

BASE_URL = "https://jouw.postnl.nl"

AUTHENTICATE_URL = BASE_URL + "/mobile/token"
SHIPMENTS_URL = BASE_URL + "/mobile/api/shipments"
PROFILE_URL = BASE_URL + "/mobile/api/profile"
LETTERS_URL = BASE_URL + "/mobile/api/letters"
VALIDATE_LETTERS_URL = BASE_URL + "/mobile/api/letters/validation"

## PROFILE_URL
## isMyMailAvailable: true / false
## hasPendingMyMailValidation: true / false

## VALIDATE_LETTERS_URL
## status: Validated

## CHANGE NAME
## PATCH /mobile/api/shipments/{package-key}

## DELETE SHIPMENT
## DELETE /mobile/api/shipments/{package-key}

## DELETE LETTER
## DELETE /mobile/api/letters/{letter-barcode}

DEFAULT_HEADER = {"api-version": "4.16", "X-Client-Library": "python-postnl-api", "User-Agent": "PostNL/Android/6.5.1"}

REFRESH_RATE = 120

_LOGGER = logging.getLogger(__name__)


class PostNL_API(object):
    """ Interface class for the PostNL API """

    def __init__(self, user, password, refresh_rate=REFRESH_RATE):
        """ Constructor """
        self._user = user
        self._password = password
        self._deliveries = {}
        self._distributions = {}
        self._letters = {}
        self._letters_activated = False
        self._last_refresh = None
        self._refresh_rate = refresh_rate
        self._request_login()

    @property
    def _token_expired(self):
        """ checks whether or not the token is expired """
        return datetime.now() > self._token_expires_at

    def _update(self):
        """ Update the cache """
        current_time = int(time.time())
        last_refresh = 0 if self._last_refresh is None else self._last_refresh

        if current_time >= (last_refresh + self._refresh_rate):
            self._update_packages()
            self._update_letter_status()
            self._update_letters()
            self._last_refresh = int(time.time())

    def _update_packages(self):
        """ Retrieve packages """
        packages = self._request_update(SHIPMENTS_URL)
        if packages is False:
            return

        self._deliveries = {}
        self._distributions = {}

        for package in packages:
            if package.get("settings").get("box") == "Sender":
                self._distributions[package["key"]] = Package(package)
            else:
                self._deliveries[package["key"]] = Package(package)

    def _update_letters(self):
        """ Retrieve letters """
        if self._letters_activated is False:
            return

        letters = self._request_update(LETTERS_URL)
        if letters is False:
            return

        self._letters = {}

        for letter in letters:
            documents = self._request_update(LETTERS_URL + "/" + letter["barcode"])
            self._letters[letter["barcode"]] = Letter(letter, documents)

    def _update_letter_status(self):
        """ update the state of being able to see letters """
        validate = self._request_update(VALIDATE_LETTERS_URL)

        if validate.get("status") == "Validated":
            self._letters_activated = True

    def get_relevant_deliveries(self):
        """ filter shipments to today's and future shipments """
        self._update()
        return [
            d
            for d in self._deliveries.values()
            if (not d.is_delivered) or (d.is_delivered and d.delivery_today)
        ]

    def get_deliveries(self):
        """ Get all packages to be delivered to you """
        self._update()
        return self._deliveries.values()

    def get_distributions(self):
        """ Get all packages submitted by you """
        self._update()
        return self._distributions.values()

    def get_letters(self):
        """ Get all letters to be delivered to you """
        self._update()
        return self._letters.values()

    @property
    def is_letters_activated(self):
        """ Return if letters are activated or not """
        return self._letters_activated

    def _request_update(self, url, count=0, max=3):
        """ Perform a request to update information """
        if self._token_expired:
            self._request_access_token()
        headers = {
            "authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers={**headers, **DEFAULT_HEADER})

        if response.status_code == 401:
            count += 1
            _LOGGER.debug(f"Access denied. Failed to refresh, attempt {count} of {max}.")
            self._request_update(url, count, max)

        if response.status_code != 200:
            _LOGGER.error("Unable to perform request " + str(response.content))
            return False

        return response.json()

    def _request_login(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        payload = {
            "grant_type": "password",
            "client_id": "pwAndroidApp",
            "username": self._user,
            "password": self._password,
        }

        try:
            response = requests.request(
                "POST",
                AUTHENTICATE_URL,
                data=payload,
                headers={**headers, **DEFAULT_HEADER},
            )
            data = response.json()

        except Exception:
            raise (UnauthorizedException())

        if "error" in data:
            raise UnauthorizedException(data["error"])

        self._access_token = data["access_token"]
        self._refresh_token = unquote(data["refresh_token"])
        self._token_expires_in = data["expires_in"]
        self._token_expires_at = datetime.now() + timedelta(
            0, (int(data["expires_in"]) - 20)
        )

    def _request_access_token(self):
        """ Refresh access_token """

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {"grant_type": "refresh_token", "refresh_token": self._refresh_token}
        response = requests.request(
            "POST",
            AUTHENTICATE_URL,
            data=payload,
            headers={**headers, **DEFAULT_HEADER},
        )

        data = response.json()
        if response.status_code != 200:
            self._request_login()
        else:
            self._access_token = data["access_token"]
            self._refresh_token = unquote(data["refresh_token"])
            self._token_expires_in = data["expires_in"]
            self._token_expires_at = datetime.now() + timedelta(
                0, (int(data["expires_in"]) - 20)
            )


class UnauthorizedException(Exception):
    pass


class PostnlApiException(Exception):
    pass
