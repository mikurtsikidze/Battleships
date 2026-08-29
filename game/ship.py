from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class Ship:
    name: str
    size: int
    orientation: Orientation = Orientation.HORIZONTAL
    positions: list[tuple[int, int]] = field(default_factory=list)
    hits: set[tuple[int, int]] = field(default_factory=set)

    def place(
        self,
        row: int,
        column: int,
        orientation: Orientation | None = None,
    ) -> None:
        if orientation is not None:
            self.orientation = orientation

        if self.orientation == Orientation.HORIZONTAL:
            self.positions = [
                (row, column + offset)
                for offset in range(self.size)
            ]
        else:
            self.positions = [
                (row + offset, column)
                for offset in range(self.size)
            ]

        self.hits.clear()

    def register_hit(self, row: int, column: int) -> bool:
        position = (row, column)

        if position not in self.positions:
            return False

        self.hits.add(position)
        return True

    def contains(self, row: int, column: int) -> bool:
        return (row, column) in self.positions

    @property
    def is_placed(self) -> bool:
        return len(self.positions) == self.size

    @property
    def is_sunk(self) -> bool:
        return self.is_placed and len(self.hits) == self.size

    @property
    def remaining_health(self) -> int:
        return self.size - len(self.hits)

    def rotate(self) -> None:
        if self.orientation == Orientation.HORIZONTAL:
            self.orientation = Orientation.VERTICAL
        else:
            self.orientation = Orientation.HORIZONTAL