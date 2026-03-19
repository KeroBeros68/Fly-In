import logging

from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
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
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        header_layout = QHBoxLayout()

        btn_back = Button(
            "<--", 50, 50, "#be123c", "#121212", self.font_family
        )
        btn_back.clicked.connect(lambda: stack.setCurrentIndex(0))

        title_font = QFont(self.font_family, 32, QFont.Weight.Bold)

        title = QLabel("MAP NAME")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet(
            """
            color: #00FFCC;
            margin-bottom: 20px;
        """
        )

        self.glow = QGraphicsDropShadowEffect()
        self.glow.setColor(QColor("#00FFCC"))
        self.glow.setOffset(0, 0)
        self.glow.setBlurRadius(20)

        title.setGraphicsEffect(self.glow)

        self.anim = QPropertyAnimation(self.glow, b"blurRadius")
        self.anim.setStartValue(40)
        self.anim.setEndValue(90)
        self.anim.setDuration(3200)
        self.anim.setLoopCount(-1)
        self.anim.start()

        header_layout.addWidget(btn_back)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()

        header_layout.addSpacing(100)

        main_layout.addLayout(header_layout)

        main_layout.addStretch()

        return widget

    # def draw_graph(self, graph: Graph) -> None:
    #     """Replace splash with the graph view."""
    #     # Set the container (with title and graph) as central widget
    #     # ---- Scene graphique ----
    #     self.scene = QGraphicsScene()
    #     self.view = QGraphicsView(self.scene)
    #     self.scene.setBackgroundBrush(QColor("#0d1117"))

    #     # ---- Titre ----
    #     self.title = QLabel("Fly In - Drone Router")
    #     self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.title.setStyleSheet("font-size: 22px; font-weight: bold;")

    #     # ---- Scroll Area ----
    #     self.scroll_area = QScrollArea()
    #     self.scroll_area.setWidgetResizable(True)
    #     self.scroll_area.setWidget(self.view)

    #     # ---- Layout principal ----
    #     self.container = QWidget()
    #     self.layout_main = QVBoxLayout()

    #     self.layout_main.addWidget(self.title)
    #     self.layout_main.addWidget(self.scroll_area)

    #     self.container.setLayout(self.layout_main)

    #     self.setCentralWidget(self.container)

    #     self.scene.clear()  # Clear before redrawing

    #     scale: int = 150
    #     node_size: int = 40
    #     offset: int = node_size // 2

    #     # Create a dictionary to quickly find hub positions
    #     node_positions = {node.name: node.pos for node in
    # graph.nodes.values()}

    #     # Draw connections first so they appear under hubs
    #     for link in graph.links.values():
    #         names = link.name.split("-")
    #         if (
    #             len(names) == 2
    #             and names[0] in node_positions
    #             and names[1] in node_positions
    #         ):
    #             x1, y1 = node_positions[names[0]]
    #             x2, y2 = node_positions[names[1]]
    #             pen_line = QPen(QColor("#e2e8f0"))
    #             pen_line.setWidth(2)
    #             self.scene.addLine(
    #                 x1 * scale,
    #                 y1 * scale,
    #                 x2 * scale,
    #                 y2 * scale,
    #                 pen_line,
    #             )

    #     def __draw_hub(node: Node):
    #         orig_x, orig_y = node.pos
    #         x = orig_x * scale
    #         y = orig_y * scale

    #         # Create a circle centered on the point
    #         node_color = (
    #             node.color if hasattr(node, "color") and node.color else
    # "cyan"
    #         )
    #         self.scene.addEllipse(
    #             x - offset,
    #             y - offset,
    #             node_size,
    #             node_size,
    #             QPen(Qt.GlobalColor.black),
    #             QBrush(QColor(node_color)),
    #         )

    #         # Add hub name above
    #         text = self.scene.addText(node.name)
    #         text.setPos(x - offset, y - offset - 25)

    #     # Draw hubs
    #     for node in graph.nodes.values():
    #         __draw_hub(node)

    #     rect = self.scene.itemsBoundingRect()

    #     padding = 120

    #     self.scene.setSceneRect(
    #         rect.adjusted(-padding, -padding, padding, padding)
    #     )
