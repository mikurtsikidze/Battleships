from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtGui import QIcon, QPainter, QPixmap, QTransform
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

        self.ship_images: list[
            tuple[
                list[tuple[int, int]],
                str,
                bool,
            ]
        ] = []

        self.cell_effects: dict[
            tuple[int, int],
            str,
        ] = {}

        self.sunk_effects: list[
            tuple[
                list[tuple[int, int]],
                QLabel,
            ]
        ] = []

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
        self._update_cell_effects()
        self._update_sunk_effects()

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

                self._set_cell_default_style(cell)

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

    def _set_cell_default_style(
        self,
        cell: QPushButton,
    ) -> None:
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
        position = (row, column)

        self.ship_images = [
            ship
            for ship in self.ship_images
            if position not in ship[0]
        ]

        self.cell_effects.pop(
            position,
            None,
        )

        for positions, label in self.sunk_effects[:]:
            if position in positions:
                label.deleteLater()
                self.sunk_effects.remove(
                    (positions, label)
                )

        cell = self.cells[row][column]

        cell.setText("")
        cell.setIcon(QIcon())

        self._set_cell_default_style(cell)

        self.update()

    def set_cell_ship(
        self,
        row: int,
        column: int,
    ) -> None:
        cell = self.cells[row][column]

        cell.setText("")
        cell.setIcon(QIcon())

        cell.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: 1px solid #263238;
            }
            """
        )

    def set_ship_image(
        self,
        positions: list[tuple[int, int]],
        image_path: str,
        vertical: bool = False,
    ) -> None:
        self.ship_images.append(
            (
                positions.copy(),
                image_path,
                vertical,
            )
        )

        self.update()

    def set_cell_hit(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cell_effects[(row, column)] = "hit"

        self._apply_cell_effect(
            row,
            column,
            "hit",
        )

    def set_cell_miss(
        self,
        row: int,
        column: int,
    ) -> None:
        self.cell_effects[(row, column)] = "miss"

        self._apply_cell_effect(
            row,
            column,
            "miss",
        )

    def _apply_cell_effect(
        self,
        row: int,
        column: int,
        effect_name: str,
    ) -> None:
        image_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "effects"
            / f"{effect_name}.png"
        )

        cell = self.cells[row][column]

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            return

        effect_pixmap = QPixmap(
            cell.size()
        )

        effect_pixmap.fill(
            Qt.GlobalColor.transparent
        )

        painter = QPainter(effect_pixmap)
        painter.setOpacity(0.60)

        painter.drawPixmap(
            effect_pixmap.rect(),
            pixmap,
        )

        painter.end()

        cell.setText("")
        cell.setIcon(
            QIcon(effect_pixmap)
        )
        cell.setIconSize(
            cell.size()
        )

        cell.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: 1px solid #7f0000;
            }
            """
        )

    def _update_cell_effects(self) -> None:
        for (row, column), effect_name in self.cell_effects.items():
            self._apply_cell_effect(
                row,
                column,
                effect_name,
            )

    def set_ship_sunk(
        self,
        positions: list[tuple[int, int]],
    ) -> None:
        if not positions:
            return

        image_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "effects"
            / "sunk.png"
        )

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            return

        label = QLabel(self)

        label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )

        self.sunk_effects.append(
            (
                positions.copy(),
                label,
            )
        )

        self._update_sunk_label(
            positions,
            label,
            pixmap,
        )

        label.show()
        label.raise_()

    def _update_sunk_effects(self) -> None:
        image_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "effects"
            / "sunk.png"
        )

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            return

        for positions, label in self.sunk_effects:
            self._update_sunk_label(
                positions,
                label,
                pixmap,
            )

    def _update_sunk_label(
        self,
        positions: list[tuple[int, int]],
        label: QLabel,
        pixmap: QPixmap,
    ) -> None:
        cells = [
            self.cells[row][column]
            for row, column in positions
        ]

        left = min(
            cell.geometry().left()
            for cell in cells
        )

        top = min(
            cell.geometry().top()
            for cell in cells
        )

        right = max(
            cell.geometry().right()
            for cell in cells
        )

        bottom = max(
            cell.geometry().bottom()
            for cell in cells
        )

        width = right - left + 1
        height = bottom - top + 1

        effect_pixmap = QPixmap(
            width,
            height,
        )

        effect_pixmap.fill(
            Qt.GlobalColor.transparent
        )

        painter = QPainter(effect_pixmap)
        painter.setOpacity(0.55)

        painter.drawPixmap(
            effect_pixmap.rect(),
            pixmap,
        )

        painter.end()

        label.setPixmap(effect_pixmap)

        label.setGeometry(
            left,
            top,
            width,
            height,
        )

        label.raise_()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform
        )

        for positions, image_path, vertical in self.ship_images:
            if not positions:
                continue

            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                continue

            if not vertical:
                pixmap = pixmap.transformed(
                    QTransform().rotate(90),
                    Qt.TransformationMode.SmoothTransformation,
                )

            cells = [
                self.cells[row][column]
                for row, column in positions
            ]

            x = min(
                cell.geometry().left()
                for cell in cells
            )

            y = min(
                cell.geometry().top()
                for cell in cells
            )

            right = max(
                cell.geometry().right()
                for cell in cells
            )

            bottom = max(
                cell.geometry().bottom()
                for cell in cells
            )

            target_rect = QRect(
                x,
                y,
                right - x + 1,
                bottom - y + 1,
            )

            painter.drawPixmap(
                target_rect,
                pixmap,
            )

    def reset(self) -> None:
        for _, label in self.sunk_effects:
            label.deleteLater()

        self.sunk_effects.clear()
        self.ship_images.clear()
        self.cell_effects.clear()

        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                cell = self.cells[row][column]

                cell.setText("")
                cell.setIcon(QIcon())

                self._set_cell_default_style(
                    cell
                )

        self.update()