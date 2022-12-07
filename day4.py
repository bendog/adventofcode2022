import csv

with open("day4-input.csv") as f:
    data = list(csv.reader(f))
    data = [([int(x) for x in cell.split("-")] for cell in row) for row in data]


def is_inside(smaller, bigger) -> bool:
    """ check to see if smaller is inside bigger"""
    return smaller[0] >= bigger[0] and bigger[1] >= smaller[1]


def no_overlap(first, second) -> bool:
    """check to see if overlap"""
    return first[1] < second[0] or second[1] < first[0]


inside = 0
overlap = 0
for x, y in data:
    if is_inside(x, y) or is_inside(y, x):
        inside += 1
    if not no_overlap(x, y):
        overlap += 1

print(inside)
print(overlap)
