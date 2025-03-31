from abc import ABC, abstractmethod
from typing import Generator


class Curve(ABC):
    required_params: list = []

    def __init__(self) -> None:
        self.parameters: dict[str, any] = {}

    @abstractmethod
    def get_points(self) -> list[tuple[int, int]]:
        # list of points for displaying the curve
        pass

    @abstractmethod
    def step_by_step(self) -> Generator[dict, None, None]:
        # generator for steps of the algorithm
        yield {}
