"""
Module to create map.
"""

from random import uniform
from math import sqrt, sin, cos, radians, asin
from collections import Counter

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

    point1: first point
    point2: second point
    """
    if not point1 or not point2:
        return float("inf")

    lat1, lon1 = point1
    lat2, lon2 = point2

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    num = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return asin(sqrt(num))

def get_coordinates(location: str) -> tuple[float, float]:
    """
    Function returns coodrinated of location by address name.

    location: location name
    """
    try:
        coords = geolocator.geocode(location)
    except (GeocoderUnavailable, GeocoderTimedOut) as error:
        print(f"Error {error} in: {location}")
        coords = None

    return (coords.latitude, coords.longitude) if coords else None

def unificate_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Function unificate points with same coordinates.

    points: list of points
    """
    distribution = 0.001
    unificate = []
    counts = Counter(points)

    for point in points:
        if counts[point] != 1:
            delta_x = uniform(-distribution, distribution)
            delta_y = uniform(-distribution, distribution)
            point = (point[0] + delta_x, point[1] + delta_y)

            unificate.append(point)

    return unificate

def nearest_points(
    origin: tuple[float, float],
    locations: list[str],
    n_first: int) -> list[tuple[float, float]]:
    """
    Function returns n_first nearest
    points to origin.

    origin: origin point
    locations: list of locations
    n_first: number of nearest points
    """
    locations = [get_coordinates(location) for location in locations]
    locations.sort(key=lambda location: distance(origin, location))
    locations = unificate_points(locations)

    return locations[:min(n_first, len(locations))]

def create_map(
    dest: str,
    user_coords: tuple[float, float],
    points: list[tuple[int, int]]) -> None:
    """
    Function writes map in .html file.

    dest: path to map file
    user_coords: user coordinates
    points: list of points to show on map
    """
    wmap = folium.Map(location=list(user_coords), zoom_start=10)
    fgroup = folium.FeatureGroup(name="World map")

    for lat, lon in points:
        fgroup.add_child(folium.Marker(location=[lat, lon], icon=folium.Icon()))

    wmap.add_child(fgroup)
    wmap.save(dest)
