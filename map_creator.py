"""
Module to create map.
"""

from random import uniform
from math import sqrt, sin, cos, radians, asin
from collections import Counter

import folium
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="movie-near")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """
    Function calculates distance between two points on a map.
    This function have only to estimate distance.

    point1: first point
    point2: second point
    >>> distance((0, 0), (0, 0))
    0.0
    >>> distance((0, 0), (0, 1))
    111194.92664455874
    """
    if not point1 or not point2:
        return float("inf")

    lat1, lon1 = point1
    lat2, lon2 = point2

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    num = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return asin(sqrt(num)) * 2 * 6371e3

def get_coordinates(location: str) -> tuple[float, float]:
    """
    Function returns coodrinated of location by address name.

    location: location name
    >>> list(map(int, get_coordinates("Ternopil, Ukraine")))
    [49, 25]
    >>> list(map(int, get_coordinates("Kiev, Ukraine")))
    [50, 30]
    >>> get_coordinates("")
    """
    try:
        coords = geolocator.geocode(location)
    except (GeocoderUnavailable, GeocoderTimedOut, GeocoderServiceError) as error:
        print(f"Error {error.strerror} in: {location}")
        coords = None

    return (coords.latitude, coords.longitude) if coords else None

def unificate_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Function unificate points with same coordinates.
    Also functuion removes points with None coordinates.

    points: list of points
    >>> len(unificate_points([(0, 0), None])) == 1
    True
    """
    distribution = 0.005
    unificated = []
    counts = Counter(points)

    for point in points:
        if not point:
            continue

        if counts[point] != 1:
            delta_x = uniform(-distribution, distribution)
            delta_y = uniform(-distribution, distribution)
            point = (point[0] + delta_x, point[1] + delta_y)

        unificated.append(point)

    return unificated

def nearest_points(
    origin: tuple[float, float],
    locations: list[str],
    n_first: int) -> list[tuple[float, float]]:
    """
    Function returns n_first nearest points to origin.

    origin: origin point
    locations: list of locations
    n_first: number of nearest points

    >>> pnt = nearest_points((49.553802, 25.594092),\
    ["Paris, France", "Kiev, Ukraine"], 1)[0]
    >>> list(map(int, pnt)) == [50, 30]
    True
    """
    locations = [get_coordinates(location) for location in locations]
    locations = unificate_points(locations)
    locations.sort(key=lambda location: distance(origin, location))

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
    
    >>> create_map("", (49.553802, 25.594092), [(50.4501, 30.5234)])
    Error: invalid destination path
    """
    if not isinstance(dest, str) or len(dest) == 0:
        print("Error: invalid destination path")
        return

    wmap = folium.Map(location=list(user_coords), zoom_start=10)

    main_group = folium.FeatureGroup(name="World map")
    markers_group = folium.FeatureGroup(name="Markers")
    ragius_group = folium.FeatureGroup(name="Radius")

    # draw radius from user to farthest point
    ragius_group.add_child(folium.Circle(
        location=[user_coords[0], user_coords[1]],
        radius=distance(user_coords, points[-1]) + 1e5,
        color="green",
        fill=True,
        fill_color="green"
    ))

    # add user marker
    markers_group.add_child(folium.Marker(
        location=[user_coords[0], user_coords[1]],
        icon=folium.Icon(color="red")
    ))

    # add films markers
    for lat, lon in points:
        markers_group.add_child(folium.Marker(location=[lat, lon], icon=folium.Icon()))

    wmap.add_child(ragius_group)
    wmap.add_child(main_group)
    wmap.add_child(markers_group)

    wmap.save(dest)

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
