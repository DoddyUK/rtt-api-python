import requests
import datetime
import rttapi.parser as parser
from rttapi.model import SearchResult, Service
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


    def fetch_service_info_datetime(self, credentials: tuple, service_uid: str, service_date: datetime.date) -> dict:
        """
        Requests the service information for a given service UID, including the list of intermediate stops

        :param credentials: A username/password pair used for the HTTPBasicAuth challenge
        :param service_uid: The unique identifier for the train service
        :param service_date: The running date of the service

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """
        return self.fetch_service_info_ymd(
            credentials,
            service_uid,
            service_date.strftime('%Y'),
            service_date.strftime('%m'),
            service_date.strftime('%d')
        )

    def fetch_service_info_ymd(self, credentials: tuple, service_uid: str, year: str, month: str, day: str) -> dict:
        """
        Requests the service information for a given service UID, including the list of intermediate stops

        :param credentials: A username/password pair used for the HTTPBasicAuth challenge
        :param service_uid: The unique identifier for the train service
        :param year: Year of the service running date
        :param month: Month of the service running date
        :param day: Day of the service running date

        :return: A rttapi.model.SearchResult object mirroring the JSON reply
        """

        url = "{base}/json/service/{service_uid}/{year}/{month}/{day}".format(
            base=self.__urlBase,
            service_uid=service_uid,
            year=year,
            month=month,
            day=day
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

    def fetch_service_info_datetime(self, service_uid: str, service_date: datetime.date) -> Service:
        """
        Requests detailed information about a given service, using a datetime.date object to specify the running date

        :param service_uid: The unique ID of the service
        :param service_date: The running date of the service as a datetime.date object

        :return: A model.Service object representing this service's details
        """
        json = self.__api.fetch_service_info_datetime(self.credentials, service_uid, service_date)
        return parser.parse_service(json)


    def fetch_service_info_ymd(self, service_uid: str, service_year: str, service_month: str, service_day: str) -> Service:
        """
        Requests detailed information about a given service, using year/month/day to specify the running date

        :param service_uid: The unique ID of the service
        :param service_year: The year component of the service's running date
        :param service_month: The month component of the service's running date
        :param service_day: The day component of the service's running date

        :return: A model.Service object representing this service's details
        """
        json = self.__api.fetch_service_info_ymd(self.credentials, service_uid, service_year, service_month, service_day)
        return parser.parse_service(json)