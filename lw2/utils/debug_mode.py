from typing import Generator


class StepDebugger:
    def __init__(self, generator: Generator[dict, None, None]) -> None:
        self.steps: list = list(generator)
        self.index: int = 0

    def current(self) -> list:
        points = []
        for i in range(self.index + 1):
            points.extend(self.steps[i]['points'])
        return points

    def next(self) -> list:
        if self.index < len(self.steps) - 1:
            self.index += 1
        return self.current()

    def prev(self) -> list:
        if self.index > 0:
            self.index -= 1
        return self.current()

    def reset(self):
        self.index = 0
        return self.current()
