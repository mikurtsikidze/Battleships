from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class ControlPanel(QWidget):
    place_clicked = Signal()
    erase_clicked = Signal()
    rotate_clicked = Signal()
    ready_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)

        self.place_button = QPushButton("PLACE")
        self.erase_button = QPushButton("ERASE")
        self.rotate_button = QPushButton("ROTATE")
        self.ready_button = QPushButton("READY")

        self.place_button.setMinimumHeight(62)
        self.erase_button.setMinimumHeight(62)
        self.rotate_button.setMinimumHeight(58)
        self.ready_button.setMinimumHeight(62)

        self.ready_button.setObjectName("readyButton")

        top_layout.addWidget(self.place_button)
        top_layout.addWidget(self.erase_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.rotate_button)
        main_layout.addWidget(self.ready_button)

        self.place_button.clicked.connect(
            lambda: self.place_clicked.emit()
        )

        self.erase_button.clicked.connect(
            lambda: self.erase_clicked.emit()
        )

        self.rotate_button.clicked.connect(
            lambda: self.rotate_clicked.emit()
        )

        self.ready_button.clicked.connect(
            lambda: self.ready_clicked.emit()
        )

    def set_ready_enabled(self, enabled: bool) -> None:
        self.ready_button.setEnabled(enabled)

    def set_placement_controls_enabled(self, enabled: bool) -> None:
        self.place_button.setEnabled(enabled)
        self.erase_button.setEnabled(enabled)
        self.rotate_button.setEnabled(enabled)