from typing import Any

from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsObject
from PySide6.QtCore import Property, QPointF, QRectF
from PySide6.QtGui import (
    QBrush,
    QColor,
)


class Drone(QGraphicsObject):
    """
    A QGraphicsObject representing a drone sprite on the simulation scene.

    Supports property-based animation via the `position` Qt property.
    """

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        """
        Initializes the Drone at the given position with the given dimensions.

        Args:
            x (float): Initial x position on the scene.
            y (float): Initial y position on the scene.
            w (float): Width of the drone rectangle.
            h (float): Height of the drone rectangle.
        """
        super().__init__()
        self.rect_item = QGraphicsRectItem(0, 0, w, h, self)
        self.rect_item.setBrush(QBrush(QColor("blue")))
        self.setPos(x, y)

    def _get_pos(self) -> QPointF:
        """Returns the current scene position of the drone."""
        return self.pos()

    def _set_pos(self, value: QPointF) -> None:
        """
        Sets the scene position of the drone.

        Args:
            value (QPointF): The new position.
        """
        self.setPos(value)

    position = Property(QPointF, _get_pos, _set_pos)

    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rectangle of the drone for collision/rendering.

        Returns:
            QRectF: The bounding rectangle delegated to the inner rect item.
        """
        return self.rect_item.boundingRect()

    def paint(self, painter: Any, option: Any, widget: Any = None) -> None:
        """
        No-op paint method; rendering is handled by the child
        QGraphicsRectItem.

        Args:
            painter (Any): The QPainter instance (unused).
            option (Any): Style options (unused).
            widget (Any, optional): The widget being painted on (unused).
        """
        pass
