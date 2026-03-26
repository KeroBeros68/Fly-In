from PySide6.QtWidgets import (
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFont,
)


class Button(QPushButton):
    """
    A styled QPushButton with a fixed size, custom color, and hover effect.
    """

    def __init__(
        self,
        name: str,
        width_x: int,
        height_y: int,
        color: str,
        hover_color: str,
        font_family: str,
    ) -> None:
        """
        Initializes the Button with label, dimensions, colors, and font.

        Args:
            name (str): The button label text.
            width_x (int): Fixed button width in pixels.
            height_y (int): Fixed button height in pixels.
            color (str): Border and text color (hex string).
            hover_color (str): Text color on hover.
            font_family (str): Font family to use for the label.
        """
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
