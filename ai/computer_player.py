from __future__ import annotations

import random

from game.board import Board, ShotResult
from game.ship import Orientation, Ship


class ComputerPlayer:
    def __init__(self) -> None:
        self.available_shots = [
            (row, column)
            for row in range(Board.SIZE)
            for column in range(Board.SIZE)
        ]

        self.target_queue: list[tuple[int, int]] = []
        self.hit_positions: list[tuple[int, int]] = []
        self.target_direction: tuple[int, int] | None = None

    def choose_shot(self) -> tuple[int, int]:
        if self.target_queue:
            shot = self.target_queue.pop(0)

            if shot in self.available_shots:
                self.available_shots.remove(shot)

            return shot

        shot = random.choice(self.available_shots)
        self.available_shots.remove(shot)

        return shot

    def process_shot_result(
        self,
        board: Board,
        row: int,
        column: int,
        result: ShotResult,
    ) -> None:
        if result == ShotResult.HIT:
            self.hit_positions.append((row, column))

            if len(self.hit_positions) >= 2:
                first_row, first_column = self.hit_positions[-2]
                second_row, second_column = self.hit_positions[-1]

                if first_row == second_row:
                    self.target_direction = (0, 1)
                elif first_column == second_column:
                    self.target_direction = (1, 0)

            self._add_target_positions(
                board,
                row,
                column,
            )

        elif result == ShotResult.MISS:
            if self.target_direction is not None:
                self.target_queue = [
                    target
                    for target in self.target_queue
                    if target != (row, column)
                ]

        elif result == ShotResult.SUNK:
            self.target_queue.clear()
            self.hit_positions.clear()
            self.target_direction = None

    def place_fleet(self, board: Board) -> None:
        fleet = (
            ("Battleship", 4, 1),
            ("Cruiser", 3, 2),
            ("Destroyer", 2, 3),
            ("Patrol Boat", 1, 4),
        )

        for ship_name, ship_size, count in fleet:
            for _ in range(count):
                while True:
                    orientation = random.choice(
                        [
                            Orientation.HORIZONTAL,
                            Orientation.VERTICAL,
                        ]
                    )

                    ship = Ship(
                        name=ship_name,
                        size=ship_size,
                        orientation=orientation,
                    )

                    row = random.randrange(Board.SIZE)
                    column = random.randrange(Board.SIZE)

                    if board.place_ship(
                        ship,
                        row,
                        column,
                    ):
                        break

    def reset(self) -> None:
        self.available_shots = [
            (row, column)
            for row in range(Board.SIZE)
            for column in range(Board.SIZE)
        ]

        self.target_queue.clear()
        self.hit_positions.clear()
        self.target_direction = None

    def _add_target_positions(
        self,
        board: Board,
        row: int,
        column: int,
    ) -> None:
        if self.target_direction is not None:
            direction_row, direction_column = self.target_direction

            targets = [
                (
                    row + direction_row,
                    column + direction_column,
                ),
                (
                    row - direction_row,
                    column - direction_column,
                ),
            ]
        else:
            targets = [
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
            ]

        for target in targets:
            if (
                self._is_inside_board(target)
                and target in self.available_shots
                and target not in self.target_queue
            ):
                self.target_queue.append(target)


    @staticmethod
    def _is_inside_board(
        position: tuple[int, int],
    ) -> bool:
        row, column = position

        return 0 <= row < Board.SIZE and 0 <= column < Board.SIZE