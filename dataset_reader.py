"""
Module contains function for reading dataset.
"""

import re
from collections import defaultdict

def extaract_data(line: str) -> tuple[str]:
    """
    Function returns important data from line.

    line: line from dataset
    """
    line = re.sub(r'\{[^{}]*\}', '', line)
    line = re.sub(r'\"[^""]*\"', '', line)
    line = re.sub(r'[()]', "|", line)

    year, location = [part.strip() for part in line.split("|")[1:3]]
    return (year, location)

def read_dataset(dataset_path: str) -> dict[int, set]:
    """
    Function reads locations of
    films and groups them by release year.

    dataset_path: path to dataset
    """
    result = defaultdict(set)

    with open(dataset_path, "rb") as file:
        for line in file.readlines():
            try:
                line = line.decode()
            except UnicodeDecodeError:
                continue

            if not line.startswith("\""):
                continue

            year, location = extaract_data(line)
            result[year].add(location)

    return result
