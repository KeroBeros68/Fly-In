import logging
import tomllib

from PySide6.QtWidgets import (
    QFileDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
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
    QFontDatabase,
)
import os


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


class MenuPage(QWidget):
    file_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.font_family = self._load_fonts()

    def _load_fonts(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir, "..", "assets", "fonts", "Orbitron-Bold.ttf"
        )

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
        return "Arial"  # Fallback si le fichier est manquant

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

        # 2. LOGO
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
        button_file = self.__new_button(
            "Browse", 150, 50, "#00FFCC", "#121212"
        )

        button_file.clicked.connect(lambda: self.open_file(widget, file_input))
        file_input.textChanged.connect(
            lambda path: self.file_selected.emit(path)
        )

        file_layout = QHBoxLayout()
        file_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_layout.addWidget(file_input)
        file_layout.addWidget(button_file)

        btn_start = self.__new_button(
            "LANCER LA SIMULATION", 300, 50, "#00FFCC", "#121212"
        )
        btn_start.clicked.connect(lambda: stack.setCurrentIndex(1))

        def __open_website():
            url = QUrl("https://github.com/keroberos68")
            QDesktopServices.openUrl(url)

        btn_git = self.__new_button(
            "VERS MON GIT", 300, 50, "#f9c414", "#121212"
        )
        btn_git.clicked.connect(__open_website)

        def __exit_btn() -> None:
            logger.info("Exit program")
            widget.window().close()

        btn_exit = self.__new_button("EXIT", 300, 50, "#be123c", "#121212")
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

        # Organisation
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(label_logo)
        layout.addSpacing(50)
        layout.addLayout(file_layout)
        layout.addSpacing(10)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
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
        )
        if file_path:
            file_input.setText(file_path)

    def __new_button(
        self, name: str, width: int, height: int, color: str, hover_color: str
    ) -> QPushButton:
        btn = QPushButton(name)
        btn.setFont(QFont(self.font_family, 12))
        btn.setFixedWidth(width)
        btn.setFixedHeight(height)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style pour coller au thème
        btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {color};
                color: {color};
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color};
                color: {hover_color};
            }}
            """
        )

        return btn
