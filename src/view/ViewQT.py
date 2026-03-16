from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QGraphicsScene,
    QGraphicsView,
    QWidget,
    QVBoxLayout,
    QScrollArea,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor, QIcon, QPixmap
import os

from src.graph.Graph import Graph
from src.graph.node.Node import Node


class ViewQT(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Fly In")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(
            current_dir, "..", "..", "assets", "drone_router_icon.png"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # ---- Scene graphique ----
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.scene.setBackgroundBrush(QColor("#0d1117"))

        # ---- Titre ----
        self.title = QLabel("Fly In - Drone Router")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")

        # ---- Scroll Area ----
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.view)

        # ---- Layout principal ----
        self.container = QWidget()
        self.layout_main = QVBoxLayout()

        self.layout_main.addWidget(self.title)
        self.layout_main.addWidget(self.scroll_area)

        self.container.setLayout(self.layout_main)

        self.start_frame()

    def start_frame(self) -> None:
        """Display the splash screen with the icon."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(
            current_dir, "assets", "drone_router_icon.png"
        )

        label = QLabel()
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            label.setPixmap(
                pixmap.scaled(
                    400,
                    400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

    def draw_graph(self, graph: Graph) -> None:
        """Replace splash with the graph view."""
        # Set the container (with title and graph) as central widget
        self.setCentralWidget(self.container)

        self.scene.clear()  # Clear before redrawing

        scale: int = 150
        node_size: int = 40
        offset: int = node_size // 2

        # Create a dictionary to quickly find hub positions
        node_positions = {node.name: node.pos for node in graph.nodes.values()}

        # Draw connections first so they appear under hubs
        for link in graph.links.values():
            names = link.name.split("-")
            if (
                len(names) == 2
                and names[0] in node_positions
                and names[1] in node_positions
            ):
                x1, y1 = node_positions[names[0]]
                x2, y2 = node_positions[names[1]]
                pen_line = QPen(QColor("#e2e8f0"))
                pen_line.setWidth(2)
                self.scene.addLine(
                    x1 * scale,
                    y1 * scale,
                    x2 * scale,
                    y2 * scale,
                    pen_line,
                )

        def __draw_hub(node: Node):
            orig_x, orig_y = node.pos
            x = orig_x * scale
            y = orig_y * scale

            # Create a circle centered on the point
            node_color = (
                node.color if hasattr(node, "color") and node.color else "cyan"
            )
            self.scene.addEllipse(
                x - offset,
                y - offset,
                node_size,
                node_size,
                QPen(Qt.GlobalColor.black),
                QBrush(QColor(node_color)),
            )

            # Add hub name above
            text = self.scene.addText(node.name)
            text.setPos(x - offset, y - offset - 25)

        # Draw hubs
        for node in graph.nodes.values():
            __draw_hub(node)

        rect = self.scene.itemsBoundingRect()

        padding = 120

        self.scene.setSceneRect(
            rect.adjusted(-padding, -padding, padding, padding)
        )
