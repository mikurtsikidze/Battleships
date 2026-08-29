from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class FleetPanel(QWidget):
    ship_selected = Signal(str)

    SHIPS = (
        ("Battleship", 4, 1, "ship_1.png"),
        ("Cruiser", 3, 2, "ship_2.png"),
        ("Destroyer", 2, 3, "ship_3.png"),
        ("Patrol Boat", 1, 4, "ship_4.png"),
    )

    def __init__(self) -> None:
        super().__init__()

        self.ship_rows: dict[str, QWidget] = {}
        self.ship_images_dir = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "images"
            / "ships"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        for name, size, count, image_name in self.SHIPS:
            ship_row = self._create_ship_row(
                name,
                size,
                count,
                image_name,
            )

            layout.addWidget(ship_row)
            self.ship_rows[name] = ship_row

        layout.addStretch()

    def _create_ship_row(
        self,
        name: str,
        size: int,
        count: int,
        image_name: str,
    ) -> QWidget:
        frame = QFrame()
        frame.setObjectName("shipRow")
        frame.setMinimumHeight(82)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)

        ship_column = QVBoxLayout()
        ship_column.setSpacing(2)
        ship_column.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(name)
        name_label.setObjectName("shipName")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ship_image = self._create_ship_image(image_name)
        ship_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ship_column.addWidget(name_label)
        ship_column.addWidget(ship_image)

        remaining_label = QLabel(f"x{count}")
        remaining_label.setObjectName("shipCount")
        remaining_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        remaining_label.setFixedWidth(35)

        count_colors = {
            1: "#5ee06b",
            2: "#f5c542",
            3: "#ff8a2a",
            4: "#ff4d3d",
        }

        remaining_label.setStyleSheet(
            f"""
            QLabel {{
                color: {count_colors[count]};
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
            """
        )

        layout.addLayout(ship_column)
        layout.addStretch()
        layout.addWidget(remaining_label)

        return frame

    def _create_ship_image(
        self,
        image_name: str,
    ) -> QLabel:
        image_label = QLabel()
        image_label.setObjectName("shipImage")
        image_label.setFixedSize(80, 45)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_path = self.ship_images_dir / image_name

        pixmap = QPixmap(str(image_path))

        if not pixmap.isNull():
            image_label.setPixmap(
                pixmap.scaled(
                    image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        return image_label

    def mousePressEvent(self, event) -> None:
        child = self.childAt(event.position().toPoint())

        while child is not None:
            for name, ship_row in self.ship_rows.items():
                if child is ship_row:
                    self.ship_selected.emit(name)
                    return

            child = child.parentWidget()

        super().mousePressEvent(event)

    def set_ship_remaining(
        self,
        ship_name: str,
        count: int,
    ) -> None:
        ship_row = self.ship_rows.get(ship_name)

        if ship_row is None:
            return

        count_label = ship_row.findChild(
            QLabel,
            "shipCount",
        )

        if count_label is not None:
            count_label.setText(f"x{count}")

    def remove_ship(self, ship_name: str) -> None:
        self.set_ship_remaining(ship_name, 0)

        ship_row = self.ship_rows.get(ship_name)

        if ship_row is not None:
            ship_row.setEnabled(False)

    def reset(self) -> None:
        for name, size, count, image_name in self.SHIPS:
            self.set_ship_remaining(name, count)

            ship_row = self.ship_rows.get(name)

            if ship_row is not None:
                ship_row.setEnabled(True)

    def update_ship_counts(
        self,
        ships: dict[str, int],
    ) -> None:
        for ship_name, count in ships.items():
            self.set_ship_remaining(ship_name, count)