from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QLabel,
)
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
)


class Title(QLabel):
    def __init__(self, name: str, font_family) -> None:
        super().__init__(name)
        self.title_font = QFont(font_family, 32, QFont.Weight.Bold)
        self.name = name
        self.setFont(self.title_font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            """
                color: #00FFCC;
                margin-bottom: 20px;
            """
        )

        self.glow = QGraphicsDropShadowEffect()
        self.glow.setColor(QColor("#00FFCC"))
        self.glow.setOffset(0, 0)
        self.glow.setBlurRadius(20)

        self.setGraphicsEffect(self.glow)

        self.anim = QPropertyAnimation(self.glow, b"blurRadius")
        self.anim.setStartValue(40)
        self.anim.setEndValue(90)
        self.anim.setDuration(3200)
        self.anim.setLoopCount(-1)
        self.anim.start()
