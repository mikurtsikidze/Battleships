from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainMenu(QWidget):
    play_vs_computer_clicked = Signal()
    settings_clicked = Signal()
    help_clicked = Signal()

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

        title = QLabel("BATTLESHIPS")
        title.setObjectName("gameTitle")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel("MAIN MENU")
        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        play_button = QPushButton(
            "PLAY VS COMPUTER"
        )

        online_button = QPushButton(
            "ONLINE MULTIPLAYER"
        )
        online_button.clicked.connect(
            self._play_click_sound
        )

        settings_button = QPushButton(
            "SETTINGS"
        )

        settings_button.clicked.connect(
            self.settings_clicked
        )
        settings_button.clicked.connect(
            self._play_click_sound
        )

        help_button = QPushButton(
            "HELP"
        )
        help_button.clicked.connect(
            self.help_clicked
        )
        help_button.clicked.connect(
            self._play_click_sound
        )

        exit_button = QPushButton(
            "EXIT"
        )
        exit_button.clicked.connect(
            lambda: self.window().close()
        )
        exit_button.clicked.connect(
            self._play_click_sound
        )

        play_button.clicked.connect(
            self.play_vs_computer_clicked
        )
        play_button.clicked.connect(
            self._play_click_sound
        )

        for button in (
            play_button,
            online_button,
            settings_button,
            help_button,
            exit_button,
        ):
            button.setMinimumWidth(280)
            button.setMinimumHeight(45)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(play_button)
        layout.addWidget(online_button)
        layout.addWidget(settings_button)
        layout.addWidget(help_button)
        layout.addWidget(exit_button)

    def _play_click_sound(self) -> None:
        main_window = self.window()

        if hasattr(main_window, "game_screen"):
            main_window.game_screen._play_click_sound()