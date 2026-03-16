from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor

from src.parsing.models import HubModel, MapModel


class ViewQT(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Fly In")

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

    def draw_graph(self, map_model: "MapModel") -> None:
        self.scene.clear()  # On nettoie avant de redessiner

        scale: int = 150
        hub_size: int = 40
        offset: int = hub_size // 2

        # Create a dictionary to quickly find hub positions for connections
        hub_positions = {hub.name: hub.pos for hub in map_model.hubs}
        hub_positions[map_model.end_hub.name] = map_model.end_hub.pos
        hub_positions[map_model.start_hub.name] = map_model.start_hub.pos

        # Dessiner les connexions d'abord pour qu'elles soient sous les hubs
        pen_line = QPen(Qt.GlobalColor.black)
        pen_line.setWidth(2)
        for conn in map_model.connections:
            if conn.zone1 in hub_positions and conn.zone2 in hub_positions:
                x1, y1 = hub_positions[conn.zone1]
                x2, y2 = hub_positions[conn.zone2]
                self.scene.addLine(
                    x1 * scale,
                    y1 * scale,
                    x2 * scale,
                    y2 * scale,
                    pen_line,
                )

        def __draw_hub(hub: HubModel):
            orig_x, orig_y = hub.pos
            x = orig_x * scale
            y = orig_y * scale

            # On crée un cercle centré sur le point
            hub_color = (
                hub.color if hasattr(hub, "color") and hub.color else "cyan"
            )
            self.scene.addEllipse(
                x - offset,
                y - offset,
                hub_size,
                hub_size,
                QPen(Qt.GlobalColor.black),
                QBrush(QColor(hub_color)),
            )

            # Ajouter le nom du hub au-dessus
            text = self.scene.addText(hub.name)
            text.setPos(x - offset, y - offset - 25)

        # Dessiner les Hubs
        for hub in map_model.hubs:
            __draw_hub(hub)

        __draw_hub(map_model.end_hub)

        __draw_hub(map_model.start_hub)

        # Ajuster la vue pour voir tous les éléments
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
