import os

from PySide6.QtWidgets import (
    QWidget,
)
from PySide6.QtGui import (
    QFontDatabase,
)


class Page(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.font_family = self._load_fonts()

    def _load_fonts(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir, "..", "assets", "fonts", "Orbitron-Bold.ttf"
        )

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
        return "Arial"
