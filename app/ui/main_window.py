"""
Main Window for C# Code Reviewer

This module provides the main application window with menu bar, toolbar, and status bar.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QPushButton,
    QLabel, QMessageBox, QFileDialog, QProgressDialog
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeySequence, QIcon

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.ui.before_after_editor import BeforeAfterEditor
from app.core.ollama_client import OllamaClient, OllamaClientError
from app.core.prompt_builder import PromptBuilder, ReviewCategory, OutputFormat
from app.core.report_generator import ReportGenerator


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

        # Initialize Prompt Builder
        self.prompt_builder = PromptBuilder()

        # Initialize Report Generator
        self.report_generator = ReportGenerator()

        # Store last analysis results
        self.last_analysis = {
            'original_code': '',
            'improved_code': '',
            'categories': []
        }

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
        save_action = QAction("리포트 저장(&S)...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("코드 리뷰 리포트를 Markdown으로 저장")
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

        # 분석 결과가 있는지 확인
        if not self.last_analysis.get('improved_code'):
            QMessageBox.warning(
                self,
                "저장 실패",
                "저장할 분석 결과가 없습니다.\n\n"
                "먼저 코드 분석을 실행해주세요."
            )
            return

        # 자동 파일명 생성
        default_filename = self.report_generator.generate_filename()

        # 저장 위치 선택
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "리포트 저장",
            default_filename,
            "Markdown Files (*.md);;All Files (*)"
        )

        if file_path:
            try:
                # 프로그레스 다이얼로그
                progress = QProgressDialog("리포트 생성 중...", None, 0, 100, self)
                progress.setWindowTitle("리포트 저장")
                progress.setWindowModality(Qt.WindowModality.WindowModal)
                progress.setMinimumDuration(0)
                progress.setValue(0)

                # 리포트 생성
                progress.setLabelText("Markdown 리포트 생성 중...")
                progress.setValue(30)

                report = self.report_generator.generate_report(
                    original_code=self.last_analysis['original_code'],
                    improved_code=self.last_analysis['improved_code'],
                    categories=self.last_analysis['categories'],
                    model_name="phi3:mini"
                )

                # 파일 저장
                progress.setLabelText("파일 저장 중...")
                progress.setValue(70)

                self.report_generator.save_report(report, file_path)

                progress.setValue(100)
                progress.close()

                # 성공 메시지
                self.statusBar().showMessage(f"✅ 리포트 저장 완료: {file_path}", 5000)

                QMessageBox.information(
                    self,
                    "저장 완료",
                    f"리포트가 성공적으로 저장되었습니다!\n\n"
                    f"저장 위치: {file_path}\n\n"
                    f"Markdown 뷰어로 확인하실 수 있습니다."
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "저장 실패",
                    f"리포트 저장 중 오류가 발생했습니다.\n\n"
                    f"오류: {str(e)}"
                )

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

        # 분석할 코드 가져오기
        before_code = self.editor.get_before_text().strip()

        if not before_code:
            QMessageBox.warning(self, "코드 없음", "Before 에디터에 C# 코드를 붙여넣어주세요.")
            return

        if self.ollama_client is None:
            QMessageBox.warning(self, "연결 안 됨", "Ollama 클라이언트가 연결되지 않았습니다. 연결을 확인해주세요.")
            return

        # 프로그레스 다이얼로그 생성
        progress = QProgressDialog("코드 분석 중...", "취소", 0, 100, self)
        progress.setWindowTitle("AI 코드 분석")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        # 분석 중 버튼 비활성화
        self.analyze_button.setEnabled(False)

        try:
            # Step 1: 프롬프트 생성 (10%)
            progress.setLabelText("프롬프트 생성 중...")
            progress.setValue(10)

            # 모든 리뷰 카테고리 활성화
            categories = [
                ReviewCategory.NULL_REFERENCE,
                ReviewCategory.EXCEPTION_HANDLING,
                ReviewCategory.RESOURCE_MANAGEMENT,
                ReviewCategory.PERFORMANCE,
                ReviewCategory.SECURITY,
                ReviewCategory.NAMING_CONVENTION
            ]

            # 프롬프트 생성
            prompt = self.prompt_builder.build_review_prompt(
                code=before_code,
                categories=categories,
                output_format=OutputFormat.IMPROVED_CODE,
                include_examples=True
            )

            # 시스템 프롬프트와 사용자 프롬프트 결합
            full_prompt = f"{self.prompt_builder.SYSTEM_PROMPT}\n\n{prompt}"

            # Step 2: LLM 분석 (30%)
            progress.setLabelText("AI 분석 중... (Phi-3-mini)")
            progress.setValue(30)

            if progress.wasCanceled():
                self.statusBar().showMessage("분석이 취소되었습니다.", 3000)
                return

            # Ollama로 코드 분석 (스트리밍 비활성화)
            improved_code = self.ollama_client.analyze_code(
                prompt=full_prompt,
                stream=False
            )

            # Step 3: 결과 처리 (80%)
            progress.setLabelText("결과 처리 중...")
            progress.setValue(80)

            # 결과를 After 에디터에 표시
            self.editor.set_after_text(improved_code)

            # 분석 결과 저장 (리포트 생성용)
            self.last_analysis = {
                'original_code': before_code,
                'improved_code': improved_code,
                'categories': [cat.value for cat in categories]
            }

            # Step 4: 완료 (100%)
            progress.setValue(100)
            progress.close()

            # 성공 메시지
            self.statusBar().showMessage("✅ 코드 분석 완료!", 5000)

            QMessageBox.information(
                self,
                "분석 완료",
                f"코드 분석이 완료되었습니다!\n\n"
                f"적용된 리뷰 카테고리:\n"
                f"• Null 참조 체크\n"
                f"• Exception 처리\n"
                f"• 리소스 관리\n"
                f"• 성능 최적화\n"
                f"• 보안\n"
                f"• 네이밍 컨벤션\n\n"
                f"개선된 코드가 After 에디터에 표시되었습니다.\n"
                f"리포트를 저장하려면 '파일 > 리포트 저장'을 사용하세요."
            )

        except Exception as e:
            progress.close()

            # 에러 처리
            self.statusBar().showMessage(f"❌ 분석 실패: {str(e)}", 10000)

            QMessageBox.critical(
                self,
                "분석 실패",
                f"코드 분석 중 오류가 발생했습니다.\n\n"
                f"오류: {str(e)}\n\n"
                f"다음을 확인해주세요:\n"
                f"1. Ollama 서버가 실행 중인지\n"
                f"2. phi3:mini 모델이 다운로드되었는지\n"
                f"3. 네트워크 연결 상태"
            )

        finally:
            # 분석 완료 후 버튼 다시 활성화
            self.analyze_button.setEnabled(True)

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
