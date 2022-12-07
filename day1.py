# GET DATA
data = []
elf = []
with open("day1-input.txt") as f:
    for line in f:
        try:
            elf.append(int(line))
        except ValueError:
            # if type error reset elf
            data.append(elf)
            elf = []
    # extra check to make sure the last elf is counted
    if data[-1] != elf:
        data.append(elf)


# PROCESS DATA
sums = [sum(x) for x in data]
# get most
print(max(sums))
# get sum of three most
print(sum(sorted(sums)[-3:]))
