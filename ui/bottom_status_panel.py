from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget


class BottomStatusPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)

        self.player_label = QLabel("PLAYER 1")
        self.status_label = QLabel("PLACE YOUR SHIPS")
        self.enemy_label = QLabel("COMPUTER")

        self.player_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enemy_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.player_label.setStyleSheet("font-weight: bold;")
        self.status_label.setStyleSheet("font-weight: bold;")
        self.enemy_label.setStyleSheet("font-weight: bold;")

        layout.addWidget(self.player_label, 1)
        layout.addWidget(self.status_label, 2)
        layout.addWidget(self.enemy_label, 1)

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)

    def set_player_name(self, name: str) -> None:
        self.player_label.setText(name)

    def set_enemy_name(self, name: str) -> None:
        self.enemy_label.setText(name)