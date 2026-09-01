from __future__ import annotations

import random

from PySide6.QtCore import QPointF, QTimer, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


class FireworksWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        self.particles: list[dict] = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animation)

    def start(self) -> None:
        self.particles.clear()
        self._create_fireworks()
        self.show()
        self.raise_()
        self.timer.start(30)

    def stop(self) -> None:
        self.timer.stop()
        self.particles.clear()
        self.hide()
        self.update()

    def _create_fireworks(self) -> None:
        for _ in range(5):
            center_x = random.randint(
                int(self.width() * 0.15),
                int(self.width() * 0.85),
            )
            center_y = random.randint(
                int(self.height() * 0.15),
                int(self.height() * 0.65),
            )

            color = QColor(
                random.randint(120, 255),
                random.randint(120, 255),
                random.randint(120, 255),
            )

            for _ in range(35):
                angle = random.uniform(0, 6.283185)
                speed = random.uniform(2.0, 6.0)

                self.particles.append(
                    {
                        "position": QPointF(
                            center_x,
                            center_y,
                        ),
                        "velocity": QPointF(
                            speed * __import__("math").cos(angle),
                            speed * __import__("math").sin(angle),
                        ),
                        "life": random.randint(30, 55),
                        "color": color,
                    }
                )

    def _update_animation(self) -> None:
        for particle in self.particles:
            particle["position"] += particle["velocity"]
            particle["velocity"].setY(
                particle["velocity"].y() + 0.08
            )
            particle["life"] -= 1

        self.particles = [
            particle
            for particle in self.particles
            if particle["life"] > 0
        ]

        if not self.particles:
            self._create_fireworks()

        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        for particle in self.particles:
            life = particle["life"]
            alpha = min(255, life * 8)

            color = QColor(particle["color"])
            color.setAlpha(alpha)

            painter.setPen(
                QPen(
                    color,
                    7,
                )
            )

            position = particle["position"]

            painter.drawPoint(position)