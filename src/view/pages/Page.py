import os

from PySide6.QtWidgets import (
    QWidget,
)
from PySide6.QtGui import (
    QFontDatabase,
)

from src.view.components.Button import Button


class Page(QWidget):
    """
    Abstract base class for application pages, providing shared font loading
    and button styling utilities.
    """

    def __init__(self) -> None:
        """Initializes the page and loads the application font."""
        super().__init__()
        self.font_family = self._load_fonts()

    def _load_fonts(self) -> str:
        """
        Loads the Orbitron font from the assets directory.

        Returns:
            str: The font family name if found, otherwise 'Arial'.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir, "..", "assets", "fonts", "Orbitron-Bold.ttf"
        )

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
        return "Arial"

    def set_btn_enabled(self, btn: Button,  enabled: bool) -> None:
        """
        Enables or disables a button and updates its stylesheet accordingly.

        Args:
            btn (Button): The button to update.
            enabled (bool): True to enable, False to disable.
        """
        btn.setEnabled(enabled)
        if enabled:
            btn.setStyleSheet(self._get_enabled_button_style())
        else:
            btn.setStyleSheet(self._get_disabled_button_style())

    def _get_disabled_button_style(self) -> str:
        """
        Returns the CSS stylesheet string for a disabled button.

        Returns:
            str: Qt stylesheet for a greyed-out button.
        """
        return """
            QPushButton {
                background-color: #333333;
                color: #777777;
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """

    def _get_enabled_button_style(self) -> str:
        """
        Returns the CSS stylesheet string for an enabled button.

        Returns:
            str: Qt stylesheet for an active, hoverable button.
        """
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
