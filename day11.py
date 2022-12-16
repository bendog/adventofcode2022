import math
import time
from dataclasses import dataclass, field
from typing import Callable

WORRY_LEVEL: int = 3


@dataclass
class Item:
    name: str
    worry_value: int

    # monkey_history: list[Monkey] = field(default_factory=list)
    #
    # @property
    # def held_by(self):
    #     """ currently held by """
    #     return self.monkey_history[-1] if self.monkey_history else None


@dataclass
class Monkey:
    name: str
    operation: Callable[[int], int]
    # an operation takes one value, and returns a calculation
    test: Callable[[int], str | None]
    # a test should take a float, and return None or the name of a monkey depending on if true or false
    items: list[Item] = field(default_factory=list)
    # inspected: list[str] = field(default_factory=list)
    inspected_count = 0

    def __str__(self):
        return f"Monkey {self.name} count:{self.inspected_count} items:{','.join(str(item.worry_value) for item in self.items)}"

    def add_item(self, name: str, worry_level: int):
        self.items.append(Item(name, worry_level))

    def inspect_all_items(self):
        while self.items:
            self.inspect(self.items.pop(0))

    def inspect(self, item):
        """monkey inspects the item"""
        # self.inspected.append(str(item))
        self.inspected_count += 1
        item.worry_value = self.operation(item.worry_value)
        if WORRY_LEVEL != 1:
            item.worry_value = item.worry_value // WORRY_LEVEL
        monkey_to_throw = self.test(item.worry_value)
        item.worry_value %= COMMON_MULTIPLE
        for m in MONKEY_LIST:
            if m.name == monkey_to_throw:
                m.items.append(item)


MONKEY_LIST: list[Monkey] = []


def initilise_monkeys() -> tuple[list[Monkey], list[int]]:
    monkey_list = []
    divisor_primes = []
    with open("input/day11.txt") as f:
        for line in list(f.readlines()) + ["\n"]:
            if line[:7] == "Monkey ":
                monkey_name = line[7 : line.find(":")]
            elif line[:18] == "  Starting items: ":
                starting_items = [int(x) for x in line[18 : line.find("\n")].split(", ")]
            elif line[:19] == "  Operation: new = ":
                operation_str = "lambda old: " + line[19 : line.find("\n")]
            elif line[:21] == "  Test: divisible by ":
                divisor = int(line[21 : line.find("\n")])
                test_str = f"x % {divisor} == 0"
                divisor_primes.append(divisor)
            elif line[:29] == "    If true: throw to monkey ":
                true_monkey = line[29 : line.find("\n")]
            elif line[:30] == "    If false: throw to monkey ":
                false_monkey = line[30 : line.find("\n")]
            else:
                # build monkey
                full_test = f"lambda x: '{true_monkey}' if {test_str} else '{false_monkey}'"
                monkey = Monkey(monkey_name, eval(operation_str), eval(full_test))
                for idx, worry in enumerate(starting_items):
                    monkey.add_item(f"{monkey_name}:{idx}", worry)
                print(monkey)
                monkey_list.append(monkey)
                # reset values
                monkey = None
                monkey_name = None
                starting_items = []
                operation = None
                test_str = None
                true_monkey = None
                false_monkey = None
    return monkey_list, divisor_primes


print(MONKEY_LIST)

###
# PART 1
###

print("*" * 20, " part 1 ", "*" * 20)

ROUNDS = 20
MONKEY_LIST, div_by_list = initilise_monkeys()
COMMON_MULTIPLE = math.prod(div_by_list)


for _ in range(1, ROUNDS + 1):
    for monkey in MONKEY_LIST:
        monkey.inspect_all_items()


for monkey in MONKEY_LIST:
    print(f"Monkey {monkey.name} inspected items {monkey.inspected_count}")

monkey_inspected_count = [monkey.inspected_count for monkey in MONKEY_LIST]
monkey_inspected_count.sort()
print(f"Monkey Business: {str(math.prod(monkey_inspected_count[-2:]))}")

###
# PART 2
###


print("*" * 20, " part 2 ", "*" * 20)

WORRY_LEVEL = 1
ROUNDS = 10000
# ROUNDS = 900
CHECK_INTERVAL = 1000
MONKEY_LIST, div_by_list = initilise_monkeys()
COMMON_MULTIPLE = math.prod(div_by_list)

start = time.process_time()
for round_num in range(1, ROUNDS + 1):
    if round_num % CHECK_INTERVAL == 0:
        print(
            f"  {round_num=} ({(time.process_time() - start) / CHECK_INTERVAL:.3f} seconds per round)"
        )
        print(f"  round:{round_num}")
        for monkey in MONKEY_LIST:
            print(f"    {str(monkey)}")
        start = time.process_time()
    for monkey in MONKEY_LIST:
        monkey.inspect_all_items()

for monkey in MONKEY_LIST:
    print(f"Monkey {monkey.name} inspected items {monkey.inspected_count}")

monkey_inspected_count = [monkey.inspected_count for monkey in MONKEY_LIST]
monkey_inspected_count.sort()
print(f"Monkey Business: {str(math.prod(monkey_inspected_count[-2:]))}")
