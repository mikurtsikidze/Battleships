from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class GameInfoPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("GAME INFO")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        self.player_ships_label = QLabel(
            "YOUR SHIPS: 0"
        )

        self.enemy_ships_label = QLabel(
            "ENEMY SHIPS: 0"
        )

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(
            self.player_ships_label
        )
        layout.addWidget(
            self.enemy_ships_label
        )
        layout.addStretch()

    def set_player_ships(self, count: int) -> None:
        self.player_ships_label.setText(
            f"YOUR SHIPS: {count}"
        )

    def set_enemy_ships(self, count: int) -> None:
        self.enemy_ships_label.setText(
            f"ENEMY SHIPS: {count}"
        )