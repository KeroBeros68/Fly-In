import logging

from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
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
    """
    The simulation view page displaying the graph, drone animations, and logs.

    Manages the graphical scene, drone objects, and simulation replay.
    """

    def __init__(self) -> None:
        """Initializes the SimPage with default state."""
        super().__init__()
        self.logger = logging.getLogger("Fly-In")
        self.font_family = self._load_fonts()
        self.graph: Graph | None = None
        self.allpaths: dict[int, dict[int, str]] = {}
        self.metrics: dict[str, str] = {}
        self.title_label: QLabel | None = None
        self.drone_list: dict[int, Drone] = {}
        self.animations: list[QPropertyAnimation] = []
        self.node_labels: dict[str, tuple[QGraphicsTextItem, int]] = {}

    def _load_graph(self, graph: Graph) -> None:
        """
        Stores the graph and redraws it on the scene if already set up.

        Args:
            graph (Graph): The graph to display.
        """
        self.graph = graph
        if self.title_label is not None:
            self.title_label.setText(self.graph.name)
        if self.scene is not None:
            self.draw_graph(self.graph)

    def _load_sim(self, allpaths: dict[int, dict[int, str]]) -> None:
        """
        Stores the simulation paths for replay.

        Args:
            allpaths (dict[int, dict[int, str]]): Per-drone turn-to-node
            mapping.
        """
        self.allpaths = allpaths

    def _load_metrics(self, metrics: dict[str, str]) -> None:
        """
        Stores the metrics to display after simulation.

        Args:
            metrics (dict[str, str]): Key-value pairs of simulation statistics.
        """
        self.metrics = metrics

    def _read_sim(self) -> None:
        """
        Replays the simulation by animating drones turn-by-turn using QTimer.

        Reads stored paths and schedules animations and log updates for each
        turn.
        """
        if not self.allpaths:
            return
        self.log_remove()
        self.set_btn_enabled(self.btn_play, False)

        max_turn = max(
            [max(path.keys()) for path in self.allpaths.values() if path] + [0]
        )

        assert self.graph
        for drone_id in range(len(self.allpaths)):
            self._draw_drone(self.graph.nodes["start"].pos, drone_id + 1)

        for i in range(max_turn + 1):
            string = ""
            delay = i * 1000
            turn_move = {}
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

                    turn_move[drone_id] = (x, y)

            QTimer.singleShot(
                delay,
                lambda turn_move=turn_move, i=i, string=string:
                self.__log_and_animate(
                    turn_move, i, string
                ),
            )

        QTimer.singleShot(
            (max_turn + 1) * 1000,
            lambda: self.set_btn_enabled(self.btn_play, True),
        )
        self.write_metrics()

    def __log_and_animate(
        self, turn_move: dict[int, tuple[int, int]], i: int, string: str
    ) -> None:
        """
        Animates drones for a given turn and logs the movement string.

        Args:
            turn_move (dict[int, tuple[int, int]]): Drone positions for this
            turn.
            i (int): The turn index.
            string (str): The formatted movement string to log.
        """
        self._animate_drone(turn_move)
        self.log_move(str(i), string)
        self._update_node_labels(i)
        self._update_link_labels(i)

    def _update_node_labels(self, turn: int) -> None:
        """Updates each node's occupancy label for the given turn."""
        self.occ: dict[str, int] = {}
        for path in self.allpaths.values():
            past_keys = [key for key in path if key <= turn]
            if not past_keys:
                continue
            pos = path[max(past_keys)]
            if pos and "-" not in pos:
                self.occ[pos] = self.occ.get(pos, 0) + 1

        for node_name, (text_item, max_drones) in self.node_labels.items():
            current = self.occ.get(node_name, 0)
            text_item.setPlainText(f"{node_name}: {current}/{max_drones}")
            color = (
                "red" if current >= max_drones and max_drones > 0 else "white"
            )
            text_item.setDefaultTextColor(QColor(color))

    def _update_link_labels(self, turn: int) -> None:
        """Updates each link's occupancy label for the given turn."""
        link_occ: dict[str, int] = {}
        for path in self.allpaths.values():
            past_keys = [key for key in path if key <= turn]
            if not past_keys:
                continue
            pos = path[max(past_keys)]
            if pos and "-" in pos:
                link_occ[pos] = link_occ.get(pos, 0) + 1

        for link_name, (text_item, connection_max) in self.link_labels.items():
            current = link_occ.get(link_name, 0)
            max_cap = connection_max or 1
            text_item.setPlainText(f"{current}/{max_cap}")
            color = (
                "red"
                if current >= max_cap
                else "white"
            )
            text_item.setDefaultTextColor(QColor(color))

    def create_page(self, stack: QStackedWidget) -> QWidget:
        """
        Builds and returns the simulation page widget.

        Args:
            stack (QStackedWidget): The navigation stack for the back button.

        Returns:
            QWidget: The fully constructed simulation page widget.
        """
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        header_layout = QHBoxLayout()
        btn_back = Button(
            "<--", 50, 50, "#be123c", "#121212", self.font_family
        )

        def __go_back() -> None:
            self.log_remove()
            self.remove_metrics()
            stack.setCurrentIndex(0)

        btn_back.clicked.connect(__go_back)

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
        log_container_layout = QHBoxLayout(log_container)
        log_container_layout.setContentsMargins(5, 5, 5, 5)

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

        self.metrics_console = QTextEdit()
        self.metrics_console.setReadOnly(True)
        self.metrics_console.setFixedHeight(280)

        self.metrics_console.setStyleSheet(
            """
            QTextEdit {
                background-color: transparent;
                color: #00FFCC;
                border: none;
                font-family: 'Consolas';
                margin: 50px
            }
        """
        )

        log_container_layout.addWidget(self.log_console, stretch=2)
        log_container_layout.addWidget(self.metrics_console, stretch=1)

        log_container.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
                border: none
            }
        """
        )

        log_container.setFixedHeight(300)
        log_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        log_container.setContentsMargins(10, 10, 10, 10)

        overlay_layout.addWidget(self.btn_play)
        overlay_layout.addStretch()
        overlay_layout.addWidget(
            log_container, alignment=Qt.AlignmentFlag.AlignBottom
        )
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        main_layout.addWidget(view)

        self.log_remove()

        return widget

    def draw_graph(self, graph: Graph) -> None:
        """
        Renders all nodes and links of the graph onto the QGraphicsScene.

        Args:
            graph (Graph): The graph to render.
        """
        if self.scene is None:
            return

        scene: QGraphicsScene = self.scene
        scene.clear()

        self.node_labels = {}
        self.link_labels = {}
        self.drone_list = {}
        self.animations = []

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
                pen_line = QPen(QColor("grey"))
                pen_line.setWidth(3)
                scene.addLine(
                    x1 * SCALE,
                    y1 * SCALE,
                    x2 * SCALE,
                    y2 * SCALE,
                    pen_line,
                )
            mid_x = (x1 + x2) / 2 * SCALE
            mid_y = (y1 + y2) / 2 * SCALE
            label = scene.addText(f"0/{link.max_drone}")
            label.setPos(mid_x, mid_y)
            self.link_labels[link.name] = (label, link.max_drone)

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

            text = scene.addText(f"{node.name}: 0/{node.max_drones}")
            text.setDefaultTextColor("white")
            text.setPos(x - OFFSET, y - OFFSET - 25)
            self.node_labels[node.name] = (text, node.max_drones)

        for node in graph.nodes.values():
            __draw_hub(node)

        rect = scene.itemsBoundingRect()

        padding = 120

        scene.setSceneRect(rect.adjusted(-padding, 0, padding, padding))

    def _draw_drone(self, position: tuple[int, int], id: int) -> None:
        """
        Creates and places a Drone sprite on the scene at the given position.

        Args:
            position (tuple[int, int]): The starting (x, y) tile coordinates.
            id (int): The drone identifier.
        """
        x, y = position
        self.drone_list[id] = Drone(
            x - OFFSET / 2, y - OFFSET / 2, NODE_SIZE / 2, NODE_SIZE / 2
        )

        self.scene.addItem(self.drone_list[id])

    def _animate_drone(self, turn_move: dict[int, tuple[int, int]]) -> None:
        """
        Animates drones smoothly to their new positions for the current turn.

        Args:
            turn_move (dict[int, tuple[int, int]]): Maps drone id to target
            (x, y) position.
        """
        for drone, drone_move in turn_move.items():
            x, y = drone_move
            animation = QPropertyAnimation(self.drone_list[drone], b"position")
            animation.setDuration(800)
            animation.setEndValue(
                QPointF(x * SCALE - OFFSET / 2, y * SCALE - OFFSET / 2)
            )
            animation.start()
            self.animations.append(animation)

    def log_move(self, tour: str, texte: str) -> None:
        """
        Appends a formatted turn log entry to the log console.

        Args:
            tour (str): The turn number as a string.
            texte (str): The movement description to display.
        """
        self.log_console.append("")
        self.log_console.append(
            f"<b style='color:white;'>[TOUR {tour}]</b> : {texte}"
        )

    def log_remove(self) -> None:
        """
        Clears the log console and resets it to the initial welcome message.
        """
        self.log_console.clear()
        for _ in range(7):
            self.log_console.append("\n")
        self.log_console.append(
            "Fly-In system initialized... Ready for takeoff."
        )

    def write_metrics(self) -> None:
        """Displays the stored simulation metrics in the metrics console."""
        self.remove_metrics()
        for title, metrics in self.metrics.items():
            self.metrics_console.append(f"{title}: {metrics}")

    def remove_metrics(self) -> None:
        """Clears the metrics console."""
        self.metrics_console.clear()

    def _scroll_log_to_bottom(self) -> None:
        """Scrolls the log console to the most recent entry."""
        sb = self.log_console.verticalScrollBar()
        sb.setValue(sb.maximum())
