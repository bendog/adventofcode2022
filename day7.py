import re
from dataclasses import dataclass, field


@dataclass
class Folder:
    name: str
    size: int = 0
    contents: list = field(default_factory=list)


PATTERN = re.compile(r"(\d+) \w+\.?\w*")


def process_children(current_folder: Folder, content: iter):
    for line in content:
        line = line.replace("\n", "")
        if line == "$ cd ..":
            return current_folder.size
        elif line[:5] == "$ cd ":
            child = Folder(f"{current_folder.name}/{line[5:]}")
            current_folder.size += process_children(child, content)
            current_folder.contents.append(child)
        elif match := PATTERN.search(line):
            size = match.group(1)
            current_folder.size += int(size)
    return current_folder.size


with open("day7-input.txt") as f:
    root = Folder("/")
    next(f)
    process_children(root, f)
    print(root.size)

# def get_unique_size(current_folder):
#     if current_folder.size > 100000:
#         for folder in current_folder.contents:
#             get_unique_size(folder)
#     else:
#         found_folder_size.append(current_folder.size)


found_folder_size = []


def get_size(current_folder):
    if current_folder.size <= 100000:
        found_folder_size.append(current_folder.size)
    for folder in current_folder.contents:
        get_size(folder)


get_size(root)
print(sum(found_folder_size))

### PART 2 ###


FLAT_FOLDERS = {}


def flatten_folders(current_folder):
    FLAT_FOLDERS[current_folder.name] = current_folder.size
    for folder in current_folder.contents:
        flatten_folders(folder)


flatten_folders(root)

TOTAL_DISK = 70000000
REQUIRED_DISK = 30000000

available_disk = TOTAL_DISK - root.size
required_to_free = REQUIRED_DISK - available_disk

folders_large_enough = [val for val in FLAT_FOLDERS.values() if val > required_to_free]
folders_large_enough.sort()
print(folders_large_enough[0])
folder_name = list(FLAT_FOLDERS.keys())[list(FLAT_FOLDERS.values()).index(folders_large_enough[0])]
print(folder_name)
