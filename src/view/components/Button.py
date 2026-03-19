from PySide6.QtWidgets import (
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFont,
)


class Button(QPushButton):
    def __init__(
        self,
        name: str,
        width_x: int,
        height_y: int,
        color: str,
        hover_color: str,
        font_family: str,
    ) -> None:
        super().__init__(name)

        self.name: str = name
        self.width_x: int = width_x
        self.height_y: int = height_y
        self.color: str = color
        self.hover_color: str = hover_color
        self.font_family: str = font_family

        self.setFont(QFont(self.font_family, 12))
        self.setFixedWidth(self.width_x)
        self.setFixedHeight(self.height_y)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style pour coller au thème
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {self.color};
                color: {self.color};
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color};
                color: {self.hover_color};
            }}
            """
        )
