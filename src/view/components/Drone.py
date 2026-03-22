from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsObject
from PySide6.QtCore import Property, QPointF
from PySide6.QtGui import (
    QBrush,
    QColor,
)


class Drone(QGraphicsObject):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.rect_item = QGraphicsRectItem(0, 0, w, h, self)
        self.rect_item.setBrush(QBrush(QColor("blue")))
        self.setPos(x, y)

    def _get_pos(self):
        return self.pos()  # appel méthode Qt

    def _set_pos(self, value: QPointF):
        self.setPos(value)

    # Nom "position" pour éviter le conflit avec QGraphicsItem.pos
    position = Property(QPointF, _get_pos, _set_pos)

    def boundingRect(self):
        return self.rect_item.boundingRect()

    def paint(self, painter, option, widget=None):
        pass  # QGraphicsRectItem enfant se peint lui-même
