from __future__ import annotations

import random

from game.board import Board, ShotResult


class ComputerPlayer:
    def __init__(self) -> None:
        self.available_shots = [
            (row, column)
            for row in range(Board.SIZE)
            for column in range(Board.SIZE)
        ]

        self.target_queue: list[tuple[int, int]] = []

    def choose_shot(self) -> tuple[int, int]:
        if self.target_queue:
            return self.target_queue.pop(0)

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
            self._add_target_positions(board, row, column)

        elif result == ShotResult.SUNK:
            self.target_queue.clear()

    def reset(self) -> None:
        self.available_shots = [
            (row, column)
            for row in range(Board.SIZE)
            for column in range(Board.SIZE)
        ]

        self.target_queue.clear()

    def _add_target_positions(
        self,
        board: Board,
        row: int,
        column: int,
    ) -> None:
        possible_targets = [
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ]

        for target in possible_targets:
            if (
                self._is_inside_board(target)
                and target in self.available_shots
                and target not in self.target_queue
            ):
                self.target_queue.append(target)

        random.shuffle(self.target_queue)

    @staticmethod
    def _is_inside_board(
        position: tuple[int, int],
    ) -> bool:
        row, column = position

        return 0 <= row < Board.SIZE and 0 <= column < Board.SIZE