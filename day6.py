with open("day6-input.txt") as f:
    data = f.read().replace("\n", "")


def find_unique_chunk(content: str, length: int):
    for idx in range(len(content)):
        segment = content[idx : idx + length]
        if len(segment) == len(set(segment)):
            return idx + length, segment


print(find_unique_chunk(data, 4))

### PART 2 ###

print(find_unique_chunk(data, 14))
