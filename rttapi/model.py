import datetime
from typing import List

class LocationDetail:
    """
    Detail of the queried station
    """
    def __init__(self, name: str, crs: str, tiploc: List[str]):
        """
        Constructor
        :param name: The name of the station
        :param crs: The 3-letter Computer Reservation System code (e.g. 'CLJ')
        :param tiploc: The timing point location (TIPLOC) code(s) for this station. May be a string or a list[string].
        """
        self.name = name
        self.crs = crs
        self.tiploc = tiploc

class LocationContainer:
    def __init__(self):
        self.location_detail: Location = None
        self.service_uid: str = None
        self.run_date: datetime.date = None
        self.train_identity: str = None
        self.running_identity: str = None

        self.atoc_code: str = "ZZ"
        self.atoc_name: str = "Unknown"

        self.service_type: str = None
        self.is_passenger: bool = False
        self.planned_cancel: bool = False

        self.origin: List[Pair] = []
        self.destination: List[Pair] = []

        self.countdown_minutes: int = -1

class SearchResult:
    """
    This class isn't defined in the RTT API but forms the first part
    of all search API calls
    """
    def __init__(self):
        self.location: LocationDetail = None
        """ rttapi.model.LocationDetail object detailing the location searched for """

        self.filter: LocationDetail = None
        """ rttapi.model.LocationDetail objects detailing the location searched for, nested within from & to properties """

        self.services: List[LocationContainer] = []
        """" Array of rttapi.model.LocationContainer containing the location information and service metadata """

class Pair:
    """
     A TIPLOC/timing pair for a location
    """
    def __init__(self):
        self.tiploc: str = None
        """ The TIPLOC code for this timing point"""

        self.description: str = None
        """ The name of this timing point"""

        self.working_time: str = None
        """
         Relevant working time for this location for the activity that this pair is performing. 
         If it is in the context of an origin, it will be a departure time - for a destination it will be an arrival time. 
         In format HHmmss e.g. 150330 
        """

        self.public_time: str = None
        """ As working_time but for the advertised public times. In format HHmm e.g. 1503 """


class Location:
    """
    See https://www.realtimetrains.co.uk/about/developer/pull/docs/locationlist/ - This class is a mirror of the API
    """
    def __init__(self):
        self.realtime_activated: bool = False
        self.tiploc: str = None
        self.crs: str = None
        self.description: str = None

        self.wtt_booked_arrival: str = None
        self.wtt_booked_departure: str = None
        self.wtt_booked_pass: str = None

        self.gbtt_booked_arrival: str = None
        self.gbtt_booked_departure: str = None

        self.origin: List[Pair] = []
        self.destination: List[Pair] = []

        self.is_call: bool = False
        self.is_call_public_simple: bool = False

        self.realtime_arrival: str = None
        self.realtime_arrival_actual: bool = False
        self.realtime_arrival_no_report: bool = False
        self.realtime_wtt_arrival_lateness: int = 0
        self.realtime_gbtt_arrival_lateness: int = 0

        self.realtime_departure: str = None
        self.realtime_departure_actual: bool = False
        self.realtime_departure_no_report: bool = False
        self.realtime_wtt_departure_lateness: int = 0
        self.realtime_gbtt_departure_lateness: int = 0

        self.platform: str = None
        self.platform_confirmed: bool = False
        self.platform_changed: bool = False

        self.line: str = None
        self.line_confirmed: bool = False

        self.path: str = None
        self.path_confirmed: bool = False

        self.cancel_reason_code: str = None
        self.cancel_reason_short_text: str = None
        self.cancel_reason_long_text: str = None

        self.display_as: str = None

        self.service_location: str = None


class Service:
    """
    See https://www.realtimetrains.co.uk/about/developer/pull/docs/locationlist/ - This class is a mirror of the API
    """
    def __init__(self):
        self.service_uid: str = None
        self.run_date: datetime.date = None
        self.service_type: str = None
        self.is_passenger: bool = False
        self.train_identity: str = None
        self.power_type: str = None
        self.train_class: str = None
        self.sleeper: str = None

        self.atoc_code: str = "ZZ"
        self.atoc_name: str = "Unknown"

        self.performance_monitored: bool = False
        self.origin: List[Pair] = []
        self.destination: List[Pair] = []
        self.locations: List[Location] = []

        self.realtime_activated: bool = False
        self.running_identity: str = None