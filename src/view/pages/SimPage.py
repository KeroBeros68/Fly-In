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
from PySide6.QtCore import QPointF, QPropertyAnimation, QTimer, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPen,
)

from src.graph.Graph import Graph
from src.graph.node import Node
from src.view.components.Drone import Drone
from src.view.components.Button import Button
from src.view.components.Title import Title
from src.view.pages.Page import Page


SCALE: int = 150
NODE_SIZE: int = 40
OFFSET: int = NODE_SIZE // 2


class SimPage(Page):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger("Fly-In")
        self.font_family = self._load_fonts()
        self.graph: Graph | None = None
        self.allpaths: dict[int, dict[int, str]] = {}
        self.title_label: QLabel | None = None
        self.drone_list: dict[int, Drone] = {}
        self.animations: list = []

    def _load_graph(self, graph: Graph) -> None:
        self.graph = graph
        if self.title_label is not None:
            self.title_label.setText(self.graph.name)
        if self.scene is not None:
            self.draw_graph(self.graph)

    def _load_sim(self, allpaths: dict[int, dict[int, str]]) -> None:
        self.allpaths = allpaths

    def _read_sim(self) -> None:
        if not self.allpaths:
            return
        self.log_remove()
        for _ in range(7):
            self.log_console.append("\n")
        self.log_console.append(
            "Fly-In system initialized... Ready for takeoff."
        )
        self.set_play_enabled(False)

        max_turn = max(
            [max(path.keys()) for path in self.allpaths.values() if path] + [0]
        )

        assert self.graph
        for drone_id in range(len(self.allpaths)):
            self._draw_drone(self.graph.nodes["start"].pos, drone_id + 1)

        for i in range(max_turn + 1):
            string = ""
            delay = i * 1000
            for drone_id, path in self.allpaths.items():
                path_node = path.get(i, None)
                if path_node:
                    string += f"D{drone_id}-{path_node} "
                    if "-" in path_node:
                        x1, y1 = self.graph.nodes[path_node.split("-")[0]].pos
                        x2, y2 = self.graph.nodes[path_node.split("-")[1]].pos
                        x = (x1 * SCALE + x2 * SCALE) / 2 / SCALE
                        y = (y1 * SCALE + y2 * SCALE) / 2 / SCALE
                    else:
                        x1, y1 = self.graph.nodes[path_node].pos
                        x = x1
                        y = y1
                    QTimer.singleShot(
                        delay,
                        lambda did=drone_id, x=x, y=y: self._animate_drone(
                            self.drone_list[did],
                            x,
                            y,
                        ),
                    )
            if string:
                self.log_move(str(i), string)

        QTimer.singleShot(
            (max_turn + 1) * 1000, lambda: self.set_play_enabled(True)
        )
        self.set_play_enabled(True)

    def _get_disabled_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #333333;
                color: #777777;
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """

    def _get_enabled_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #121212;
                color: #00FFCC;
                border: 2px solid #00FFCC;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00FFCC;
                color: #121212;
            }
        """

    def set_play_enabled(self, enabled: bool) -> None:
        self.btn_play.setEnabled(enabled)
        if enabled:
            self.btn_play.setStyleSheet(self._get_enabled_button_style())
        else:
            self.btn_play.setStyleSheet(self._get_disabled_button_style())

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
        view.setStyleSheet("background-color: #121212;")

        overlay_layout = QVBoxLayout(view)
        overlay_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_play = Button(
            ">", 50, 50, "#00FFCC", "#121212", self.font_family
        )
        self.btn_play.clicked.connect(lambda: self._read_sim())

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

        overlay_layout.addWidget(self.btn_play)
        overlay_layout.addStretch()
        overlay_layout.addWidget(
            log_container, alignment=Qt.AlignmentFlag.AlignBottom
        )
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        main_layout.addWidget(view)

        self.log_remove()
        for _ in range(7):
            self.log_console.append("\n")
        self.log_console.append(
            "Fly-In system initialized... Ready for takeoff."
        )
        return widget

    def draw_graph(self, graph: Graph) -> None:
        if self.scene is None:
            return

        scene: QGraphicsScene = self.scene
        scene.clear()

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
                    x1 * SCALE,
                    y1 * SCALE,
                    x2 * SCALE,
                    y2 * SCALE,
                    pen_line,
                )

        def __draw_hub(node: Node) -> None:
            orig_x, orig_y = node.pos
            x = orig_x * SCALE
            y = orig_y * SCALE

            node_color = (
                node.color if hasattr(node, "color") and node.color else "cyan"
            )
            scene.addEllipse(
                x - OFFSET,
                y - OFFSET,
                NODE_SIZE,
                NODE_SIZE,
                QPen(Qt.GlobalColor.white),
                QBrush(QColor(node_color)),
            )

            text = scene.addText(node.name)
            text.setDefaultTextColor("white")
            text.setPos(x - OFFSET, y - OFFSET - 25)

        for node in graph.nodes.values():
            __draw_hub(node)

        rect = scene.itemsBoundingRect()

        padding = 120

        scene.setSceneRect(rect.adjusted(-padding, 0, padding, padding))

    def _draw_drone(self, position: tuple[int, int], id: int) -> None:

        x, y = position
        self.drone_list[id] = Drone(
            x - OFFSET / 2, y - OFFSET / 2, NODE_SIZE / 2, NODE_SIZE / 2
        )

        self.scene.addItem(self.drone_list[id])

    def _animate_drone(self, drone: Drone, x, y) -> None:
        animation = QPropertyAnimation(drone, b"position")
        animation.setDuration(800)
        animation.setEndValue(
            QPointF(x * SCALE - OFFSET / 2, y * SCALE - OFFSET / 2)
        )
        animation.start()
        self.animations.append(animation)

    def log_move(self, tour: str, texte: str) -> None:
        self.log_console.append(
            f"<b style='color:white;'>[TOUR {tour}]</b> : {texte}\n"
        )

    def log_remove(self) -> None:
        self.log_console.clear()

    def _scroll_log_to_bottom(self) -> None:
        sb = self.log_console.verticalScrollBar()
        sb.setValue(sb.maximum())
