from abc import ABC, abstractmethod


class Curve(ABC):
    def __init__(self, control_points) -> None:
        self.control_points = control_points

    @abstractmethod
    def get_points(self, num_points=100) -> list:
        pass
