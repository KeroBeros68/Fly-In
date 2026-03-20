import logging
import tomllib

from PySide6.QtWidgets import (
    QFileDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import QPropertyAnimation, QUrl, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QDesktopServices,
    QFont,
    QPixmap,
)
import os

from src.view.components.Button import Button
from src.view.pages.Page import Page


logger = logging.getLogger("Fly-In")


class FileDropInput(QLineEdit):
    def __init__(self, on_file_selected=None):
        super().__init__()
        self.setAcceptDrops(True)
        self.on_file_selected = on_file_selected
        self.setPlaceholderText("Drag & drop a file or click Browse")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = event.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            self.setText(file_path)

            if self.on_file_selected:
                self.on_file_selected(file_path)


class MenuPage(Page):
    file_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()

    def _get_disabled_button_style(self):
        return """
            QPushButton {
                background-color: #333333;
                color: #777777;
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """

    def _get_enabled_button_style(self):
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

    def set_start_enabled(self, enabled: bool):
        self.btn_start.setEnabled(enabled)
        if enabled:
            self.btn_start.setStyleSheet(self._get_enabled_button_style())
        else:
            self.btn_start.setStyleSheet(self._get_disabled_button_style())

    def create_page(self, stack: QStackedWidget) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = QFont(self.font_family, 32, QFont.Weight.Bold)

        title = QLabel("FLY-IN SIMULATOR")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet(
            """
            color: #00FFCC;
            margin-bottom: 20px;
        """
        )

        self.glow = QGraphicsDropShadowEffect()
        self.glow.setColor(QColor("#00FFCC"))
        self.glow.setOffset(0, 0)
        self.glow.setBlurRadius(20)

        title.setGraphicsEffect(self.glow)

        self.anim = QPropertyAnimation(self.glow, b"blurRadius")
        self.anim.setStartValue(40)
        self.anim.setEndValue(90)
        self.anim.setDuration(3200)
        self.anim.setLoopCount(-1)
        self.anim.start()

        label_logo = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(
            current_dir, "..", "assets", "drone_router_icon.png"
        )

        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            label_logo.setPixmap(
                pixmap.scaled(
                    350,
                    350,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        file_input = FileDropInput(
            on_file_selected=lambda path: self.file_selected.emit(path)
        )
        file_input.setFixedWidth(500)
        file_input.setPlaceholderText("Select a flight file (.txt)")
        button_file = Button(
            "Browse", 150, 50, "#00FFCC", "#121212", self.font_family
        )

        button_file.clicked.connect(lambda: self.open_file(widget, file_input))
        file_input.textChanged.connect(
            lambda path: self.file_selected.emit(path)
        )

        file_layout = QHBoxLayout()
        file_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_layout.addWidget(file_input)
        file_layout.addWidget(button_file)

        self.btn_start = Button(
            "LAUNCH SIMULATION",
            300,
            50,
            "#00FFCC",
            "#121212",
            self.font_family,
        )
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet(self._get_disabled_button_style())

        self.btn_start.clicked.connect(lambda: stack.setCurrentIndex(1))

        def __open_website():
            url = QUrl("https://github.com/keroberos68")
            QDesktopServices.openUrl(url)

        btn_git = Button(
            "TO GITHUB", 300, 50, "#f9c414", "#121212", self.font_family
        )
        btn_git.clicked.connect(__open_website)

        def __exit_btn() -> None:
            logger.info("Exit program")
            widget.window().close()

        btn_exit = Button(
            "EXIT", 300, 50, "#be123c", "#121212", self.font_family
        )
        btn_exit.clicked.connect(__exit_btn)

        def __version_read() -> str:
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
            return data["project"]["version"]

        label_version = QLabel(f"Version: {__version_read()}")
        label_version.setStyleSheet(
            "font-weight: bold; color: #00FFCC; font-size: 16px"
        )

        label_copyright = QLabel("Copyright -> @KeroBeros68")
        label_copyright.setStyleSheet(
            "font-weight: bold; color: #00FFCC; font-size: 16px"
        )

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(label_logo)
        layout.addSpacing(50)
        layout.addLayout(file_layout)
        layout.addSpacing(10)
        layout.addWidget(
            self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addSpacing(10)
        layout.addWidget(btn_git, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(btn_exit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(100)
        layout.addWidget(label_version, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(
            label_copyright, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addStretch()

        return widget

    def open_file(self, parent: QWidget, file_input: FileDropInput):
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select flight file",
            "",
            "Flight Files (*.txt);;All Files (*)",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if file_path:
            file_input.setText(file_path)
