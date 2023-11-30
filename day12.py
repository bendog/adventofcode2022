from dataclasses import dataclass
from string import ascii_lowercase


@dataclass
class Coordinate:
    x: int
    y: int

    @property
    def height(self) -> int | None:
        """ return height if available """
        if -1 < self.x < len(DATA[0]) and -1 < self.y < len(DATA):
            return DATA[self.y][self.x]
        return None

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"{self.x},{self.y}:{self.height}"

    def __hash__(self):
        return self.x * 1000000 + self.y


def import_data(file_name) -> tuple[list[list[int]], Coordinate, Coordinate]:
    """ takes filename, returns matrix of heights, start and end coordinates"""
    with open(file_name) as f:
        _data = []
        _start = None
        _finish = None
        for idy, row in enumerate(f):
            data_row = []
            for idx, col in enumerate(row.replace("\n", "")):
                if col in ascii_lowercase:
                    data_row.append(ascii_lowercase.index(col)+1)
                elif col == 'S':
                    # this is the start
                    _start = Coordinate(idx, idy)
                    data_row.append(ascii_lowercase.index('a')+1)
                elif col == 'E':
                    # this is the end
                    data_row.append(ascii_lowercase.index('z')+1)
                    _finish = Coordinate(idx, idy)
            _data.append(data_row)
    return _data, _start, _finish


DATA, START, FINISH = import_data('input/day12.txt')
MAX_STEPS = 2000


def find_path(start: Coordinate, finish: Coordinate, step_size: int = 1) -> list[Coordinate]:
    # seen: dict[Coordinate: int] = {start: 0}
    process_queue: list[list[Coordinate]] = [[start]]
    max_length = MAX_STEPS
    solution: list[Coordinate] = []
    # check north
    while process_queue:
        current_path: list[Coordinate] = process_queue.pop(0)
        if current_path is None:
            raise IndexError("not current_path")
        if len(current_path) >= max_length:
            # skip if this list is longer than the shortest solved path
            continue
        my_loc: Coordinate = current_path[-1]
        # 20:122
        if finish.y-10 < my_loc.y < finish.y+10 and finish.x-10 < my_loc.x < finish.x+10:
            print(f"    close   : {my_loc}")
        if my_loc == finish:
            max_length = len(current_path)
            solution = current_path
        check_direction = (
            Coordinate(my_loc.x, my_loc.y - 1),  # north
            Coordinate(my_loc.x + 1, my_loc.y),  # east
            Coordinate(my_loc.x, my_loc.y + 1),  # south
            Coordinate(my_loc.x - 1, my_loc.y),  # west
        )
        # filter out seen and off map
        check_direction = [loc for loc in check_direction if loc.height is not None and loc not in current_path]
        if not check_direction:
            max_height = max(path[-1].height for path in process_queue)
            process_queue_len = len(process_queue)
            print(f"    deadend: {my_loc} ({max_height=} {process_queue_len=} {len(current_path)=}")

            # remove all of this dead end from the process queue
            process_queue = [path for path in process_queue if my_loc not in path]
        for new_loc in check_direction:
            if my_loc.height + step_size >= new_loc.height >= my_loc.height:
                if seen := [path for path in process_queue if new_loc in path]:
                    seen_length = min(path.index(new_loc) for path in seen) + 1
                else:
                    seen_length = 99999999
                # seen_length = seen.get(new_loc, 1000000)
                new_path = [*current_path, new_loc]
                if len(new_path) < seen_length:
                    # if this is currently the shortest path to this node
                    # remove all other paths to this node
                    # seen[new_loc] = len(new_path)
                    process_queue = [path for path in process_queue if new_loc not in path]
                    process_queue.append(new_path)
        process_queue.sort(key=lambda x: len(x), reverse=False)
    if solution:
        return solution
    raise Exception("not found")

    # my_loc = my_path[-1]
    # if my_loc == finish:
    #     MAX_LENGTH = len(my_path)
    #     print(f"found path: {len(my_path)}")
    #     return my_path
    # check_direction = (
    #     Coordinate(my_loc.x, my_loc.y - 1),  # north
    #     Coordinate(my_loc.x + 1, my_loc.y),  # east
    #     Coordinate(my_loc.x, my_loc.y + 1),  # south
    #     Coordinate(my_loc.x - 1, my_loc.y),  # west
    # )
    # results = []
    # check_order = []
    # for new_loc in check_direction:
    #     # new_height = new_loc.height
    #     # my_height = my_loc.height
    #     if new_loc.height is not None and new_loc not in my_path and my_loc.height + 2 > new_loc.height >= my_loc.height:
    #         if new_loc.height > my_loc.height:
    #             # prioritise higher options
    #             check_order.insert(0, new_loc)
    #         else:
    #             check_order.append(new_loc)
    #     else:
    #         results.append([])
    # results.extend(find_path(my_path + [new_loc]) for new_loc in check_order)
    # results.sort(key=len)
    # filtered_results = [r for r in results if r]
    # return filtered_results[0] if filtered_results else []


found_path = find_path(START, FINISH)
print(found_path)
print("Number of steps: ", len(found_path) - 1)
