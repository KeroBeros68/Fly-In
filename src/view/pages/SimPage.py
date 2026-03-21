import logging

from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QTextEdit,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPen,
)

from src.graph.Graph import Graph
from src.graph.node import Node
from src.view.components.Button import Button
from src.view.components.Title import Title
from src.view.pages.Page import Page

logger = logging.getLogger("Fly-In")


class SimPage(Page):
    def __init__(self) -> None:
        super().__init__()
        self.font_family = self._load_fonts()
        self.graph: Graph | None = None
        self.title_label: QLabel | None = None
        self.scene: QGraphicsScene | None = None

    def _load_graph(self, graph: Graph) -> None:
        self.graph = graph
        if self.title_label is not None:
            self.title_label.setText(self.graph.name)
        if self.scene is not None:
            self.draw_graph(self.graph)

    def create_page(self, stack: QStackedWidget) -> QWidget:
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        header_layout = QHBoxLayout()
        btn_back = Button(
            "<--", 50, 50, "#be123c", "#121212", self.font_family
        )
        btn_back.clicked.connect(lambda: stack.setCurrentIndex(0))

        graph_name = (
            self.graph.name if self.graph is not None else "Simulation"
        )
        self.title_label = Title(graph_name, self.font_family)

        header_layout.addWidget(btn_back)
        header_layout.addStretch()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addSpacing(50)
        main_layout.addLayout(header_layout)

        self.scene = QGraphicsScene()
        view = QGraphicsView(self.scene)
        view.setStyleSheet(
            "background-color: #121212; border: 1px solid #00FFCC;"
        )

        overlay_layout = QVBoxLayout(view)
        overlay_layout.setContentsMargins(
            0, 0, 0, 0
        )

        log_container = QWidget()
        log_container_layout = QVBoxLayout(log_container)
        log_container_layout.setContentsMargins(5, 5, 5, 5)
        log_container_layout.addStretch()

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setFixedHeight(280)

        self.log_console.setStyleSheet(
            """
            QTextEdit {
                background-color: transparent;
                color: #00FFCC;
                border: none;
                font-family: 'Consolas';
            }
        """
        )

        self.log_console.document().contentsChanged.connect(
            self._scroll_log_to_bottom
        )

        log_container_layout.addWidget(self.log_console)

        log_container.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
                border: none
            }
        """
        )

        log_container.setFixedHeight(300)
        log_container.setContentsMargins(10, 10, 10, 10)

        overlay_layout.addStretch()
        overlay_layout.addWidget(
            log_container, alignment=Qt.AlignmentFlag.AlignBottom
        )
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        main_layout.addWidget(view)

        for _ in range(6):
            self.log_console.append("\n")
        self.log_console.append(
            "Fly-In system initialized... Ready for takeoff."
        )
        return widget

    def draw_graph(self, graph: Graph) -> None:
        if self.scene is None:
            return

        assert self.scene is not None
        scene: QGraphicsScene = self.scene
        scene.clear()

        scale: int = 150
        node_size: int = 40
        offset: int = node_size // 2

        node_positions = {node.name: node.pos for node in graph.nodes.values()}

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
                scene.addLine(
                    x1 * scale,
                    y1 * scale,
                    x2 * scale,
                    y2 * scale,
                    pen_line,
                )

        def __draw_hub(node: Node) -> None:
            orig_x, orig_y = node.pos
            x = orig_x * scale
            y = orig_y * scale

            node_color = (
                node.color if hasattr(node, "color") and node.color else "cyan"
            )
            scene.addEllipse(
                x - offset,
                y - offset,
                node_size,
                node_size,
                QPen(Qt.GlobalColor.white),
                QBrush(QColor(node_color)),
            )

            text = scene.addText(node.name)
            text.setDefaultTextColor("white")
            text.setPos(x - offset, y - offset - 25)

        for node in graph.nodes.values():
            __draw_hub(node)

        rect = scene.itemsBoundingRect()

        padding = 120

        scene.setSceneRect(rect.adjusted(-padding, 0, padding, padding))

    def log_move(self, tour: str, texte: str) -> None:
        self.log_console.append(
            f"<b style='color:white;'>[TOUR {tour}]</b> : {texte}"
        )

    def _scroll_log_to_bottom(self) -> None:
        sb = self.log_console.verticalScrollBar()
        sb.setValue(sb.maximum())
