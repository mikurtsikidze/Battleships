from __future__ import annotations

from game.board import Board, ShotResult


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.board = Board()

    @property
    def ships(self):
        return self.board.ships

    @property
    def remaining_ships(self) -> int:
        return sum(
            not ship.is_sunk
            for ship in self.board.ships
        )

    @property
    def has_lost(self) -> bool:
        return self.board.all_ships_sunk

    def shoot(
        self,
        opponent: Player,
        row: int,
        column: int,
    ) -> ShotResult:
        return opponent.board.receive_shot(row, column)