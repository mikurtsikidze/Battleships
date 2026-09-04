from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from ui.game_screen import GameScreen
from ui.main_menu import MainMenu
from ui.settings_screen import SettingsScreen
from ui.help_screen import HelpScreen

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Battleships")

        self.resize(1500, 950)
        self.setMinimumSize(1200, 750)

        self._apply_style()

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )
        root_layout.setSpacing(10)

        self.main_menu = MainMenu()
        self.game_screen = GameScreen()
        self.settings_screen = SettingsScreen()
        self.sound_enabled = True
        self.help_screen = HelpScreen()

        root_layout.addWidget(
            self.main_menu,
            1,
        )
        root_layout.addWidget(
            self.help_screen,
            1,
        )

        root_layout.addWidget(
            self.settings_screen,
            1,
        )

        root_layout.addWidget(
            self.game_screen,
            1,
        )

        self.game_screen.hide()
        self.settings_screen.hide()
        self.help_screen.hide()

        self.main_menu.play_vs_computer_clicked.connect(
            self._start_game
        )

        self.main_menu.settings_clicked.connect(
            self._show_settings
        )
        self.main_menu.help_clicked.connect(
            self._show_help
        )
        self.help_screen.back_clicked.connect(
            self._show_main_menu
        )
        self.settings_screen.back_clicked.connect(
            self._show_main_menu
        )
    def _start_game(self) -> None:
        self.main_menu.hide()
        self.game_screen.show()

    def _show_settings(self) -> None:
        self.main_menu.hide()
        self.game_screen.hide()
        self.settings_screen.show()

    def _show_help(self) -> None:
        self.main_menu.hide()
        self.game_screen.hide()
        self.settings_screen.hide()
        self.help_screen.show()
\
    def _show_main_menu(self) -> None:
        self.settings_screen.hide()
        self.game_screen.hide()
        self.help_screen.hide()
        self.main_menu.show()

    def _apply_style(self) -> None:
        background_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "backgrounds"
            / "background.png"
        ).as_posix()

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: #06131e;
            }}

            #centralWidget {{
                border-image: url("{background_path}") 0 0 0 0 stretch stretch;
            }}

            QWidget {{
                background-color: transparent;
                color: #d9e5ec;
                font-family: Arial;
            }}

            #gameScreen {{
                background-color: transparent;
            }}

            #gameTitle {{
                background-color: transparent;
                color: #e6edf2;
                font-size: 38px;
                font-weight: bold;
                letter-spacing: 2px;
            }}

            QPushButton {{
                background-color: #123249;
                border: 1px solid #416780;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: #1b4a68;
            }}

            #leftHeaderButton {{
                background-color: #0e2434;
                border: 1px solid #34566d;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: bold;
                min-height: 36px;
            }}

            #leftHeaderButton:hover {{
                background-color: #16384d;
            }}

            #rightHeaderButton {{
                background-color: #0e2434;
                border: 1px solid #34566d;
                border-radius: 7px;
                padding: 10px;
                min-width: 48px;
                min-height: 42px;
                font-size: 16px;
            }}

            #rightHeaderButton:hover {{
                background-color: #16384d;
            }}

            #panelFrame {{
                background-color: rgba(
                    8,
                    25,
                    37,
                    190
                );
                border: 1px solid #29485d;
                border-radius: 8px;
            }}

            #panelTitle {{
                background-color: rgba(
                    16,
                    41,
                    59,
                    230
                );
                border-bottom: 1px solid #29485d;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }}

            #boardContainer {{
                background-color: rgba(
                    6,
                    23,
                    37,
                    175
                );
                border: 1px solid #24516d;
                border-radius: 8px;
            }}

            #boardTitle {{
                background-color: rgba(
                    16,
                    63,
                    96,
                    230
                );
                border: 1px solid #2776a5;
                border-radius: 5px;
                padding: 10px;
                font-size: 17px;
                font-weight: bold;
            }}

            #bottomPanel {{
                background-color: rgba(
                    7,
                    24,
                    36,
                    180
                );
                border: 1px solid #29485d;
                border-radius: 8px;
                min-height: 90px;
            }}

            #shipRow {{
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #1d3444;
                border-radius: 0;
                min-height: 72px;
            }}

            #shipRow:hover {{
                background-color: rgba(
                    16,
                    42,
                    59,
                    180
                );
            }}

            #shipRow[selected="true"] {{
                background-color: #1b4a68;
                border: 2px solid #5aa7d9;
            }}

            #shipName {{
                color: #e6eef3;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }}

            #shipSize {{
                color: #8fa9b8;
                font-size: 11px;
                background-color: transparent;
            }}

            #shipCount {{
                color: #5ee06b;
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
            }}

            #shipImage {{
                background-color: transparent;
                border: none;
            }}

            #shipCell {{
                background-color: #7a8b95;
                border: 1px solid #b5c2c8;
                border-radius: 3px;
            }}
            """
        )