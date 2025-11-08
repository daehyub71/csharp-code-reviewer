"""
Main Window for C# Code Reviewer

This module provides the main application window with menu bar, toolbar, and status bar.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QPushButton,
    QLabel, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeySequence, QIcon

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.ui.before_after_editor import BeforeAfterEditor
from app.core.ollama_client import OllamaClient, OllamaClientError


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("C# Code Reviewer - Phi-3-mini")
        self.resize(1400, 800)

        # Initialize Ollama client
        self.ollama_client = None
        self.ollama_status = "Disconnected"

        # Setup UI
        self._setup_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()

        # Test Ollama connection
        QTimer.singleShot(1000, self._test_ollama_connection)

    def _setup_ui(self):
        """Setup main UI layout."""

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create before/after editor
        self.editor = BeforeAfterEditor()
        main_layout.addWidget(self.editor)

    def _create_menu_bar(self):
        """Create menu bar."""

        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # New action
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip("Clear all editors")
        new_action.triggered.connect(self._on_new)
        file_menu.addAction(new_action)

        # Open action
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open C# file")
        open_action.triggered.connect(self._on_open)
        file_menu.addAction(open_action)

        # Save action
        save_action = QAction("&Save Report...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("Save code review report")
        save_action.triggered.connect(self._on_save)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        # Copy before action
        copy_before_action = QAction("Copy &Before", self)
        copy_before_action.setShortcut("Ctrl+Shift+C")
        copy_before_action.setStatusTip("Copy before code")
        copy_before_action.triggered.connect(self._on_copy_before)
        edit_menu.addAction(copy_before_action)

        # Copy after action
        copy_after_action = QAction("Copy &After", self)
        copy_after_action.setShortcut("Ctrl+Shift+V")
        copy_after_action.setStatusTip("Copy after code")
        copy_after_action.triggered.connect(self._on_copy_after)
        edit_menu.addAction(copy_after_action)

        edit_menu.addSeparator()

        # Clear action
        clear_action = QAction("C&lear All", self)
        clear_action.setShortcut("Ctrl+Shift+X")
        clear_action.setStatusTip("Clear all editors")
        clear_action.triggered.connect(self._on_clear)
        edit_menu.addAction(clear_action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        # Analyze action
        analyze_action = QAction("&Analyze Code", self)
        analyze_action.setShortcut("F5")
        analyze_action.setStatusTip("Analyze C# code with AI")
        analyze_action.triggered.connect(self._on_analyze)
        tools_menu.addAction(analyze_action)

        tools_menu.addSeparator()

        # Test connection action
        test_connection_action = QAction("Test &Ollama Connection", self)
        test_connection_action.setStatusTip("Test connection to Ollama server")
        test_connection_action.triggered.connect(self._test_ollama_connection)
        tools_menu.addAction(test_connection_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        # About action
        about_action = QAction("&About", self)
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_toolbar(self):
        """Create toolbar."""

        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Analyze button
        self.analyze_button = QPushButton("▶ Analyze Code")
        self.analyze_button.setFixedHeight(32)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5a5d;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
        """)
        self.analyze_button.clicked.connect(self._on_analyze)
        toolbar.addWidget(self.analyze_button)

        toolbar.addSeparator()

        # Clear button
        clear_button = QPushButton("🗑 Clear")
        clear_button.setFixedHeight(32)
        clear_button.clicked.connect(self._on_clear)
        toolbar.addWidget(clear_button)

        toolbar.addSeparator()

        # Settings button (placeholder)
        settings_button = QPushButton("⚙ Settings")
        settings_button.setFixedHeight(32)
        settings_button.setEnabled(False)  # Not implemented yet
        toolbar.addWidget(settings_button)

        # Add stretch to push buttons to the left
        toolbar.addWidget(QWidget())  # Spacer

    def _create_status_bar(self):
        """Create status bar."""

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # Ollama status label
        self.ollama_status_label = QLabel("Ollama: Checking...")
        self.ollama_status_label.setStyleSheet("color: #999;")
        statusbar.addPermanentWidget(self.ollama_status_label)

        # Model info label
        self.model_info_label = QLabel("")
        statusbar.addPermanentWidget(self.model_info_label)

        # Memory label (placeholder)
        self.memory_label = QLabel("")
        statusbar.addPermanentWidget(self.memory_label)

        # Set initial status
        statusbar.showMessage("Ready", 5000)

    def _update_ollama_status(self, status: str, color: str = "#999"):
        """Update Ollama status display."""
        self.ollama_status = status
        self.ollama_status_label.setText(f"Ollama: {status}")
        self.ollama_status_label.setStyleSheet(f"color: {color};")

    def _test_ollama_connection(self):
        """Test connection to Ollama server."""

        self._update_ollama_status("Testing...", "#FFA500")

        try:
            # Create client if not exists
            if self.ollama_client is None:
                self.ollama_client = OllamaClient(model_name="phi3:mini")

            # Test connection
            self.ollama_client.test_connection()

            # Get model info
            model_info = self.ollama_client.get_model_info()
            model_name = model_info.get('name', 'Unknown')
            parameter_size = model_info.get('details', {}).get('parameter_size', 'N/A')

            # Update status
            self._update_ollama_status("Connected ✓", "#00FF00")
            self.model_info_label.setText(f"Model: {model_name} ({parameter_size})")
            self.analyze_button.setEnabled(True)

            self.statusBar().showMessage("Ollama connection successful", 5000)

        except OllamaClientError as e:
            self._update_ollama_status("Disconnected ✗", "#FF0000")
            self.model_info_label.setText("")
            self.analyze_button.setEnabled(False)

            error_msg = str(e)
            self.statusBar().showMessage(f"Ollama connection failed: {error_msg}", 10000)

            QMessageBox.warning(
                self,
                "Ollama Connection Failed",
                f"Failed to connect to Ollama server.\n\n"
                f"Error: {error_msg}\n\n"
                f"Please ensure:\n"
                f"1. Ollama is installed\n"
                f"2. Ollama server is running (ollama serve)\n"
                f"3. phi3:mini model is downloaded (ollama pull phi3:mini)"
            )

    # Menu action handlers
    def _on_new(self):
        """Handle New action."""
        self.editor.clear_all()
        self.statusBar().showMessage("Editors cleared", 3000)

    def _on_open(self):
        """Handle Open action."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open C# File",
            "",
            "C# Files (*.cs);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.editor.set_before_text(content)
                    self.statusBar().showMessage(f"Loaded: {file_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")

    def _on_save(self):
        """Handle Save action."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            "code_review_report.md",
            "Markdown Files (*.md);;All Files (*)"
        )

        if file_path:
            try:
                # For now, just save the after code
                # In the future, this will save a full report
                content = self.editor.get_after_text()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    self.statusBar().showMessage(f"Saved: {file_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    def _on_copy_before(self):
        """Handle Copy Before action."""
        self.editor.before_panel.copy_to_clipboard()
        self.statusBar().showMessage("Before code copied to clipboard", 3000)

    def _on_copy_after(self):
        """Handle Copy After action."""
        self.editor.after_panel.copy_to_clipboard()
        self.statusBar().showMessage("After code copied to clipboard", 3000)

    def _on_clear(self):
        """Handle Clear action."""
        self.editor.clear_all()
        self.statusBar().showMessage("All editors cleared", 3000)

    def _on_analyze(self):
        """Handle Analyze action."""

        # Get before code
        before_code = self.editor.get_before_text().strip()

        if not before_code:
            QMessageBox.warning(self, "No Code", "Please paste C# code in the Before editor.")
            return

        if self.ollama_client is None:
            QMessageBox.warning(self, "Not Connected", "Ollama client not connected. Please check connection.")
            return

        # Disable analyze button during analysis
        self.analyze_button.setEnabled(False)
        self.statusBar().showMessage("Analyzing code...", 0)

        # For now, just show a placeholder message
        # TODO: Implement actual code analysis in Day 5
        placeholder_after = """// Analysis not yet implemented
// This will be completed in Day 5 (Prompt Builder implementation)

// For now, showing placeholder response
public class ImprovedExample
{
    // TODO: AI-generated improved code will appear here
}"""

        self.editor.set_after_text(placeholder_after)

        # Re-enable analyze button
        self.analyze_button.setEnabled(True)
        self.statusBar().showMessage("Analysis complete (placeholder - full implementation in Day 5)", 5000)

        QMessageBox.information(
            self,
            "Analysis Placeholder",
            "Code analysis is not yet implemented.\n\n"
            "This will be completed in Day 5 when we implement the Prompt Builder.\n\n"
            "For now, a placeholder response is shown in the After editor."
        )

    def _on_about(self):
        """Handle About action."""
        QMessageBox.about(
            self,
            "About C# Code Reviewer",
            "<h3>C# Code Reviewer v1.0.0</h3>"
            "<p>AI-powered C# code review tool using Phi-3-mini LLM.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>6 code review categories</li>"
            "<li>Automated code improvement suggestions</li>"
            "<li>100% offline operation</li>"
            "</ul>"
            "<p><b>Technology:</b></p>"
            "<ul>"
            "<li>LLM: Phi-3-mini (3.8B parameters)</li>"
            "<li>Framework: PySide6 (Qt6)</li>"
            "<li>Backend: Python 3.13</li>"
            "</ul>"
            "<p>© 2025 Code Review Team</p>"
        )


# Test the main window
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
