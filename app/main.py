"""
C# Code Reviewer - Main Application Entry Point

This is the main entry point for the C# Code Reviewer application.
It initializes the PySide6 QApplication and creates the main window.

Features:
- Automatic Ollama server management (portable mode supported)
- High DPI scaling
- Dark theme stylesheet
- Graceful shutdown
"""

import sys
import os
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ui.main_window import MainWindow
from app.services.ollama_manager import OllamaManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def get_portable_ollama_path() -> Path | None:
    """
    Get path to portable Ollama executable if it exists

    Checks:
    1. ./ollama_portable/ollama.exe (Windows)
    2. ./ollama_portable/ollama (macOS/Linux)
    3. ../ollama_portable/ollama.exe (if running from app/)
    """
    # Get application directory
    if getattr(sys, 'frozen', False):
        # Running as EXE (PyInstaller)
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent.parent

    # Possible portable Ollama paths
    possible_paths = [
        app_dir / "ollama_portable" / "ollama.exe",  # Windows
        app_dir / "ollama_portable" / "ollama",      # macOS/Linux
    ]

    for path in possible_paths:
        if path.exists() and path.is_file():
            logger.info(f"Found portable Ollama: {path}")
            return path

    logger.info("No portable Ollama found, will try system Ollama")
    return None


def show_ollama_startup_message(app: QApplication):
    """Show startup message while Ollama initializes"""
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Starting Ollama...")
    msg_box.setText("Initializing Ollama LLM server...")
    msg_box.setInformativeText(
        "This may take 5-10 seconds on first launch.\n"
        "Please wait..."
    )
    msg_box.setStandardButtons(QMessageBox.StandardButton.NoButton)
    msg_box.setModal(True)

    # Show non-blocking
    msg_box.show()
    app.processEvents()

    return msg_box


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

    logger.info("=" * 80)
    logger.info("C# Code Reviewer starting...")
    logger.info("=" * 80)

    # Initialize Ollama manager
    portable_path = get_portable_ollama_path()
    ollama_manager = OllamaManager(
        ollama_host="http://localhost:11434",
        portable_path=portable_path,
        startup_timeout=30,
        model_name="phi3:mini"
    )

    # Show startup message
    startup_msg = show_ollama_startup_message(app)

    # Start Ollama
    logger.info("Starting Ollama server...")
    ollama_started = ollama_manager.start()

    # Close startup message
    startup_msg.close()
    startup_msg.deleteLater()  # Explicitly delete the dialog
    app.processEvents()  # Force UI update to close the dialog

    # Give Qt time to cleanup
    QApplication.processEvents()

    if not ollama_started:
        logger.error("Failed to start Ollama")
        QMessageBox.critical(
            None,
            "Ollama Startup Failed",
            "Failed to start Ollama LLM server.\n\n"
            "Possible solutions:\n"
            "1. Wait 10-20 seconds and try again\n"
            "2. Start Ollama manually: ollama serve\n"
            "3. Check logs/app.log for details\n\n"
            "The application will continue, but AI analysis will not work\n"
            "until Ollama is running."
        )
        logger.warning("Application starting without Ollama")
    else:
        logger.info("Ollama started successfully")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Register cleanup on exit
    app.aboutToQuit.connect(lambda: cleanup(ollama_manager))

    # Start event loop
    exit_code = app.exec()

    logger.info("Application shutting down...")
    sys.exit(exit_code)


def cleanup(ollama_manager: OllamaManager):
    """Cleanup on application exit"""
    logger.info("Cleaning up...")
    ollama_manager.stop()
    logger.info("Cleanup complete")


if __name__ == "__main__":
    main()
