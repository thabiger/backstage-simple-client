
from typing import List

def flatten(l: List) -> List:
    """Flatten a list of lists."""

    r = []

    for item in l:
        if isinstance(item, list):
            r.extend(item)
        else:
            r.append(item)
    return r

    #return [item for sublist in l for item in sublist if isinstance(sublist, list)]

def remove_false_and_none(lst: list) -> list:
    return [value for value in lst if value not in (False, None)]