from PySide6 import QtCore, QtWidgets


class ViewQT(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fly In")

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel(
            "Hello World", alignment=QtCore.Qt.AlignCenter
        )

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
