"""
Module for generating shorter dataset.
"""

from random import choice

def shrink_dataset(src: str, lines: int, dest: str) -> None:
    """
    Function shrinks dataset.
    """
    data = []
    with open(src, "rb") as file:
        data = file.readlines()

    new_data = []
    rng = list(range(len(data)))

    for _ in range(lines):
        chs = choice(rng)
        rng.remove(chs)

        new_data.append(data[chs])

    with open(dest, "wb") as file:
        file.writelines(new_data)
