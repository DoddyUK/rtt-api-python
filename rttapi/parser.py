from rttapi.model import SearchResult, LocationDetail


def parse_search(json) -> SearchResult:
    if not all(key in json for key in ('location', 'filter', 'services')):
        raise ValueError("JSON object missing required keys")

    out = SearchResult()
    out.location = parse_location_detail(json['location'])

    if 'filter' in json and json['filter'] is not None:
        out.filter = parse_location_detail(json['filter'])

    if 'services' in json and json['services'] is not None:
        out.services = parse_services(json['services'])

    return out



def parse_location_detail(json: dict) -> LocationDetail:
    if not all(key in json for key in ('name', 'crs', 'tiploc')):
        raise ValueError("JSON object missing required keys")

    return LocationDetail(
        json['name'],
        json['crs'],
        json['tiploc']
    )

def parse_services(json: dict):
    return ""