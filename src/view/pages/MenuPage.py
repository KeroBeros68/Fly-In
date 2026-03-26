import logging
import tomllib
from typing import Any

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtGui import (
    QDesktopServices,
    QPixmap,
)
import os

from src.view.components.Button import Button
from src.view.components.Title import Title
from src.view.pages.Page import Page


logger = logging.getLogger("Fly-In")


class FileDropInput(QLineEdit):
    """
    A QLineEdit that accepts file drag-and-drop events and triggers a callback.
    """

    def __init__(self, on_file_selected: Any = None) -> None:
        """
        Initializes the file drop input with an optional selection callback.

        Args:
            on_file_selected (Any, optional): Callable invoked with the
            selected file path.
        """
        super().__init__()
        self.setAcceptDrops(True)
        self.on_file_selected = on_file_selected
        self.setPlaceholderText("Drag & drop a file or click Browse")

    def dragEnterEvent(self, event: Any) -> None:
        """
        Accepts drag enter events that contain file URLs.

        Args:
            event (Any): The Qt drag enter event.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: Any) -> None:
        """
        Handles file drop: sets the input text and triggers the callback.

        Args:
            event (Any): The Qt drop event containing file URLs.
        """
        files = event.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            self.setText(file_path)

            if self.on_file_selected:
                self.on_file_selected(file_path)


class MenuPage(Page):
    """
    The main menu page of the application.

    Provides file selection, simulation launch, GitHub link, and exit controls.

    Signals:
        file_selected (str): Emitted with the selected file path.
    """

    file_selected = Signal(str)

    def __init__(self) -> None:
        """Initializes the MenuPage."""
        super().__init__()

    def create_page(self, stack: QStackedWidget) -> QWidget:
        """
        Builds and returns the menu page widget.

        Args:
            stack (QStackedWidget): The page stack used for navigation.

        Returns:
            QWidget: The fully constructed menu page widget.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = Title("FLY-IN SIMULATOR", self.font_family)

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

        def __open_website() -> None:
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

        def __version_read() -> Any:
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

    def open_file(self, parent: QWidget, file_input: FileDropInput) -> None:
        """
        Opens a native file dialog and populates the file input on selection.

        Args:
            parent (QWidget): The parent widget for the dialog.
            file_input (FileDropInput): The input field to update with the
            selected path.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select flight file",
            "",
            "Flight Files (*.txt);;All Files (*)",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if file_path:
            file_input.setText(file_path)
