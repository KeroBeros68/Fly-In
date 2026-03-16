import os

from PySide6 import QtWidgets
from PySide6.QtGui import QFontDatabase

from src.view.ViewQT import ViewQT


class ViewApp:
    def __init__(self) -> None:
        self.app = QtWidgets.QApplication([])

        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir,
            "assets",
            "font",
            "Orbitron-VariableFont_wght.ttf",
        )
        font_id = QFontDatabase.addApplicationFont(font_path)

        font_family_list = QFontDatabase.applicationFontFamilies(font_id)
        if font_family_list:
            font_family = font_family_list[0]

        self.app.setStyleSheet(
            f"""
            * {{
                background-color: #121212;
                color: white;
            }}
            QLabel {{
                font-family: '{font_family}';
                color: white;
                background: transparent;
            }}
            QPushButton {{
                font-family: '{font_family}';
                background-color: #333;
                border: 2px solid #00ffcc;
                color: #00ffcc;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #00ffcc;
                color: black;
            }}
            QGraphicsView {{
                background-color: #121212;
            }}
        """
        )

        self.app_window = ViewQT()
        self.app_window.setMinimumSize(800, 600)
        self.app_window.setMaximumSize(1920, 1080)
        self.app_window.resize(1920, 1080)
        self.app_window.show()
