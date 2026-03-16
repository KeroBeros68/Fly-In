import logging
import tomllib

from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QLabel,
    QPushButton,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import QPropertyAnimation, QUrl, Qt
from PySide6.QtGui import (
    QColor,
    QDesktopServices,
    QFont,
    QPixmap,
    QFontDatabase,
)
import os


logger = logging.getLogger("Fly-In")


class MenuPage:
    def __init__(self) -> None:
        self.font_family = self._load_fonts()

    def _load_fonts(self):
        # On charge la police Orbitron depuis les assets
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

        # 1. TITRE avec Orbitron
        title_font = QFont(self.font_family, 32, QFont.Weight.Bold)

        title = QLabel("FLY-IN SIMULATOR")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            color: #00FFCC;
            margin-bottom: 20px;
        """)

        # Effet glow
        self.glow = QGraphicsDropShadowEffect()
        self.glow.setColor(QColor("#00FFCC"))
        self.glow.setOffset(0, 0)
        self.glow.setBlurRadius(20)

        title.setGraphicsEffect(self.glow)

        # Animation du glow
        self.anim = QPropertyAnimation(self.glow, b"blurRadius")
        self.anim.setStartValue(40)
        self.anim.setEndValue(90)
        self.anim.setDuration(3200)
        self.anim.setLoopCount(-1)  # boucle infinie
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

        # 3. BOUTON
        btn = QPushButton("LANCER LA SIMULATION")
        btn.setFont(QFont(self.font_family, 12))
        btn.setFixedWidth(300)
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style pour coller au thème
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: 2px solid #00FFCC;
                color: #00FFCC;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00FFCC;
                color: #121212;
            }
        """
        )

        btn.clicked.connect(lambda: stack.setCurrentIndex(1))

        btn2 = QPushButton("VOIR MON GIT")
        btn2.setFont(QFont(self.font_family, 12))
        btn2.setFixedWidth(300)
        btn2.setFixedHeight(50)
        btn2.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style pour coller au thème
        btn2.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: 2px solid #f9c414;
                color: #f9c414;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f9c414;
                color: #121212;
            }
        """
        )

        def __open_website():
            # Remplace par l'URL de ton choix (ton repo GitHub par exemple)
            url = QUrl("https://github.com/keroberos68")
            QDesktopServices.openUrl(url)

        btn2.clicked.connect(__open_website)

        btn3 = QPushButton("EXIT")
        btn3.setFont(QFont(self.font_family, 12))
        btn3.setFixedWidth(300)
        btn3.setFixedHeight(50)
        btn3.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style pour coller au thème
        btn3.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: 2px solid #be123c;
                color: #be123c;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #be123c;
                color: #121212;
            }
        """
        )

        def __exit_btn() -> None:
            logger.info("Exit program")
            widget.window().close()

        btn3.clicked.connect(__exit_btn)

        def __version_read() -> str:
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
            return data["project"]["version"]

        ma_legende = QLabel(f"Version: {__version_read()}")

        # Style (gras, couleur, taille)
        ma_legende.setStyleSheet(
            "font-weight: bold; color: #00FFCC; font-size: 16px"
        )

        ma_legende2 = QLabel("Copyright -> @Moi-meme")

        # Style (gras, couleur, taille)
        ma_legende2.setStyleSheet(
            "font-weight: bold; color: #00FFCC; font-size: 16px"
        )

        # Organisation
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(label_logo)
        layout.addSpacing(50)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(btn2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(btn3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(150)
        layout.addWidget(ma_legende, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ma_legende2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        return widget
