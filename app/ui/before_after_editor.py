"""
Before/After Split Code Editor

This module provides a split-view code editor with Before (input) and After (output) panels.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPlainTextEdit, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QTextCursor


class CodeEditor(QPlainTextEdit):
    """Enhanced QPlainTextEdit for code editing."""

    def __init__(self, parent=None, read_only=False):
        super().__init__(parent)

        # Set monospace font
        font = QFont("Monaco, Consolas, Courier New", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        # Configure editor
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(40)  # 4 spaces
        self.setReadOnly(read_only)

        # Placeholder text
        if not read_only:
            self.setPlaceholderText("Paste your C# code here...")


class EditorPanel(QWidget):
    """Single editor panel with label and copy button."""

    copy_clicked = Signal()  # Signal emitted when copy button is clicked

    def __init__(self, title: str, read_only: bool = False, parent=None):
        super().__init__(parent)

        self.title = title
        self.read_only = read_only

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Header with title and copy button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)

        # Title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Copy button
        self.copy_button = QPushButton("📋 Copy")
        self.copy_button.setFixedWidth(80)
        self.copy_button.clicked.connect(self.copy_clicked)
        header_layout.addWidget(self.copy_button)

        layout.addLayout(header_layout)

        # Editor
        self.editor = CodeEditor(read_only=read_only)
        layout.addWidget(self.editor)

    def get_text(self) -> str:
        """Get editor text content."""
        return self.editor.toPlainText()

    def set_text(self, text: str):
        """Set editor text content."""
        self.editor.setPlainText(text)

    def clear(self):
        """Clear editor content."""
        self.editor.clear()

    def copy_to_clipboard(self):
        """Copy editor content to clipboard."""
        self.editor.selectAll()
        self.editor.copy()
        # Clear selection
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)


class BeforeAfterEditor(QWidget):
    """Split-view code editor with Before and After panels."""

    # Signals
    before_text_changed = Signal(str)  # Emitted when before text changes
    after_text_changed = Signal(str)   # Emitted when after text changes

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Before panel (editable)
        self.before_panel = EditorPanel("Before (Original Code)", read_only=False)
        self.before_panel.copy_clicked.connect(self._on_before_copy)
        self.before_panel.editor.textChanged.connect(self._on_before_text_changed)

        # After panel (read-only)
        self.after_panel = EditorPanel("After (Improved Code)", read_only=True)
        self.after_panel.copy_clicked.connect(self._on_after_copy)
        self.after_panel.editor.textChanged.connect(self._on_after_text_changed)

        # Add panels to splitter
        self.splitter.addWidget(self.before_panel)
        self.splitter.addWidget(self.after_panel)

        # Set equal split (50:50)
        self.splitter.setSizes([1000, 1000])

        # Add splitter to layout
        layout.addWidget(self.splitter)

    def get_before_text(self) -> str:
        """Get text from Before editor."""
        return self.before_panel.get_text()

    def get_after_text(self) -> str:
        """Get text from After editor."""
        return self.after_panel.get_text()

    def set_before_text(self, text: str):
        """Set text in Before editor."""
        self.before_panel.set_text(text)

    def set_after_text(self, text: str):
        """Set text in After editor."""
        self.after_panel.set_text(text)

    def clear_before(self):
        """Clear Before editor."""
        self.before_panel.clear()

    def clear_after(self):
        """Clear After editor."""
        self.after_panel.clear()

    def clear_all(self):
        """Clear both editors."""
        self.clear_before()
        self.clear_after()

    def _on_before_copy(self):
        """Handle Before copy button click."""
        self.before_panel.copy_to_clipboard()

    def _on_after_copy(self):
        """Handle After copy button click."""
        self.after_panel.copy_to_clipboard()

    def _on_before_text_changed(self):
        """Handle Before text changed."""
        text = self.get_before_text()
        self.before_text_changed.emit(text)

    def _on_after_text_changed(self):
        """Handle After text changed."""
        text = self.get_after_text()
        self.after_text_changed.emit(text)


# Test the editor
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Create editor
    editor = BeforeAfterEditor()
    editor.setWindowTitle("Before/After Code Editor Test")
    editor.resize(1200, 600)

    # Set sample text
    before_code = """using System;

public class Example
{
    public void ProcessData(string data)
    {
        var result = data.ToUpper();
        Console.WriteLine(result);
    }
}"""

    after_code = """using System;

public class Example
{
    public void ProcessData(string data)
    {
        if (string.IsNullOrEmpty(data))
            throw new ArgumentNullException(nameof(data));

        var result = data.ToUpper();
        Console.WriteLine(result);
    }
}"""

    editor.set_before_text(before_code)
    editor.set_after_text(after_code)

    editor.show()

    sys.exit(app.exec())
