from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsScreen(QWidget):
    back_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.sound_enabled = True

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

        title = QLabel("SETTINGS")
        title.setObjectName("gameTitle")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        sound_button = QPushButton(
            "SOUND: ON"
        )

        music_button = QPushButton(
            "MUSIC: ON"
        )
        self.music_enabled = True

        back_button = QPushButton(
            "BACK TO MAIN MENU"
        )

        for button in (
            sound_button,
            music_button,
            back_button,
        ):
            button.setMinimumWidth(280)
            button.setMinimumHeight(45)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(sound_button)
        layout.addWidget(music_button)
        layout.addSpacing(20)
        layout.addWidget(back_button)

        sound_button.clicked.connect(
            self._toggle_sound
        )
        sound_button.clicked.connect(
            self._play_click_sound
        )
        music_button.clicked.connect(
            self._toggle_music
        )

        back_button.clicked.connect(
            self.back_clicked
        )
    def _play_click_sound(self) -> None:
        main_window = self.window()

        if hasattr(main_window, "game_screen"):
            main_window.game_screen._play_click_sound()
            
    def _toggle_sound(self) -> None:
        self.sound_enabled = not self.sound_enabled
        main_window = self.window()
        main_window.sound_enabled = self.sound_enabled
        if not self.sound_enabled:
            main_window.game_screen.click_sound.stop()

        main_window = self.window()

        if hasattr(main_window, "game_screen"):
            main_window.game_screen.sound_enabled = self.sound_enabled

        if self.sound_enabled:
            self.sender().setText(
                "SOUND: ON"
            )
        else:
            self.sender().setText(
                "SOUND: OFF"
            )

    def _toggle_music(self) -> None:
        self.music_enabled = not self.music_enabled

        if self.music_enabled:
            self.sender().setText(
                "MUSIC: ON"
            )
        else:
            self.sender().setText(
                "MUSIC: OFF"
            )