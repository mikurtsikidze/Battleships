from __future__ import annotations

from enum import Enum

from game.ship import Ship


class ShotResult(Enum):
    HIT = "hit"
    MISS = "miss"
    SUNK = "sunk"
    ALREADY_SHOT = "already_shot"


class Board:
    SIZE = 10

    def __init__(self) -> None:
        self.ships: list[Ship] = []
        self.shots: set[tuple[int, int]] = set()

    def is_valid_position(
        self,
        ship: Ship,
        row: int,
        column: int,
    ) -> bool:
        positions = self._get_ship_positions(ship, row, column)

        if any(not self._is_inside_board(position) for position in positions):
            return False

        return not any(
            existing_ship.contains(*position)
            for existing_ship in self.ships
            for position in positions
        )

    def place_ship(
        self,
        ship: Ship,
        row: int,
        column: int,
    ) -> bool:
        if not self.is_valid_position(ship, row, column):
            return False

        ship.place(row, column)
        self.ships.append(ship)

        return True

    def remove_ship(self, ship: Ship) -> bool:
        if ship not in self.ships:
            return False

        self.ships.remove(ship)
        ship.positions.clear()
        ship.hits.clear()

        return True

    def receive_shot(self, row: int, column: int) -> ShotResult:
        position = (row, column)

        if not self._is_inside_board(position):
            raise ValueError("Shot position is outside the board.")

        if position in self.shots:
            return ShotResult.ALREADY_SHOT

        self.shots.add(position)

        for ship in self.ships:
            if ship.register_hit(row, column):
                if ship.is_sunk:
                    return ShotResult.SUNK

                return ShotResult.HIT

        return ShotResult.MISS

    def get_ship_at(
        self,
        row: int,
        column: int,
    ) -> Ship | None:
        for ship in self.ships:
            if ship.contains(row, column):
                return ship

        return None

    @property
    def all_ships_sunk(self) -> bool:
        return bool(self.ships) and all(ship.is_sunk for ship in self.ships)

    def _get_ship_positions(
        self,
        ship: Ship,
        row: int,
        column: int,
    ) -> list[tuple[int, int]]:
        if ship.orientation.value == "horizontal":
            return [
                (row, column + offset)
                for offset in range(ship.size)
            ]

        return [
            (row + offset, column)
            for offset in range(ship.size)
        ]

    def _is_inside_board(
        self,
        position: tuple[int, int],
    ) -> bool:
        row, column = position

        return 0 <= row < self.SIZE and 0 <= column < self.SIZE