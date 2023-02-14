"""
Module to create map.
"""

from math import pi, sqrt, atan2, sin, cos

import folium
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="pn-lab1-task2")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """
    Function calculates distance between two points on a map.
    This function have only to estimate distance.
    """
    pi_180 = pi / 180

    fi1 = point1[0] * pi_180
    fi2 = point2[0] * pi_180

    delta_fi = fi2 - fi1
    delta_lambda = (point2[1] - point1[1]) * pi_180

    number = sin(delta_fi/2) * sin(delta_fi / 2) +\
        cos(fi2) * cos(fi2) *\
        sin(delta_lambda / 2) * sin(delta_lambda / 2)

    return 2 * atan2(sqrt(number), sqrt(1 - number))

def get_coordinates(location: str) -> tuple[float, float]:
    """
    Function returns coodrinated of location by address name.
    """
    try:
        coords = geolocator.geocode(location)
    except (GeocoderUnavailable, GeocoderTimedOut) as error:
        print(f"Error {error} in: {location}")
        coords = None

    return (coords.latitude, coords.longitude) if coords else (float("inf"), float("inf"))

def nearest_points(
    origin: tuple[float, float],
    locations: list[str],
    n_first: int) -> list[tuple[float, float]]:
    """
    Function returns n_first nearest
    points to origin
    """
    locations = list(map(get_coordinates, locations))
    locations.sort(key=lambda location: distance(origin, location))
    return locations[:n_first]

def create_map(
    dest: str,
    user_coords: tuple[float, float],
    points: list[tuple[int, int]]) -> None:
    """
    Function writes map in .html file.
    """
    wmap = folium.Map(location=list(user_coords), zoom_start=10)
    fgroup = folium.FeatureGroup(name="World map")

    for lat, lon in points:
        fgroup.add_child(folium.Marker(location=[lat, lon], icon=folium.Icon()))

    wmap.add_child(fgroup)
    wmap.save(dest)
