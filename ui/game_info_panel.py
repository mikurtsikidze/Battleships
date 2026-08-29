from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class GameInfoPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("GAME INFO")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        self.turn_label = QLabel("PLACE YOUR SHIPS")
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setStyleSheet("font-size: 16px;")

        self.player_ships_label = QLabel("YOUR SHIPS: 5")
        self.enemy_ships_label = QLabel("ENEMY SHIPS: 5")

        layout.addWidget(title)
        layout.addWidget(self.turn_label)
        layout.addSpacing(15)
        layout.addWidget(self.player_ships_label)
        layout.addWidget(self.enemy_ships_label)
        layout.addStretch()

    def set_status(self, text: str) -> None:
        self.turn_label.setText(text)

    def set_player_ships(self, count: int) -> None:
        self.player_ships_label.setText(
            f"YOUR SHIPS: {count}"
        )

    def set_enemy_ships(self, count: int) -> None:
        self.enemy_ships_label.setText(
            f"ENEMY SHIPS: {count}"
        )

    def reset(self) -> None:
        self.set_status("PLACE YOUR SHIPS")
        self.set_player_ships(5)
        self.set_enemy_ships(5)