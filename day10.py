class Cpu:
    def __init__(self):
        self.register_x = 1
        self.cycle = 0
        self.monitor_cycle = 20
        self.monitor_cycle_interval = 40
        self.monitor_history: list[int] = []
        self.crt = []

    def run_clock(self, cycles: int):
        for _ in range(cycles):
            self.draw()
            self.cycle += 1
            if self.cycle == self.monitor_cycle:
                self.log_signal_strength()
                self.monitor_cycle += self.monitor_cycle_interval

    def process(self, command: str):
        if command == "noop":
            self.run_clock(1)
        elif command[:4] in ("addx"):
            self.run_clock(2)
            instruction, value = command.split()
            self.register_x += int(value)
        return

    def load(self, instructions: list[str]):
        for command in instructions:
            self.process(command)

    def log_signal_strength(self):
        print(f"{self.cycle=} {self.register_x=} : {self.cycle * self.register_x}")
        self.monitor_history.append(self.cycle * self.register_x)

    @property
    def crt_position(self):
        return len(self.crt) % 40

    def draw(self):
        """part 2 - add a pixel to the CRT"""
        if self.register_x - 1 <= self.crt_position <= self.register_x + 1:
            self.crt.append("#")
        else:
            self.crt.append(".")

    @property
    def crt_output(self) -> str:
        """display the crt to a string"""
        screen_size = 40
        output = [
            "".join(self.crt[i : i + screen_size]) for i in range(0, len(self.crt), screen_size)
        ]
        return "\n".join(output)


with open("day10-input.txt") as f:
    data = [row.replace("\n", "") for row in f]

cpu = Cpu()
cpu.load(data)

print(sum(cpu.monitor_history))

print(cpu.crt_output)
