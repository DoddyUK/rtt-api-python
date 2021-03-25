import datetime
from typing import List

class LocationDetail:
    def __init__(self, name: str, crs: str, tiploc: List[str]):
        self.name = name
        self.crs = crs
        self.tiploc = tiploc

    def __str__(self):
        return "\n      LocationDetail:\n" \
               "            name: {}\n" \
               "            crs: {}\n" \
               "            toploc: {}\n"\
            .format(self.name, self.crs, self.tiploc)


class LocationContainer:
    def __init__(self):
        self.location_detail = None
        self.service_uid: str = None
        self.run_date: datetime.date = None
        self.train_identity_detailed: str = None
        self.running_identity: str = None

        self.atoc_code: str = "ZZ"
        self.atoc_name: str = "Unknown"

        self.service_type: str = None
        self.is_passenger: bool = False
        self.planned_cancel: bool = False

        self.origin: List[RttPair] = []
        self.destination: List[RttPair] = []

        self.countdown_minutes: int = -1

'''
This class isn't defined in the RTT API but forms the first part
of all search API calls
'''
class SearchResult:
    def __init__(self):
        self.location: LocationDetail = None
        self.filter: LocationDetail = None
        self.services: List[LocationContainer] = []

    def __str__(self):
        return "SearchResult:\n" \
               "    location: {}\n" \
               "    filter: {}\n" \
               "    services: {}\n"\
            .format(self.location, self.filter, self.services)

'''
 Confusingly, the RTT API refers to this class as a Pair. 
 Named it RttPair to avoid confusion with internal Python data type pair
'''
class RttPair:
    def __init__(self):
        self.tiploc: str = None
        self.description: str = None
        self.working_time: str = None
        self.public_time: str = None


class Location:
    def __init__(self):
        self.realtime_activated: bool = False
        self.tiploc: str = None
        self.crs: str = None
        self.description: str = None

        self.wtt_booked_arrival: str = None
        self.wtt_booked_departure: str = None
        self.wtt_booked_pass: str = None

        self.gbbt_booked_arrival: str = None
        self.gbbt_booked_departure: str = None

        self.origin: List[RttPair] = []
        self.destination: List[RttPair] = []

        self.is_call_detailed: bool = False
        self.is_call_public_simple: bool = False

        self.realtime_arrival: str = None
        self.realtime_arrival_actual: bool = False
        self.realtime_arrival_no_report: bool = False
        self.realtime_wtt_arrival_lateness_detailed: int = 0
        self.realtime_gbbt_arrival_lateness_detailed: int = 0

        self.realtime_departure: str = None
        self.realtime_departure_actual: bool = False
        self.realtime_departure_no_report: bool = False
        self.realtime_wtt_departure_lateness_detailed: int = 0
        self.realtime_gbbt_departure_lateness_detailed: int = 0

        self.platform: str = None
        self.platform_confirmed: bool = False
        self.platform_changed: bool = False

        self.line_detailed: str = None
        self.line_confirmed_detailed: bool = False

        self.cancel_reason_code: str = None
        self.cancel_reason_short_text: str = None
        self.cancel_reason_long_text: str = None

        self.display_as: str = None

        self.service_location: str = None


class Service:
    def __init__(self):
        self.service_uid: str = None
        self.run_date: datetime.date = None
        self.service_type: str = None
        self.is_passenger: bool = False
        self.train_identity_detailed: str = None
        self.power_type_detailed: str = None
        self.train_class: str = None
        self.sleeper: str = None

        self.atoc_code: str = "ZZ"
        self.atoc_name: str = "Unknown"

        self.performance_monitored: bool = False
        self.origin: List[RttPair] = []
        self.destination: List[RttPair] = []
        self.locations: List[Location] = []

        self.realtime_activated: bool = False
        self.running_identity: str = None