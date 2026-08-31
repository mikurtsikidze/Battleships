from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from game.game_manager import GameManager
from game.ship import Orientation, Ship
from pathlib import Path
from ui.board_widget import BoardWidget
from ui.bottom_status_panel import BottomStatusPanel
from ui.control_panel import ControlPanel
from ui.fleet_panel import FleetPanel
from ui.game_info_panel import GameInfoPanel
from game.board import ShotResult
from game.game_manager import GameManager, GameState
from PySide6.QtCore import QTimer, Qt, Signal

 

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.game_manager = GameManager()
        self.selected_ship_name: str | None = None
        self.selected_ship_position: tuple[int, int] | None = None
        self.selected_orientation = "horizontal"
        self.setWindowTitle("Battleships")
        self.resize(1500, 950)
        self.setMinimumSize(1200, 750)

        self._apply_style()

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        root_layout.addWidget(self._create_header())
        root_layout.addWidget(self._create_game_area(), 1)
        root_layout.addWidget(self._create_bottom_panel())
        self._connect_signals()

    def _create_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("header")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        new_game_button = QPushButton("✚  NEW GAME")
        new_game_button.clicked.connect(
            self._new_game
        )
        players_button = QPushButton("♟  2 PLAYERS  ▼")

        title = QLabel("BATTLESHIPS")
        title.setObjectName("gameTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sound_button = QPushButton("🔊")
        music_button = QPushButton("♫")
        help_button = QPushButton("?")
        settings_button = QPushButton("⚙")

        new_game_button.setObjectName("leftHeaderButton")
        players_button.setObjectName("leftHeaderButton")

        for button in (
            sound_button,
            music_button,
            help_button,
            settings_button,
        ):
            button.setObjectName("rightHeaderButton")

        layout.addWidget(new_game_button)
        layout.addWidget(players_button)

        layout.addSpacing(40)
        layout.addStretch()

        layout.addWidget(title)

        layout.addStretch()
        layout.addSpacing(40)

        layout.addWidget(sound_button)
        layout.addWidget(music_button)
        layout.addWidget(help_button)
        layout.addWidget(settings_button)

        return header

    def _create_game_area(self) -> QWidget:
        game_area = QWidget()

        layout = QHBoxLayout(game_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(self._create_left_panel())
        layout.addWidget(self._create_player_board_area(), 1)
        layout.addWidget(self._create_enemy_board_area(), 1)
        layout.addWidget(self._create_right_panel())

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
        fleet_layout.setContentsMargins(10, 10, 10, 10)

        fleet_title = QLabel("YOUR FLEET")
        fleet_title.setObjectName("panelTitle")
        fleet_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fleet_panel = FleetPanel()

        fleet_layout.addWidget(fleet_title)
        fleet_layout.addWidget(self.fleet_panel)

        controls_frame = QFrame()
        controls_frame.setObjectName("panelFrame")

        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        controls_layout.setSpacing(10)

        controls_title = QLabel("CONTROLS")
        controls_title.setObjectName("panelTitle")
        controls_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.control_panel = ControlPanel()
        self.control_panel.layout().setDirection(
            QBoxLayout.Direction.TopToBottom
        )

        controls_layout.addWidget(controls_title)
        controls_layout.addWidget(self.control_panel)

        layout.addWidget(fleet_frame, 1)
        layout.addWidget(controls_frame)

        return panel

    def _create_player_board_area(self) -> QWidget:
        container = QFrame()
        container.setObjectName("boardContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        title = QLabel("YOUR BOARD - PLACE YOUR SHIPS")
        title.setObjectName("boardTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.player_board = BoardWidget()

        hint = QLabel(
            "Place all your ships on the grid.\n"
            "Click READY when you are done."
        )
        hint.setObjectName("hintLabel")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setFixedHeight(55)

        layout.addWidget(title)

        layout.addWidget(
            self.player_board,
            1,
        )

        layout.addWidget(hint)

        return container

    def _create_enemy_board_area(self) -> QWidget:
        container = QFrame()
        container.setObjectName("boardContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        title = QLabel("ENEMY BOARD - TAKE YOUR SHOT")
        title.setObjectName("boardTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.enemy_board = BoardWidget()

        empty_footer = QLabel()
        empty_footer.setFixedHeight(55)

        layout.addWidget(title)

        layout.addWidget(
            self.enemy_board,
            1,
        )

        layout.addWidget(empty_footer)

        return container

    def _create_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(220)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        game_info_frame = QFrame()
        game_info_frame.setObjectName("panelFrame")

        game_info_layout = QVBoxLayout(game_info_frame)
        game_info_layout.setContentsMargins(10, 10, 10, 10)

        self.game_info_panel = GameInfoPanel()

        game_info_layout.addWidget(self.game_info_panel)

        surrender_button = QPushButton("⚑  SURRENDER")
        surrender_button.setObjectName("surrenderButton")
        surrender_button.setMinimumHeight(65)

        layout.addWidget(game_info_frame, 1)
        layout.addWidget(surrender_button)

        return panel

    def _create_bottom_panel(self) -> QWidget:
        container = QFrame()
        container.setObjectName("bottomPanel")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 8, 15, 8)

        self.bottom_status_panel = BottomStatusPanel()

        layout.addWidget(self.bottom_status_panel)

        return container

    def _apply_style(self) -> None:
        background_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "backgrounds"
            / "background.png"
        ).as_posix()

        self.setStyleSheet(f"""
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

            #header {{
                background-color: transparent;
                border: none;
            }}

            #gameTitle {{
                background-color: transparent;
                color: #e6edf2;
                font-size: 38px;
                font-weight: bold;
                letter-spacing: 2px;
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
                background-color: rgba(8, 25, 37, 190);
                border: 1px solid #29485d;
                border-radius: 8px;
            }}

            #panelTitle {{
                background-color: rgba(16, 41, 59, 230);
                border-bottom: 1px solid #29485d;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }}

            #boardContainer {{
                background-color: rgba(6, 23, 37, 175);
                border: 1px solid #24516d;
                border-radius: 8px;
            }}

            #boardTitle {{
                background-color: rgba(16, 63, 96, 230);
                border: 1px solid #2776a5;
                border-radius: 5px;
                padding: 10px;
                font-size: 17px;
                font-weight: bold;
            }}

            #hintLabel {{
                padding: 5px;
                font-size: 15px;
                font-weight: bold;
                color: #cbd8e0;
            }}

            QListWidget {{
                background-color: transparent;
                border: none;
                font-size: 15px;
            }}

            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid #183244;
            }}

            QListWidget::item:selected {{
                background-color: #17405a;
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

            #surrenderButton {{
                background-color: #7d1d13;
                border: 1px solid #c94739;
                font-size: 17px;
            }}

            #surrenderButton:hover {{
                background-color: #9f281b;
            }}

            #bottomPanel {{
                background-color: rgba(7, 24, 36, 180);
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
                background-color: rgba(16, 42, 59, 180);
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
        """)

    def _connect_signals(self) -> None:
        print("CONNECTING SIGNALS")

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

        self.control_panel.place_clicked.connect(
            self._place_selected_ship
        )
        self.control_panel.ready_clicked.connect(
            self._ready
        )

        print("PLACE SIGNAL CONNECTED")

    def _select_ship(self, ship_name: str) -> None:
        self.selected_ship_name = ship_name
        self.selected_ship_position = None

    def _select_orientation(
        self,
        orientation: str,
    ) -> None:
        self.selected_orientation = orientation

    def _ready(self) -> None:
        required_fleet = {
            "Battleship": 1,
            "Cruiser": 2,
            "Destroyer": 3,
            "Patrol Boat": 4,
        }

        for ship_name, required_count in required_fleet.items():
            actual_count = sum(
                1
                for ship in self.game_manager.player.board.ships
                if ship.name == ship_name
            )

            if actual_count != required_count:
                return

        self.game_manager.computer_ai.place_fleet(
            self.game_manager.computer.board
        )

        self.control_panel.set_placement_controls_enabled(False)
        self.control_panel.set_ready_enabled(False)

        self.game_manager.start_game()
    def _select_board_position(
        self,
        row: int,
        column: int,
    ) -> None:
        if self.selected_ship_name is None:
            return

        board = self.game_manager.player.board

        existing_ship = board.get_ship_at(
            row,
            column,
        )

        if existing_ship is not None:
            if existing_ship.name == self.selected_ship_name:
                positions = existing_ship.positions.copy()

                if board.remove_ship(existing_ship):
                    for ship_row, ship_column in positions:
                        self.player_board.set_cell_empty(
                            ship_row,
                            ship_column,
                        )

                    remaining_count = sum(
                        1
                        for ship in board.ships
                        if ship.name == existing_ship.name
                    )

                    total_count = next(
                        count
                        for name, size, count, image_name
                        in self.fleet_panel.SHIPS
                        if name == existing_ship.name
                    )

                    self.fleet_panel.set_ship_remaining(
                        existing_ship.name,
                        total_count - remaining_count,
                    )

            return

        ship_data = next(
            (
                (name, size)
                for name, size, count, image_name
                in self.fleet_panel.SHIPS
                if name == self.selected_ship_name
            ),
            None,
        )

        if ship_data is None:
            return

        ship_name, ship_size = ship_data

        orientation = (
            Orientation.HORIZONTAL
            if self.selected_orientation == "horizontal"
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

        for ship_row, ship_column in ship.positions:
            self.player_board.set_cell_ship(
                ship_row,
                ship_column,
            )
            remaining_count = sum(
                1
                for existing_ship in board.ships
                if existing_ship.name == ship_name
            )

            total_count = next(
                count
                for name, size, count, image_name
                in self.fleet_panel.SHIPS
                if name == ship_name
            )

            self.fleet_panel.set_ship_remaining(
                ship_name,
                total_count - remaining_count,
            )
    def _player_shoot(
        self,
        row: int,
        column: int,
    ) -> None:
        if self.game_manager.state != GameState.PLAYER_TURN:
            return

        result = self.game_manager.player_shoot(
            row,
            column,
        )

        if result == ShotResult.ALREADY_SHOT:
            return

        if result == ShotResult.SUNK:
            sunk_ship = self.game_manager.computer.board.get_ship_at(
                row,
                column,
            )

            if sunk_ship is not None:
                for ship_row, ship_column in sunk_ship.positions:
                    self.enemy_board.set_cell_sunk(
                        ship_row,
                        ship_column,
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
        if self.game_manager.state == GameState.COMPUTER_TURN:
            QTimer.singleShot(
                1000,
                self._computer_shoot,
            )

        if self.game_manager.is_game_over:
            self._show_game_over()  

    def _new_game(self) -> None:
        self.game_manager.reset()

        self.selected_ship_name = None
        self.selected_ship_position = None
        self.selected_orientation = "horizontal"

        self.player_board.reset()
        self.enemy_board.reset()

        self.fleet_panel.reset()
        self.bottom_status_panel.set_status(
            "PLACE YOUR SHIPS"
        )

        self.control_panel.set_placement_controls_enabled(True)
        self.control_panel.set_ready_enabled(True)

    def _show_game_over(self) -> None:
        winner = self.game_manager.winner

        if winner is None:
            return

        if winner == self.game_manager.player:
            message = "YOU WIN!"
        else:
            message = "COMPUTER WINS!"

        self.control_panel.set_placement_controls_enabled(False)
        self.control_panel.set_ready_enabled(False)

        self.bottom_status_panel.set_status(message)

    def _computer_shoot(self) -> None:
        row, column = self.game_manager.computer_ai.choose_shot()

        result = self.game_manager.computer_shoot(
            row,
            column,
        )

        if result == ShotResult.SUNK:
            sunk_ship = self.game_manager.player.board.get_ship_at(
                row,
                column,
            )

            if sunk_ship is not None:
                for ship_row, ship_column in sunk_ship.positions:
                    self.player_board.set_cell_sunk(
                        ship_row,
                        ship_column,
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
    def _place_selected_ship(self) -> None:
        print("PLACE BUTTON CLICKED")

        if self.selected_ship_name is None:
            return

        if self.selected_ship_position is None:
            return

        ship_data = next(
            (
                (name, size)
                for name, size, count, image_name
                in self.fleet_panel.SHIPS
                if name == self.selected_ship_name
            ),
            None,
        )

        if ship_data is None:
            return

        ship_name, ship_size = ship_data

        ship = Ship(
            name=ship_name,
            size=ship_size,
        )

        row, column = self.selected_ship_position

        placed = self.game_manager.player.board.place_ship(
            ship,
            row,
            column,
        )

        print("Placed:", placed)

        if not placed:
            return

        for ship_row, ship_column in ship.positions:
            self.player_board.set_cell_ship(
                ship_row,
                ship_column,
            )

        self.selected_ship_name = None
        self.selected_ship_position = None