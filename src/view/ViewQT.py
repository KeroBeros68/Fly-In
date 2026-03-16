from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor

from src.graph.Graph import Graph
from src.graph.node import Node


class ViewQT(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Fly In")

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

    def draw_graph(self, graph: Graph) -> None:
        self.scene.clear()  # On nettoie avant de redessiner

        scale: int = 150
        node_size: int = 40
        offset: int = node_size // 2

        # Create a dictionary to quickly find hub positions for connections
        node_positions = {node.name: node.pos for node in graph.nodes}

        # Dessiner les connexions d'abord pour qu'elles soient sous les hubs
        pen_line = QPen(Qt.GlobalColor.black)
        pen_line.setWidth(2)
        for link in graph.links.values():
            name = link.name.split("-")
            if name[0] in node_positions and name[1] in node_positions:
                x1, y1 = node_positions[name[0]]
                x2, y2 = node_positions[name[1]]
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

            # On crée un cercle centré sur le point
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

            # Ajouter le nom du hub au-dessus
            text = self.scene.addText(node.name)
            text.setPos(x - offset, y - offset - 25)

        # Dessiner les Hubs
        for node in graph.nodes:
            __draw_hub(node)

        # Ajuster la vue pour voir tous les éléments
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
