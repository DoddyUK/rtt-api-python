from rttapi.model import *


def parse_search(json: dict) -> SearchResult:
    """
    Parses the root JSON object from a station search into a rttapi.model.SearchResult representation of the JSON data.

    :param json: The JSON data retrieved from the API, as a dictionary

    :raises ValueError: When an expected key is missing

    :return: A rttapi.model.SearchResult representation of the JSON data.
    """
    if not all(key in json for key in ('location', 'filter', 'services')):
        raise ValueError("JSON object missing required keys")

    if json['location'] is None:
        raise ValueError("location is None")

    out = SearchResult()
    out.location = parse_location_detail(json['location'])

    filter_json = __assign_if_set(out.filter, json, 'filter')
    if filter_json is not None:
        out.filter = parse_location_detail(filter_json)

    service_json = __assign_if_set(out.services, json, 'services')
    if service_json is not None:
        out.services = list(map(parse_location_container, service_json))


    return out

def parse_location_detail(json: dict) -> LocationDetail:
    """
    Parses a location detail JSON object from a station search into a rttapi.model.LocationDetail representation of the JSON data.

    :param json: The JSON data retrieved from the API, as a dictionary

    :raises ValueError: When an expected key is missing

    :return: A rttapi.model.LocationDetail representation of the JSON data.
    """
    if not all(key in json for key in ('name', 'crs', 'tiploc')):
        raise ValueError("JSON object missing required keys")

    return LocationDetail(
        json['name'],
        json['crs'],
        json['tiploc']
    )

def parse_pair(json: dict) -> Pair:
    """
    Parses a station/time Pair from JSON data

    :param json: The JSON data retrieved from the API, as a dictionary

    :raises ValueError: When an expected key is missing

    :return: A rttapi.model.Pair representation of the JSON data.
    """
    if not all(key in json for key in ('tiploc', 'description', 'workingTime', 'publicTime')):
        raise ValueError("JSON object missing required keys")

    out = Pair()
    out.tiploc = json['tiploc']
    out.description = json['description']
    out.working_time = json['workingTime']
    out.public_time = json['publicTime']

    return out

def parse_location(json: dict) -> Location:
    """
    Parses a location data JSON object from a station search into a rttapi.model.Location representation of the JSON data.

    :param json: The JSON data retrieved from the API, as a dictionary

    :raises ValueError: When an expected key is missing

    :return: A rttapi.model.Location representation of the JSON data.
    """
    if 'crs' not in json:
        raise ValueError("JSON object missing required keys")

    out = Location()

    out.realtime_activated = __assign_if_set(out.realtime_activated, json, 'realtimeActivated')
    out.tiploc = __assign_if_set(out.tiploc, json, 'tiploc')
    out.crs = json['crs']
    out.description = __assign_if_set(out.description, json, 'description')

    out.wtt_booked_arrival = __assign_if_set(out.wtt_booked_arrival, json, 'wttBookedArrival')
    out.wtt_booked_departure = __assign_if_set(out.wtt_booked_departure, json, 'wttBookedDeparture')
    out.wtt_booked_pass = __assign_if_set(out.wtt_booked_pass, json, 'wttBookedPass')

    out.gbtt_booked_arrival = __assign_if_set(out.gbtt_booked_arrival, json, 'gbttBookedArrival')
    out.gbtt_booked_departure = __assign_if_set(out.gbtt_booked_departure, json, 'gbttBookedDeparture')

    if _has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    if _has_value(json, 'destination'):
        out.destination = list(map(parse_pair, json['destination']))

    out.realtime_arrival = __assign_if_set(out.realtime_arrival, json, 'realtimeArrival')
    out.realtime_arrival_actual = __assign_if_set(out.realtime_arrival_actual, json, 'realtimeArrivalActual')
    out.realtime_arrival_no_report = __assign_if_set(out.realtime_arrival_no_report, json, 'realtimeArrivalNoReport')
    out.realtime_wtt_arrival_lateness = __assign_if_set(out.realtime_wtt_arrival_lateness, json, 'realtimeWttArrivalLateness')
    out.realtime_gbtt_arrival_lateness = __assign_if_set(out.realtime_gbtt_arrival_lateness, json, 'realtimeGbttArrivalLateness')

    out.realtime_departure = __assign_if_set(out.realtime_departure, json, 'realtimeDeparture')
    out.realtime_departure_actual = __assign_if_set(out.realtime_departure_actual, json, 'realtimeDepartureActual')
    out.realtime_departure_no_report = __assign_if_set(out.realtime_departure_no_report, json, 'realtimeDepartureNoReport')
    out.realtime_wtt_departure_lateness = __assign_if_set(out.realtime_wtt_departure_lateness, json, 'realtimeWttDepartureLateness')
    out.realtime_gbtt_departure_lateness = __assign_if_set(out.realtime_gbtt_departure_lateness, json, 'realtimeGbttDepartureLateness')

    out.platform = __assign_if_set(out.platform, json, 'platform')
    out.platform_confirmed = __assign_if_set(out.platform_confirmed, json, 'platformConfirmed')
    out.platform_changed = __assign_if_set(out.platform_changed, json, 'platformChanged')

    out.line = __assign_if_set(out.line, json, 'line')
    out.line_confirmed = __assign_if_set(out.line_confirmed, json, 'lineConfirmed')

    out.path = __assign_if_set(out.path, json, 'path')
    out.path_confirmed = __assign_if_set(out.path_confirmed, json, 'pathConfirmed')

    out.cancel_reason_code = __assign_if_set(out.cancel_reason_code, json, 'cancelReasonCode')
    out.cancel_reason_short_text = __assign_if_set(
        out.cancel_reason_short_text,
        json,
        'cancelReasonShortText'
    )
    out.cancel_reason_long_text = __assign_if_set(
        out.cancel_reason_long_text,
        json,
        'cancelReasonLongText'
    )

    out.display_as = __assign_if_set(out.display_as, json, 'displayAs')
    out.service_location = __assign_if_set(out.service_location, json, 'serviceLocation')

    return out

