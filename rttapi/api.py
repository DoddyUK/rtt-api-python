import requests
import datetime
import rttapi.parser as parser
from rttapi.model import SearchResult
from requests.auth import HTTPBasicAuth


def _request_basic_auth(credentials: tuple, url: str) -> dict:
    """
    Initiates a request to the given url. Authenticated using credentials pair via HTTPBasicAuth.

    :param credentials: A username/password pair used for the HTTPBasicAuth challenge
    :param url: The URL to call

    :raises requests.HTTPError: If the network request fails

    :return:A dict representation of the JSON body of the reply
    """

    username, password = credentials

    auth = HTTPBasicAuth(username, password)

    response = requests.get(url, auth=auth)

    if response.ok:
        return response.json()
    else:
        raise requests.HTTPError("Request to {} failed ({}, {})".format(url, response.status_code, response.reason))


class _Api:
    """
    Internal API. Makes network requests to the Realtime Trains API and returns the resulting dict data.

    Requests are authenticated via HTTPBasicAuth, with credentials passed in as a pair(username, password).
    """

    __urlBase = "https://api.rtt.io/api/v1"

    def fetch_station_departure_info(self, credentials: tuple, station_code: str) -> dict:
        """
        Requests the list of upcoming departures from a given station.

        :param credentials: A username/password pair used for the HTTPBasicAuth challenge
        :param station_code: Either the three-letter CRS station code (CRS, e.g. 'CLJ') or the longer TIPLOC code (e.g. 'CLPHMJC')

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """
        url = "{base}/json/search/{station}".format(base=self.__urlBase, station=station_code)
        return _request_basic_auth(credentials, url)

    def fetch_station_arrival_info(self, credentials, station_code) -> dict:
        """
        Requests the list of upcoming departures from a given station.

        :param credentials: A username/password pair used for the HTTPBasicAuth challenge
        :param station_code: Either the three-letter CRS station code (CRS, e.g. 'CLJ') or the longer TIPLOC code (e.g. 'CLPHMJC')

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """
        url = "{base}/json/search/{station}/arrivals".format(base=self.__urlBase, station=station_code)
        return _request_basic_auth(credentials, url)


    def fetch_service_info(self, credentials: tuple, service_uid: str, service_date: datetime.date) -> dict:
        """
        Requests the service information for a given service UID, including the list of intermediate stops

        :param credentials: A username/password pair used for the HTTPBasicAuth challenge
        :param service_uid: The unique identifier for the train service
        :param service_date: The running date of the service

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """
        url = "{base}/json/service/{service_uid}/{year}/{month}/{day}".format(
            base=self.__urlBase,
            service_uid=service_uid,
            year=service_date.strftime('%Y'),
            month=service_date.strftime('%m'),
            day=service_date.strftime('%d')
        )
        return _request_basic_auth(credentials, url)


class RttApi:
    """
    The public-facing object for this API wrapper library.
    Reponsible for initiating requests to the RealtimeTrains API and parsing the response into the model
    """

    def __init__(self, username: str, password: str):
        """
        Constructor for the RttApi object.

        :param username: The RealtimeTrains API username to authenticate with
        :param password: The password matching the RealtimeTrains API username
        """
        self.credentials = (username, password)
        self.__api = _Api()

    def search_station_departures(self, station_code: str) -> SearchResult:
        """
        Requests the list of upcoming departures from a given station.

        :param station_code: Either the three-letter CRS station code (CRS, e.g. 'CLJ') or the longer TIPLOC code (e.g. 'CLPHMJC')

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """
        json = self.__api.fetch_station_departure_info(self.credentials, station_code)
        return parser.parse_search(json)

    def search_station_arrivals(self, station_code: str) -> SearchResult:
        """
        Requests the list of upcoming arrivals at a given station.

        :param station_code: Either the three-letter CRS station code (CRS, e.g. 'CLJ') or the longer TIPLOC code (e.g. 'CLPHMJC')

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """
        json = self.__api.fetch_station_departure_info(self.credentials, station_code)
        return parser.parse_search(json)
