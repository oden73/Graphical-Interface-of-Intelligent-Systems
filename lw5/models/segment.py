from PyQt5.QtCore import QPointF
from typing import Tuple


class Segment:
    start: QPointF
    end: QPointF

    def __init__(self, start: QPointF, end: QPointF) -> None:
        self.start: QPointF = start
        self.end: QPointF = end

    def as_tuple(self) -> Tuple[QPointF, QPointF]:
        return self.start, self.end
