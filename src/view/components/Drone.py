from typing import Any

from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsObject
from PySide6.QtCore import Property, QPointF, QRectF
from PySide6.QtGui import (
    QBrush,
    QColor,
)


class Drone(QGraphicsObject):
    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        super().__init__()
        self.rect_item = QGraphicsRectItem(0, 0, w, h, self)
        self.rect_item.setBrush(QBrush(QColor("blue")))
        self.setPos(x, y)

    def _get_pos(self) -> QPointF:
        return self.pos()

    def _set_pos(self, value: QPointF) -> None:
        self.setPos(value)

    position = Property(QPointF, _get_pos, _set_pos)

    def boundingRect(self) -> QRectF:
        return self.rect_item.boundingRect()

    def paint(self, painter: Any, option: Any, widget: Any = None) -> None:
        pass
