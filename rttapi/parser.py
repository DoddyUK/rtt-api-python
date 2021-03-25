from rttapi.model import SearchResult, LocationDetail, RttPair, Location


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
        out.services = list(map(parse_location, json['services']))

    return out

def parse_location_detail(json: dict) -> LocationDetail:
    if not all(key in json for key in ('name', 'crs', 'tiploc')):
        raise ValueError("JSON object missing required keys")

    return LocationDetail(
        json['name'],
        json['crs'],
        json['tiploc']
    )

def parse_pair(json: dict) -> RttPair:
    if not all(key in json for key in ('tiploc', 'description', 'workingTime', 'publicTime')):
        raise ValueError("JSON object missing required keys")

    out = RttPair()
    out.tiploc = json['tiploc']
    out.description = json['description']
    out.working_time = json['workingTime']
    out.public_time = json['publicTime']

    return out

def parse_location(json: dict) -> Location:
    out = Location()
    location_detail = json['locationDetail']

    if has_value(location_detail, 'origin'):
        out.origin = list(map(parse_pair, location_detail['origin']))

    return out


def has_value(json, key):
    return key in json and json[key] is not None