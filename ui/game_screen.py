from pathlib import Path
from PySide6.QtCore import QEvent, QTimer, Qt
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from game.board import ShotResult
from game.game_manager import GameManager, GameState
from game.ship import Orientation, Ship

from ui.board_widget import BoardWidget
from ui.bottom_status_panel import BottomStatusPanel
from ui.control_panel import ControlPanel
from ui.fireworks_widget import FireworksWidget
from ui.fleet_panel import FleetPanel
from ui.game_info_panel import GameInfoPanel


class GameScreen(QWidget):
    REQUIRED_FLEET = {
        "Battleship": 1,
        "Cruiser": 2,
        "Destroyer": 3,
        "Patrol Boat": 4,
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.game_manager = GameManager()

        self.selected_ship_name: str | None = None
        self.selected_orientation = "horizontal"
        self.sound_enabled = True

        self.setObjectName("gameScreen")

        self.fireworks = FireworksWidget(self)

        self.click_sound = QSoundEffect(self)

        sound_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "audio"
            / "sounds"
            / "click.wav"
            ""
        )

        self.click_sound.setSource(
            sound_path.as_uri()
        )

        self.click_sound.setVolume(0.5)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(
            self._create_header()
        )

        layout.addWidget(
            self._create_game_area(),
            1,
        )

        layout.addWidget(
            self._create_bottom_panel()
        )

        self._update_game_info()
        self._update_placement_status()
        self._connect_signals()

    def _get_help_text(self) -> str:
        state = self.game_manager.state

        if state == GameState.PLACING_SHIPS:
            if not self._all_ships_ready():
                missing_ships = []

                for (
                    ship_name,
                    required_count,
                ) in self.REQUIRED_FLEET.items():
                    current_count = sum(
                        1
                        for ship
                        in self.game_manager.player.board.ships
                        if ship.name == ship_name
                    )

                    missing_count = (
                        required_count - current_count
                    )

                    if missing_count > 0:
                        missing_ships.append(
                            f"{ship_name} ×{missing_count}"
                        )

                if not missing_ships:
                    return (
                        "Choose a ship, select its orientation, "
                        "and place it on the board."
                    )

                return (
                    "You still need to place:\n"
                    + "\n".join(missing_ships)
                )

            return (
                "All ships are ready.\n"
                "Click READY to start the battle."
            )

        if state == GameState.PLAYER_TURN:
            return (
                "It's your turn.\n"
                "Click a cell on the enemy board to fire."
            )

        return "Computer is thinking. Please wait."
    def _update_help_tooltip(self) -> None:
        self.help_button.setToolTip(
            self._get_help_text()
        )
    
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        if hasattr(self, "fireworks"):
            self.fireworks.setGeometry(
                self.rect()
            )
    def _show_main_menu(self) -> None:
        self._new_game()
        self.hide()

        main_window = self.window()
        main_window.main_menu.show()

    def _create_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("header")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        main_menu_button = QPushButton(
            "☰  MAIN MENU"
        )
        
        new_game_button = QPushButton(
            "✚  NEW GAME"
        )
        new_game_button.clicked.connect(
            self._new_game
        )

        new_game_button.clicked.connect(
            self._play_click_sound
        )
        main_menu_button.clicked.connect(
            self._show_main_menu
        )

        main_menu_button.clicked.connect(
            self._play_click_sound
        )

        players_button = QPushButton(
            "♟  2 PLAYERS  ▼"
        )

        title = QLabel("BATTLESHIPS")
        title.setObjectName("gameTitle")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        sound_button = QPushButton("🔊")
        sound_button.clicked.connect(
            self._play_click_sound
        )
        sound_button.setCheckable(True)
        sound_button.setChecked(True)
        sound_button.toggled.connect(
            self._toggle_sound
        )
        sound_button.clicked.connect(
            self._play_click_sound
        )

        players_button.clicked.connect(
            self._play_click_sound
        )

        music_button = QPushButton("♫")
        music_button.clicked.connect(
            self._play_click_sound
        )
        music_button.setCheckable(True)
        music_button.setChecked(True)
        music_button.toggled.connect(
            self._toggle_music
        )

        self.help_button = QPushButton("?")
        self.help_button.setToolTip(self._get_help_text())

        self.help_button.clicked.connect(
            self._play_click_sound
        )
        self.help_button.clicked.connect(
            self._show_help
        )

        settings_button = QPushButton("⚙")
        settings_button.clicked.connect(
            self._play_click_sound
        )
        settings_button.clicked.connect(
            self._show_settings
        )

        new_game_button.setObjectName(
            "leftHeaderButton"
        )

        players_button.setObjectName(
            "leftHeaderButton"
        )

        for button in (
            sound_button,
            music_button,
            self.help_button,
            settings_button,
        ):
            button.setObjectName(
                "rightHeaderButton"
            )
        layout.addWidget(main_menu_button)
        layout.addWidget(new_game_button)
        layout.addWidget(players_button)

        layout.addSpacing(40)
        layout.addStretch()

        layout.addWidget(title)

        layout.addStretch()
        layout.addSpacing(40)

        layout.addWidget(sound_button)
        layout.addWidget(music_button)
        layout.addWidget(self.help_button)
        layout.addWidget(settings_button)

        return header

    def _create_game_area(self) -> QWidget:
        game_area = QWidget()

        layout = QHBoxLayout(game_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(
            self._create_left_panel()
        )

        layout.addWidget(
            self._create_player_board_area(),
            1,
        )

        layout.addWidget(
            self._create_enemy_board_area(),
            1,
        )

        layout.addWidget(
            self._create_right_panel()
        )

        return game_area

    def _create_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(220)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        fleet_frame = QFrame()
        fleet_frame.setObjectName("panelFrame")

        fleet_layout = QVBoxLayout(fleet_frame)
        fleet_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        fleet_title = QLabel("YOUR FLEET")
        fleet_title.setObjectName("panelTitle")
        fleet_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.fleet_panel = FleetPanel()

        fleet_layout.addWidget(fleet_title)
        fleet_layout.addWidget(self.fleet_panel)

        controls_frame = QFrame()
        controls_frame.setObjectName("panelFrame")

        controls_layout = QVBoxLayout(
            controls_frame
        )
        controls_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )
        controls_layout.setSpacing(10)

        controls_title = QLabel("CONTROLS")
        controls_title.setObjectName("panelTitle")
        controls_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.control_panel = ControlPanel()

        self.control_panel.layout().setDirection(
            QBoxLayout.Direction.TopToBottom
        )

        controls_layout.addWidget(
            controls_title
        )

        controls_layout.addWidget(
            self.control_panel
        )

        layout.addWidget(
            fleet_frame,
            1,
        )

        layout.addWidget(
            controls_frame
        )

        return panel

    def _create_player_board_area(self) -> QWidget:
        container = QFrame()
        container.setObjectName("boardContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )
        layout.setSpacing(8)

        title = QLabel(
            "YOUR BOARD - PLACE YOUR SHIPS"
        )
        title.setObjectName("boardTitle")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.player_board = BoardWidget()

        layout.addWidget(title)

        layout.addWidget(
            self.player_board,
            1,
        )

        return container

    def _create_enemy_board_area(self) -> QWidget:
        container = QFrame()
        container.setObjectName("boardContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )
        layout.setSpacing(8)

        title = QLabel(
            "ENEMY BOARD - TAKE YOUR SHOT"
        )
        title.setObjectName("boardTitle")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.enemy_board = BoardWidget()

        layout.addWidget(title)

        layout.addWidget(
            self.enemy_board,
            1,
        )

        return container

    def _create_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(220)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(10)

        game_info_frame = QFrame()
        game_info_frame.setObjectName(
            "panelFrame"
        )

        game_info_layout = QVBoxLayout(
            game_info_frame
        )
        game_info_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        self.game_info_panel = GameInfoPanel()

        game_info_layout.addWidget(
            self.game_info_panel
        )

        layout.addWidget(
            game_info_frame,
            1,
        )

        return panel

    def _create_bottom_panel(self) -> QWidget:
        container = QFrame()
        container.setObjectName("bottomPanel")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(
            15,
            8,
            15,
            8,
        )

        self.bottom_status_panel = (
            BottomStatusPanel()
        )

        layout.addWidget(
            self.bottom_status_panel
        )

        return container

    def _connect_signals(self) -> None:
        self.fleet_panel.ship_selected.connect(
            self._select_ship
        )

        self.fleet_panel.orientation_selected.connect(
            self._select_orientation
        )

        self.player_board.cell_clicked.connect(
            self._select_board_position
        )

        self.enemy_board.cell_clicked.connect(
            self._player_shoot
        )

        self.control_panel.ready_clicked.connect(
            self._ready
        )

    def _select_ship(
        self,
        ship_name: str,
    ) -> None:
        self.selected_ship_name = ship_name

    def _select_orientation(
        self,
        orientation: str,
    ) -> None:
        self.selected_orientation = orientation

    def _ready(self) -> None:
        for (
            ship_name,
            required_count,
        ) in self.REQUIRED_FLEET.items():
            actual_count = sum(
                1
                for ship
                in self.game_manager.player.board.ships
                if ship.name == ship_name
            )

            if actual_count != required_count:
                return

        self.game_manager.computer_ai.place_fleet(
            self.game_manager.computer.board
        )

        self._update_game_info()

        self.control_panel.set_placement_controls_enabled(
            False
        )

        self.control_panel.set_ready_enabled(
            False
        )

        self.game_manager.start_game()

        self.bottom_status_panel.set_status(
            "YOUR TURN — TAKE YOUR SHOT"
        )
        self._update_help_tooltip()

    def _select_board_position(
        self,
        row: int,
        column: int,
    ) -> None:
        if (
            self.game_manager.state
            != GameState.PLACING_SHIPS
        ):
            return

        if self.selected_ship_name is None:
            return

        board = self.game_manager.player.board

        existing_ship = board.get_ship_at(
            row,
            column,
        )

        if existing_ship is not None:
            if (
                existing_ship.name
                == self.selected_ship_name
            ):
                positions = (
                    existing_ship.positions.copy()
                )

                if board.remove_ship(
                    existing_ship
                ):
                    for (
                        ship_row,
                        ship_column,
                    ) in positions:
                        self.player_board.set_cell_empty(
                            ship_row,
                            ship_column,
                        )

                    remaining_count = sum(
                        1
                        for ship in board.ships
                        if ship.name
                        == existing_ship.name
                    )

                    total_count = next(
                        count
                        for (
                            name,
                            size,
                            count,
                            image_name,
                        ) in self.fleet_panel.SHIPS
                        if name
                        == existing_ship.name
                    )

                    self.fleet_panel.set_ship_remaining(
                        existing_ship.name,
                        total_count
                        - remaining_count,
                    )

                    self._update_game_info()
                    self._update_placement_status()

            return

        ship_data = next(
            (
                (name, size)
                for (
                    name,
                    size,
                    count,
                    image_name,
                ) in self.fleet_panel.SHIPS
                if name
                == self.selected_ship_name
            ),
            None,
        )

        if ship_data is None:
            return

        ship_name, ship_size = ship_data

        orientation = (
            Orientation.HORIZONTAL
            if self.selected_orientation
            == "horizontal"
            else Orientation.VERTICAL
        )

        ship = Ship(
            name=ship_name,
            size=ship_size,
            orientation=orientation,
        )

        if not board.place_ship(
            ship,
            row,
            column,
        ):
            return

        for (
            ship_row,
            ship_column,
        ) in ship.positions:
            self.player_board.set_cell_ship(
                ship_row,
                ship_column,
            )

        image_names = {
            4: "ship_1.png",
            3: "ship_2.png",
            2: "ship_3.png",
            1: "ship_4.png",
        }

        image_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "ships"
            / image_names[ship_size]
        )

        self.player_board.set_ship_image(
            ship.positions,
            str(image_path),
            vertical=(
                orientation
                == Orientation.VERTICAL
            ),
        )

        remaining_count = sum(
            1
            for existing_ship in board.ships
            if existing_ship.name
            == ship_name
        )

        total_count = next(
            count
            for (
                name,
                size,
                count,
                image_name,
            ) in self.fleet_panel.SHIPS
            if name == ship_name
        )

        self.fleet_panel.set_ship_remaining(
            ship_name,
            total_count - remaining_count,
        )

        self._update_game_info()
        self._update_placement_status()
        self._update_help_tooltip()

    def _player_shoot(
        self,
        row: int,
        column: int,
    ) -> None:
        if (
            self.game_manager.state
            != GameState.PLAYER_TURN
        ):
            return

        result = self.game_manager.player_shoot(
            row,
            column,
        )

        if result == ShotResult.ALREADY_SHOT:
            return

        self._update_game_info()

        if result == ShotResult.SUNK:
            sunk_ship = (
                self.game_manager.computer.board.get_ship_at(
                    row,
                    column,
                )
            )

            if sunk_ship is not None:
                self.enemy_board.set_ship_sunk(
                    sunk_ship.positions
                )

        elif result == ShotResult.HIT:
            self.enemy_board.set_cell_hit(
                row,
                column,
            )

        else:
            self.enemy_board.set_cell_miss(
                row,
                column,
            )

        if self.game_manager.is_game_over:
            self._show_game_over()
            return

        self.bottom_status_panel.set_status(
            "COMPUTER THINKING..."
        )
        self._update_help_tooltip()
        QTimer.singleShot(
            1000,
            self._computer_shoot,
        )

    def _computer_shoot(self) -> None:
        row, column = (
            self.game_manager.computer_ai.choose_shot()
        )

        result = self.game_manager.computer_shoot(
            row,
            column,
        )

        self._update_game_info()

        if result == ShotResult.SUNK:
            sunk_ship = (
                self.game_manager.player.board.get_ship_at(
                    row,
                    column,
                )
            )

            if sunk_ship is not None:
                self.player_board.set_ship_sunk(
                    sunk_ship.positions
                )

        elif result == ShotResult.HIT:
            self.player_board.set_cell_hit(
                row,
                column,
            )

        else:
            self.player_board.set_cell_miss(
                row,
                column,
            )

        self.game_manager.computer_ai.process_shot_result(
            self.game_manager.player.board,
            row,
            column,
            result,
        )

        if self.game_manager.is_game_over:
            self._show_game_over()
            return

        self.bottom_status_panel.set_status(
            "YOUR TURN — TAKE YOUR SHOT"
        )
        self._update_help_tooltip()

    def _update_game_info(self) -> None:
        self.game_info_panel.set_player_ships(
            self.game_manager.player.remaining_ships
        )

        self.game_info_panel.set_enemy_ships(
            self.game_manager.computer.remaining_ships
        )

    def _all_ships_ready(self) -> bool:
        board = self.game_manager.player.board

        return all(
            sum(
                1
                for ship in board.ships
                if ship.name == ship_name
            )
            == required_count
            for (
                ship_name,
                required_count,
            ) in self.REQUIRED_FLEET.items()
        )

    def _update_placement_status(self) -> None:
        if self._all_ships_ready():
            self.bottom_status_panel.set_status(
                "ALL SHIPS READY — CLICK READY"
            )
        else:
            self.bottom_status_panel.set_status(
                "PLACE YOUR SHIPS"
            )

    def _new_game(self) -> None:
        self.fireworks.stop()
        self.game_manager.reset()

        self.selected_ship_name = None
        self.selected_orientation = "horizontal"

        self.player_board.reset()
        self.enemy_board.reset()

        self.fleet_panel.reset()

        self.control_panel.set_placement_controls_enabled(
            True
        )

        self.control_panel.set_ready_enabled(
            True
        )

        self._update_game_info()
        self._update_placement_status()
        self._update_help_tooltip()

    def _show_game_over(self) -> None:
        winner = self.game_manager.winner

        if winner is None:
            return

        if winner == self.game_manager.player:
            message = "YOU WIN!"
            self.fireworks.start()
        else:
            message = "COMPUTER WINS!"

        self.control_panel.set_placement_controls_enabled(
            False
        )

        self.control_panel.set_ready_enabled(
            False
        )

        self.bottom_status_panel.set_status(
            message
        )

    def _show_help(self) -> None:
        main_window = self.window()

        self.hide()
        main_window.main_menu.hide()
        main_window.settings_screen.hide()
        main_window.help_screen.show()

    def _show_settings(self) -> None:
        QMessageBox.information(
            self,
            "Settings",
            "Settings will be available here."
        )

    def _toggle_sound(
        self,
        enabled: bool,
    ) -> None:
        sound_button = self.sender()

        if enabled:
            sound_button.setText("🔊")
        else:
            sound_button.setText("🔇")
    def _play_click_sound(self) -> None:
        if not self.window().sound_enabled:
            return
        print(
            "Sound status:",
            self.click_sound.status(),
            "Loaded:",
            self.click_sound.isLoaded(),
        )

        self.click_sound.play()

    def _toggle_music(
        self,
        enabled: bool,
    ) -> None:
        music_button = self.sender()

        if enabled:
            music_button.setText("♫")
        else:
            music_button.setText("🔇")