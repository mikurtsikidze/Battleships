from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget


class BoardWidget(QWidget):
    BOARD_SIZE = 10

    cell_clicked = Signal(int, int)

    def __init__(self) -> None:
        super().__init__()

        self.cells: list[list[QPushButton]] = []

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(2)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self._create_board()

    def _create_board(self) -> None:
        for row in range(self.BOARD_SIZE):
            row_cells: list[QPushButton] = []

            for column in range(self.BOARD_SIZE):
                cell = QPushButton()
                cell.setFixedSize(45, 45)
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

                self.grid_layout.addWidget(cell, row, column)
                row_cells.append(cell)

            self.cells.append(row_cells)

    def set_cell_ship(
        self,
        row: int,
        column: int,
    ) -> None:
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

    def reset(self) -> None:
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                cell = self.cells[row][column]

                cell.setText("")
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