import logging

from PySide6.QtWidgets import (
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFontDatabase,
)
import os

from src.view.components.Button import Button

logger = logging.getLogger("Fly-In")


class SimPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.font_family = self._load_fonts()

    def _load_fonts(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir, "..", "assets", "fonts", "Orbitron-Bold.ttf"
        )

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
        return "Arial"  # Fallback si le fichier est manquant

    def create_page(self, stack: QStackedWidget) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_start = Button(
            "<---", 200, 200, "#00FFCC", "#121212", self.font_family
        )
        btn_start.clicked.connect(lambda: stack.setCurrentIndex(0))

        # Organisation
        layout.addStretch()
        layout.addSpacing(50)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(50)
        layout.addStretch()

        return widget
