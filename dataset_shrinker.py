"""
Module for shrinking dataset.
"""

from random import choice

def shrink_dataset(src: str, lines: int, dest: str) -> None:
    """
    Function shrinks dataset.

    src: source dataset file
    lines: size of shrunk dataset
    dest: destination dataset file

    >>> shrink_dataset("", 10, "dataset_shrinked.list")
    Error: invalid source path
    """
    data = []

    try:
        with open(src, "rb") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("Error: invalid source path")
        return

    new_data = []
    rng = list(range(len(data)))

    for _ in range(lines):
        chs = choice(rng)
        rng.remove(chs)

        new_data.append(data[chs])

    with open(dest, "wb") as file:
        file.writelines(new_data)

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
