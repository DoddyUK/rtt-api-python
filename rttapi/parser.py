from rttapi.model import *


def parse_search(json) -> SearchResult:
    if not all(key in json for key in ('location', 'filter', 'services')):
        raise ValueError("JSON object missing required keys")

    if json['location'] is None:
        raise ValueError("location is None")

    out = SearchResult()
    out.location = parse_location_detail(json['location'])

    if has_value(json, 'filter'):
        out.filter = parse_location_detail(json['filter'])

    if has_value(json, 'services'):
        out.services = list(map(parse_location_container, json['services']))

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

    if has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    return out

def parse_location_container(json: dict) -> LocationContainer:
    out = LocationContainer()

    out.location_detail = parse_location(json['locationDetail'])
    out.service_uid = json['serviceUid']
    out.run_date = datetime.datetime.strptime(json['runDate'], "%Y-%m-%d").date()

    if has_value(json, 'trainIdentity'):
        out.train_identity = json['trainIdentity']
    if has_value(json, 'runningIdentity'):
        out.running_identity = json['runningIdentity']

    out.atoc_code = json['atocCode']
    out.atoc_name = json['atocName']
    out.service_type = json['serviceType']
    out.is_passenger = json['isPassenger']

    if has_value(json, 'plannedCancel'):
        out.planned_cancel = json['plannedCancel']

    if has_value(json, 'origin'):
        out.origin = list(map(parse_pair, json['origin']))

    if has_value(json, 'destination'):
        out.origin = list(map(parse_pair, json['destination']))

    if has_value(json, 'countdownMinutes'):
        out.countdown_minutes = list(map(parse_pair, json['countdownMinutes']))


    return out


def has_value(json, key):
    return key in json and json[key] is not None