def parse_location_container(json: dict) -> LocationContainer:
    """
    Parses a given dictionary (converted from JSON) into a rttapi.model.LocationContainer object

    :param json: The dictionary data to parse

    :raises ValueError: When an expected key is missing

    :return: A rttapi.model.LocationContainer representation of this data
    """
    if not all(key in json for key in ('serviceUid', 'atocCode', 'atocName', 'serviceType', 'isPassenger')):
        raise ValueError("JSON object missing required keys")

    out = LocationContainer()

    out.location_detail = parse_location(json['locationDetail'])
    out.service_uid = json['serviceUid']
    out.run_date = datetime.datetime.strptime(json['runDate'], "%Y-%m-%d").date()

    out.train_identity = __assign_if_set(out.train_identity, json, 'trainIdentity')

    out.running_identity = __assign_if_set(
        out.running_identity,
        json,
        'runningIdentity'
    )

    out.atoc_code = json['atocCode']
    out.atoc_name = json['atocName']
    out.service_type = json['serviceType']
    out.is_passenger = json['isPassenger']

    out.planned_cancel = __assign_if_set(
        out.planned_cancel,
        json,
        'plannedCancel'
    )

    out.countdown_minutes = __assign_if_set(
        out.countdown_minutes,
        json,
        'countdownMinutes'
    )

    if _has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    if _has_value(json, 'destination'):
        out.destination = list(map(parse_pair, json['destination']))

    return out

def parse_service(json: dict):
    """
    Parses a given dictionary (converted from JSON) into a rttapi.model.Service object

    :param json: The dictionary data to parse

    :raises ValueError: When an expected key is missing

    :return: A rttapi.model.Service representation of this data
    """

    if 'error' in json:
        raise ValueError(json['error'])

    out = Service()

    out.service_uid = json['serviceUid']
    out.run_date = datetime.datetime.strptime(json['runDate'], "%Y-%m-%d").date()
    out.service_type = json['serviceType']
    out.is_passenger = json['isPassenger']
    out.train_identity = json['trainIdentity']
    out.atoc_code = json['atocCode']
    out.atoc_name = json['atocName']

    out.power_type = __assign_if_set(
        out.power_type, json, 'powerType'
    )
    out.train_class = __assign_if_set(
        out.train_class, json, 'trainClass'
    )
    out.sleeper = __assign_if_set(
        out.sleeper, json, 'sleeper'
    )
    out.performance_monitored = __assign_if_set(
        out.performance_monitored, json, 'performanceMonitored'
    )

    if _has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    if _has_value(json, 'destination'):
        out.destination = list(map(parse_pair, json['destination']))

    if _has_value(json, 'locations'):
        out.locations = list(map(parse_location, json['locations']))

    out.realtime_activated = __assign_if_set(
        out.realtime_activated, json, 'realtimeActivated'
    )

    out.running_identity = __assign_if_set(
        out.realtime_activated, json, 'runningIdentity'
    )

    return out


def _has_value(json, key):
    """
    Helper method for determining if a key exists within a given dictionary

    :param json: The JSON data (as a dict) to search through
    :param key: The key to search for

    :return: True if key is found in json, False if not.
    """
    return key in json and json[key] is not None

def __assign_if_set(old_val, json, key):
    """
    Helper method for returning the value of a dictionary entry if it exists,
    and returning a default value if not

    :param old_val: The default to return if key is not found in json.
                    Typically the current assignment of the variable this
                    function is being used against.
    :param json:
    :param key:

    :return:
    """
    if key in json and json[key] is not None:
        return json[key]
    else:
        return old_val