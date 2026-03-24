import logging
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QStackedWidget,
)

from PySide6.QtGui import QIcon
import os

if TYPE_CHECKING:
    from src.Controller import Controller
from src.view.pages.SimPage import SimPage
from src.view.pages.MenuPage import MenuPage

logger = logging.getLogger("Fly-In")


class ViewQT(QMainWindow):

    def __init__(self, controller: "Controller") -> None:
        super().__init__()

        self.controller = controller

        self.setWindowTitle("Fly-In Simulator")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(
            current_dir, "assets", "drone_router_icon.png"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu = MenuPage()
        self.menu_page = self.menu.create_page(self.stack)
        self.menu.file_selected.connect(self.controller.load_file)
        self.controller.file_loaded.connect(
            lambda: self.menu.set_btn_enabled(self.menu.btn_start, True)
        )
        self.controller.file_error.connect(
            lambda msg: QMessageBox.critical(self, "Erreur", msg)
        )

        self.sim = SimPage()
        self.sim_page = self.sim.create_page(self.stack)
        self.controller.load_graph.connect(self.sim._load_graph)
        self.controller.load_sim.connect(self.sim._load_sim)

        self.stack.addWidget(self.menu_page)  # Index 0
        self.stack.addWidget(self.sim_page)  # Index 1
