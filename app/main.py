"""
C# Code Reviewer - Main Application Entry Point

This is the main entry point for the C# Code Reviewer application.
It initializes the PySide6 QApplication and creates the main window.
"""

import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ui.main_window import MainWindow


def main():
    """Main application entry point."""

    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create the application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("C# Code Reviewer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Code Review Team")

    # Load stylesheet
    stylesheet_path = Path(__file__).parent.parent / "resources" / "styles" / "dark_theme.qss"
    if stylesheet_path.exists():
        with open(stylesheet_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
