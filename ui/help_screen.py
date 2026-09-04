from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class HelpScreen(QWidget):
    back_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            40,
            40,
            40,
            40,
        )
        layout.setSpacing(15)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel("HELP")
        title.setObjectName("gameTitle")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        instructions = QLabel(
            "BATTLESHIPS\n\n"
            "1. Choose a ship, select its orientation, and place it on the board.\n"
            "2. Place all your ships and click READY when you are done.\n"
            "3. The battle begins after you click READY.\n"
            "4. Click a cell on the enemy board to fire.\n"
            "5. HIT means you hit an enemy ship.\n"
            "6. MISS means your shot missed.\n"
            "7. SUNK means you destroyed an enemy ship.\n"
            "8. Destroy all enemy ships to win the game."
        )

        instructions.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        instructions.setWordWrap(True)
        instructions.setMinimumWidth(700)
        instructions.setMinimumHeight(350)

        instructions.setStyleSheet(
            """
            QLabel {
                color: #ff4d4d;
                font-size: 18px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 190);
                padding: 20px;
                border-radius: 8px;
            }
            """
        )

        back_button = QPushButton(
            "BACK TO MAIN MENU"
        )
        back_button.clicked.connect(
           self.back_clicked
        )

        back_button.clicked.connect(
            self._play_click_sound
        )

        back_button.setMinimumWidth(280)
        back_button.setMinimumHeight(45)

        layout.addWidget(title)

        layout.addWidget(instructions)
        layout.addSpacing(30)

        back_button.setMinimumWidth(280)
        back_button.setMinimumHeight(45)

        layout.addWidget(back_button)

        back_button.clicked.connect(
            self.back_clicked
        )
    def _play_click_sound(self) -> None:
        main_window = self.window()

        if hasattr(main_window, "game_screen"):
            main_window.game_screen._play_click_sound()