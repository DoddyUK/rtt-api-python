from rttapi.model import *


def parse_search(json) -> SearchResult:
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
    if not all(key in json for key in ('name', 'crs', 'tiploc')):
        raise ValueError("JSON object missing required keys")

    return LocationDetail(
        json['name'],
        json['crs'],
        json['tiploc']
    )

def parse_pair(json: dict) -> Pair:
    if not all(key in json for key in ('tiploc', 'description', 'workingTime', 'publicTime')):
        raise ValueError("JSON object missing required keys")

    out = Pair()
    out.tiploc = json['tiploc']
    out.description = json['description']
    out.working_time = json['workingTime']
    out.public_time = json['publicTime']

    return out

def parse_location(json: dict) -> Location:
    out = Location()

    out.realtime_activated = __assign_if_set(out.realtime_activated, json, 'realtimeActivated')
    out.tiploc = __assign_if_set(out.tiploc, json, 'tiploc')
    out.crs = json['crs']
    out.description = __assign_if_set(out.description, json, 'description')

    out.wtt_booked_arrival = __assign_if_set(out.wtt_booked_arrival, json, 'wttBookedArrival')
    out.wtt_booked_departure = __assign_if_set(out.wtt_booked_departure, json, 'wttBookedDeparture')
    out.wtt_booked_pass = __assign_if_set(out.wtt_booked_pass, json, 'wttBookedPass')

    out.gbbt_booked_arrival = __assign_if_set(out.gbbt_booked_arrival, json, 'gbbtBookedArrival')
    out.gbbt_booked_departure = __assign_if_set(out.gbbt_booked_departure, json, 'gbbtBookedDeparture')

    if has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    if has_value(json, 'destination'):
        out.destination = list(map(parse_pair, json['destination']))

    out.realtime_arrival = __assign_if_set(out.realtime_arrival, json, 'realtimeArrival')
    out.realtime_arrival_actual = __assign_if_set(out.realtime_arrival_actual, json, 'realtimeArrivalActual')
    out.realtime_arrival_no_report = __assign_if_set(out.realtime_arrival_no_report, json, 'realtimeArrivalNoReport')
    out.realtime_wtt_arrival_lateness = __assign_if_set(out.realtime_wtt_arrival_lateness, json, 'realtimeWttArrivalLateness')
    out.realtime_gbbt_arrival_lateness = __assign_if_set(out.realtime_gbbt_arrival_lateness, json, 'realtimeGbttArrivalLateness')

    out.realtime_departure = __assign_if_set(out.realtime_departure, json, 'realtimeDeparture')
    out.realtime_departure_actual = __assign_if_set(out.realtime_departure_actual, json, 'realtimeDepartureActual')
    out.realtime_departure_no_report = __assign_if_set(out.realtime_departure_no_report, json, 'realtimeDepartureNoReport')
    out.realtime_wtt_departure_lateness = __assign_if_set(out.realtime_wtt_departure_lateness, json, 'realtimeWttDepartureLateness')
    out.realtime_gbbt_departure_lateness = __assign_if_set(out.realtime_gbbt_departure_lateness, json, 'realtimeGbttDepartureLateness')

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
    out = LocationContainer()

    out.location_detail = parse_location(json['locationDetail'])
    out.service_uid = json['serviceUid']
    out.run_date = datetime.datetime.strptime(json['runDate'], "%Y-%m-%d").date()

    out.train_identity = __assign_if_set(out.train_identity, json, 'trainIdentity')
    out.running_identity = __assign_if_set(out.running_identity, json, 'runningIdentity')

    out.atoc_code = json['atocCode']
    out.atoc_name = json['atocName']
    out.service_type = json['serviceType']
    out.is_passenger = json['isPassenger']

    out.planned_cancel = __assign_if_set(out.planned_cancel, json, 'plannedCancel')
    out.countdown_minutes = __assign_if_set(out.countdown_minutes, json, 'countdownMinutes')

    if has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    if has_value(json, 'destination'):
        out.origin = list(map(parse_pair, json['destination']))

    return out

def has_value(json, key):
    return key in json and json[key] is not None

def __assign_if_set(old_val, json, key):
    if key in json and json[key] is not None:
        return json[key]
    else:
        return old_val