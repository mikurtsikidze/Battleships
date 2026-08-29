from __future__ import annotations

from enum import Enum

from game.board import ShotResult
from game.player import Player


class GameState(Enum):
    PLACING_SHIPS = "placing_ships"
    PLAYER_TURN = "player_turn"
    COMPUTER_TURN = "computer_turn"
    GAME_OVER = "game_over"


class GameManager:
    def __init__(self) -> None:
        self.player = Player("Player")
        self.computer = Player("Computer")

        self.state = GameState.PLACING_SHIPS
        self.current_player: Player | None = None
        self.winner: Player | None = None

    def start_game(self) -> None:
        if not self.player.board.ships:
            raise ValueError("Player has not placed any ships.")

        if not self.computer.board.ships:
            raise ValueError("Computer has not placed any ships.")

        self.state = GameState.PLAYER_TURN
        self.current_player = self.player
        self.winner = None

    def player_shoot(
        self,
        row: int,
        column: int,
    ) -> ShotResult:
        if self.state != GameState.PLAYER_TURN:
            raise RuntimeError("It is not the player's turn.")

        result = self.player.shoot(
            self.computer,
            row,
            column,
        )

        if result == ShotResult.ALREADY_SHOT:
            return result

        self._check_winner()

        if self.state != GameState.GAME_OVER:
            self.state = GameState.COMPUTER_TURN
            self.current_player = self.computer

        return result

    def computer_shoot(
        self,
        row: int,
        column: int,
    ) -> ShotResult:
        if self.state != GameState.COMPUTER_TURN:
            raise RuntimeError("It is not the computer's turn.")

        result = self.computer.shoot(
            self.player,
            row,
            column,
        )

        if result == ShotResult.ALREADY_SHOT:
            return result

        self._check_winner()

        if self.state != GameState.GAME_OVER:
            self.state = GameState.PLAYER_TURN
            self.current_player = self.player

        return result

    def _check_winner(self) -> None:
        if self.player.has_lost:
            self.winner = self.computer
            self.state = GameState.GAME_OVER
            self.current_player = None

        elif self.computer.has_lost:
            self.winner = self.player
            self.state = GameState.GAME_OVER
            self.current_player = None

    @property
    def is_game_over(self) -> bool:
        return self.state == GameState.GAME_OVER

    def reset(self) -> None:
        self.player = Player("Player")
        self.computer = Player("Computer")

        self.state = GameState.PLACING_SHIPS
        self.current_player = None
        self.winner = None