# realtime-trains-api-python README

A Python wrapper for the [Realtime Trains](https://www.realtimetrains.co.uk/) API v1.

This library simplfies the process of making a call to the Realtime Trains API.
Requests to specific endpoints can be made from the `RttApi` class, with the returned
JSON data parsed and wrapped into a data object.

For now this is a literal mapping of the Realtime Trains API data structure into Python
data classes. Helper functionality may be added in future.

## Prerequisites
In order to make requests from this library you must first sign up for a Realtime Trains
API account. You can do so at [api.rtt.io](https://api.rtt.io/). 

## Getting Started
**IMPORTANT** - Note that you must use 
the **API Auth Credentials** as displayed within your Realtime Trains API account, **not**
the credentials you use to log into the website.

Create an instance of an `RttApi` object using your Realtime Trains API auth credentials 
like so:

```python
from rttapi.api import RttApi

api = RttApi('rttapi_exampleuser', '00112233aabbccdd')
```

## Request Station Information

To request the list of upcoming departures from Clapham Junction station:

```python
departures = api.search_station_departures('CLJ') 
```

This will return a `SearchResult` object with containing the station details and the list of
upcoming departures. You may either search using the three-letter CRS (computer reservation system)
code, or a longer TIPLOC (timing point location) code. You can find a station's CRS code by 
searching on the [National Rail website](https://www.nationalrail.co.uk/).

Arrivals can also be queried by using:

```python
arrivals = api.search_station_arrivals('CLJ') 
```

Which again returns a `SearchResult` object.

A detailed breakdown on the information returned can be found on the Realtime Trains
[API documentation page](https://www.realtimetrains.co.uk/about/developer/pull/docs/locationlist/).
This library mirrors the data returned by the API, albeit using Pythonesque `underscore_case`
properties instead of the `camelCase` properties returned by the API.

## Request Detailed Service Information

Detailed journey information for an individual service can be queried using:

```python
service_info = api.fetch_service_info_datetime(service_uid, service_date) 
```

where: 
* `service_uid` is the unique identifier of the service obtained from the `SearchResult`
e.g. `8U09FW` 
* `service_datetime` is a `datetime.date` object representing the date on 
which the service is due to depart. 

Alternatively, the year, month and day of departure can
be explicitly set (e.g. 27th March 2021) by using:

```python
service_info = api.fetch_service_info_ymd('8U09FW', '2021', '3', '27') 
```

Both of these examples will return a `Service` object, which is explained in more detail
on the Realtime Trains [API documentation page](https://www.realtimetrains.co.uk/about/developer/pull/docs/serviceinfo/).


## Other Examples
A more detailed example on how to use this library can be found in my 
[pyRailTimes](https://github.com/DoddyUK/pyRailTimes) project.

## Thanks
With thanks to the Realtime Trains API team.