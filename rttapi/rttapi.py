from rttapi.api import RttApi
import rttapi.parser as parser

class RttApiWrapper:
    def __init__(self, username: str, password: str):
        self.credentials = (username, password)
        self.__api = RttApi()

    def search_station_departures(self, station_code: str):
        json = self.__api.fetch_station_info(self.credentials, station_code)
        return parser.parse_search(json)
