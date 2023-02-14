"""
Main module of program.
Reads user input and generates map.
"""

import argparse
from dataset_reader import read_dataset
from map_creator import create_map, nearest_points

parser = argparse.ArgumentParser(
    prog="MovieNear",
    description="Program draw points on map with locations of 10 nearest filming places."
)

parser.add_argument('year', help="Year of release.", type=int)
parser.add_argument('latitude', help="Coordinates latitude.", type=float)
parser.add_argument('longtitude', help="Coordinates latitude.", type=float)
parser.add_argument('dataset', help="Path to films dataset.", type=str)
parser.add_argument('--destination', help="Map destination path.", default="Map.html", type=str)

def main(args: argparse.Namespace) -> None:
    """
    Main function generates map.
    """
    user_coords = (args.latitude, args.longtitude)

    dataset = read_dataset(args.dataset)[str(args.year)]
    points = nearest_points(user_coords, dataset, 10)
    create_map(args.destination, user_coords, points)

if __name__ == "__main__":
    arguments = parser.parse_args()
    main(arguments)
