import itertools
import string
from typing import Iterator

VALUES = dict(zip(string.ascii_letters, range(1, 53)))


def split_in_half(s: str) -> tuple[str, str]:
    if s := s.replace("\n", ""):
        middle = len(s) // 2
        return s[:middle], s[middle:]


with open("day3-input.txt") as f:
    bags = [split_in_half(line) for line in f]

# find common items
common = [list(set(part_a).intersection(set(part_b)))[0] for part_a, part_b in bags]
common_value = [VALUES[item] for item in common]

# get sum of duplicated items
print(sum(common_value))


# PART 2
def grouper(iterator: Iterator, n: int) -> Iterator[list]:
    """take an inter and chunk it into sections of three"""
    while chunk := list(itertools.islice(iterator, n)):
        yield chunk


with open("day3-input.txt") as f:
    grouped_bags = list(grouper(iter(line.replace("\n", "") for line in f), 3))

badges = []
for group in grouped_bags:
    sets = [set(bag) for bag in group]
    found_badge = tuple(sets[0].intersection(sets[1]).intersection(sets[2]))[0]
    badges.append(found_badge)

badge_values = [VALUES[item] for item in badges]
print(sum(badge_values))
