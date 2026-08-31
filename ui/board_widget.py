from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class BoardWidget(QWidget):
    BOARD_SIZE = 10
    MIN_CELL_SIZE = 24
    HEADER_SIZE = 28

    cell_clicked = Signal(int, int)

    def __init__(self) -> None:
        super().__init__()

        self.cells: list[list[QPushButton]] = []
        self.column_labels: list[QLabel] = []
        self.row_labels: list[QLabel] = []

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(2)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.corner_label = QLabel()
        self.grid_layout.addWidget(
            self.corner_label,
            0,
            0,
        )

        self._create_board()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_cell_sizes()

    def _create_board(self) -> None:
        for column in range(self.BOARD_SIZE):
            label = QLabel(str(column + 1))
            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            label.setStyleSheet(
                """
                QLabel {
                    color: #d9e5ec;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: transparent;
                }
                """
            )

            self.grid_layout.addWidget(
                label,
                0,
                column + 1,
            )

            self.column_labels.append(label)

        for row in range(self.BOARD_SIZE):
            row_label = QLabel(
                chr(ord("A") + row)
            )
            row_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            row_label.setStyleSheet(
                """
                QLabel {
                    color: #d9e5ec;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: transparent;
                }
                """
            )

            self.grid_layout.addWidget(
                row_label,
                row + 1,
                0,
            )

            self.row_labels.append(row_label)

            row_cells: list[QPushButton] = []

            for column in range(self.BOARD_SIZE):
                cell = QPushButton()

                cell.setSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Expanding,
                )

                cell.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #2d6f9f;
                        border: 1px solid #163d5c;
                    }

                    QPushButton:hover {
                        background-color: #3d8fc7;
                    }
                    """
                )

                cell.clicked.connect(
                    lambda checked=False, r=row, c=column:
                    self.cell_clicked.emit(r, c)
                )

                self.grid_layout.addWidget(
                    cell,
                    row + 1,
                    column + 1,
                )

                row_cells.append(cell)

            self.cells.append(row_cells)

    def _update_cell_sizes(self) -> None:
        spacing = self.grid_layout.spacing()

        available_width = (
            self.width()
            - self.HEADER_SIZE
            - spacing * self.BOARD_SIZE
        )

        available_height = (
            self.height()
            - self.HEADER_SIZE
            - spacing * self.BOARD_SIZE
        )

        cell_size = min(
            available_width // self.BOARD_SIZE,
            available_height // self.BOARD_SIZE,
        )

        cell_size = max(
            self.MIN_CELL_SIZE,
            cell_size,
        )

        self.corner_label.setFixedSize(
            self.HEADER_SIZE,
            self.HEADER_SIZE,
        )

        for label in self.column_labels:
            label.setFixedSize(
                cell_size,
                self.HEADER_SIZE,
            )

        for label in self.row_labels:
            label.setFixedSize(
                self.HEADER_SIZE,
                cell_size,
            )

        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.cells[row][column].setFixedSize(
                    cell_size,
                    cell_size,
                )

    def set_cell_empty(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cells[row][column].setText("")
        self.cells[row][column].setStyleSheet(
            """
            QPushButton {
                background-color: #2d6f9f;
                border: 1px solid #163d5c;
            }

            QPushButton:hover {
                background-color: #3d8fc7;
            }
            """
        )

    def set_cell_ship(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cells[row][column].setText("")
        self.cells[row][column].setStyleSheet(
            """
            QPushButton {
                background-color: #546e7a;
                border: 1px solid #263238;
            }
            """
        )

    def set_cell_hit(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cells[row][column].setText("X")
        self.cells[row][column].setStyleSheet(
            """
            QPushButton {
                background-color: #c62828;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #7f0000;
            }
            """
        )

    def set_cell_miss(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cells[row][column].setText("•")
        self.cells[row][column].setStyleSheet(
            """
            QPushButton {
                background-color: #90caf9;
                color: #0d47a1;
                font-size: 20px;
                font-weight: bold;
                border: 1px solid #1565c0;
            }
            """
        )

    def set_cell_sunk(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cells[row][column].setText("☠")
        self.cells[row][column].setStyleSheet(
            """
            QPushButton {
                background-color: #4a1f1f;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #8b3030;
            }
            """
        )   

    def reset(self) -> None:
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.set_cell_empty(
                    row,
                    column,
                )