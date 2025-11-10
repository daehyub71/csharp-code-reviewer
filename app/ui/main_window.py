"""
Main Window for C# Code Reviewer

This module provides the main application window with menu bar, toolbar, and status bar.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QPushButton,
    QLabel, QMessageBox, QFileDialog, QProgressDialog, QSplitter,
    QTabWidget
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeySequence, QIcon

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.ui.before_after_editor import BeforeAfterEditor
from app.ui.result_panel import ResultPanel
from app.ui.file_upload_widget import FileUploadWidget
from app.core.ollama_client import OllamaClient, OllamaClientError
from app.core.prompt_builder import PromptBuilder, ReviewCategory, OutputFormat
from app.core.report_generator import ReportGenerator
from app.core.batch_analyzer import BatchAnalyzer, BatchAnalysisResult
from app.utils.markdown_renderer import MarkdownRenderer
from app.services.report_saver import ReportSaver


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

        # Initialize Report Saver
        self.report_saver = ReportSaver()

        # Initialize Markdown Renderer (for HTML export)
        self.markdown_renderer = MarkdownRenderer(theme="monokai")

        # Store last analysis results
        self.last_analysis = {
            'original_code': '',
            'improved_code': '',
            'categories': [],
            'report_markdown': ''  # 생성된 Markdown 리포트 저장
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

        # Create horizontal splitter for input area and result panel
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create tab widget for different input modes
        self.input_tabs = QTabWidget()
        self.input_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3e3e42;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 8px 16px;
                border: 1px solid #3e3e42;
                border-bottom: none;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3e3e42;
            }
        """)

        # Tab 1: 텍스트 입력 모드 (기존 BeforeAfterEditor)
        self.editor = BeforeAfterEditor()
        self.input_tabs.addTab(self.editor, "✏️ 텍스트 입력")

        # Tab 2: 파일 업로드 모드
        self.file_upload_widget = FileUploadWidget()
        self.input_tabs.addTab(self.file_upload_widget, "📁 파일 업로드")

        splitter.addWidget(self.input_tabs)

        # Create result panel (리포트 표시용)
        self.result_panel = ResultPanel()
        splitter.addWidget(self.result_panel)

        # Set initial splitter sizes (70% input, 30% result panel)
        splitter.setSizes([700, 300])

        main_layout.addWidget(splitter)

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

        # View menu
        view_menu = menubar.addMenu("&View")

        # Report History action
        history_action = QAction("📜 리포트 히스토리(&H)...", self)
        history_action.setShortcut("Ctrl+H")
        history_action.setStatusTip("저장된 리포트 히스토리 조회")
        history_action.triggered.connect(self._on_show_report_history)
        view_menu.addAction(history_action)

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

        # Save button
        self.save_button = QPushButton("💾 Save Report")
        self.save_button.setFixedHeight(32)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #2c5aa0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d6fb8;
            }
            QPushButton:pressed {
                background-color: #1f4278;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
        """)
        self.save_button.clicked.connect(self._on_save)
        self.save_button.setEnabled(False)  # 초기에는 비활성화
        toolbar.addWidget(self.save_button)

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
        self.result_panel.clear()

        # 분석 결과 초기화
        self.last_analysis = {
            'original_code': '',
            'improved_code': '',
            'categories': [],
            'report_markdown': ''
        }

        # Save 버튼 비활성화
        self.save_button.setEnabled(False)

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
        """Handle Save action - Markdown과 HTML 둘 다 저장."""

        # 분석 결과가 있는지 확인
        if not self.last_analysis.get('improved_code'):
            QMessageBox.warning(
                self,
                "저장 실패",
                "저장할 분석 결과가 없습니다.\n\n"
                "먼저 코드 분석을 실행해주세요."
            )
            return

        # 자동 파일명 생성 (확장자 제외)
        default_filename = self.report_generator.generate_filename().replace('.md', '')

        # 저장 위치 선택 (폴더 선택)
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "리포트 저장 (Markdown + HTML)",
            default_filename,
            "Report Files (*.md *.html);;All Files (*)"
        )

        if file_path:
            try:
                # 프로그레스 다이얼로그
                progress = QProgressDialog("리포트 저장 중...", None, 0, 100, self)
                progress.setWindowTitle("리포트 저장")
                progress.setWindowModality(Qt.WindowModality.WindowModal)
                progress.setMinimumDuration(0)
                progress.setValue(0)

                # Step 1: Markdown 리포트 생성 또는 재사용 (20%)
                progress.setLabelText("Markdown 리포트 생성 중...")
                progress.setValue(20)

                # 이미 생성된 리포트가 있으면 재사용
                if self.last_analysis.get('report_markdown'):
                    markdown_report = self.last_analysis['report_markdown']
                else:
                    markdown_report = self.report_generator.generate_report(
                        original_code=self.last_analysis['original_code'],
                        improved_code=self.last_analysis['improved_code'],
                        categories=self.last_analysis['categories'],
                        model_name="phi3:mini"
                    )

                # Step 2: HTML 생성 (40%)
                progress.setLabelText("HTML 변환 중...")
                progress.setValue(40)

                html_report = self.markdown_renderer.render(markdown_report)

                # Step 3: 파일 경로 생성 (60%)
                progress.setLabelText("파일 저장 경로 설정 중...")
                progress.setValue(60)

                # 확장자가 없으면 .md 추가
                if not file_path.endswith(('.md', '.html')):
                    base_path = file_path
                else:
                    # 확장자 제거
                    base_path = file_path.rsplit('.', 1)[0]

                md_path = f"{base_path}.md"
                html_path = f"{base_path}.html"

                # Step 4: Markdown 파일 저장 (70%)
                progress.setLabelText("Markdown 파일 저장 중...")
                progress.setValue(70)

                self.report_generator.save_report(markdown_report, md_path)

                # Step 5: HTML 파일 저장 (85%)
                progress.setLabelText("HTML 파일 저장 중...")
                progress.setValue(85)

                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_report)

                # Step 6: 완료 (100%)
                progress.setValue(100)
                progress.close()

                # 성공 메시지
                self.statusBar().showMessage(f"✅ 리포트 저장 완료: {md_path}, {html_path}", 5000)

                QMessageBox.information(
                    self,
                    "저장 완료",
                    f"리포트가 성공적으로 저장되었습니다!\n\n"
                    f"📄 Markdown: {md_path}\n"
                    f"🌐 HTML: {html_path}\n\n"
                    f"HTML 파일을 브라우저로 열어서 확인하실 수 있습니다."
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
        self.result_panel.clear()

        # 분석 결과 초기화
        self.last_analysis = {
            'original_code': '',
            'improved_code': '',
            'categories': [],
            'report_markdown': ''
        }

        # Save 버튼 비활성화
        self.save_button.setEnabled(False)

        self.statusBar().showMessage("All editors cleared", 3000)

    def _on_analyze(self):
        """Handle Analyze action."""

        # 현재 활성화된 탭 확인
        current_tab_index = self.input_tabs.currentIndex()

        # 분석할 코드 가져오기
        before_code = ""
        source_type = ""  # "text" or "file"
        file_name = ""  # 파일 이름 (파일 모드인 경우)

        if current_tab_index == 0:
            # 텍스트 입력 모드
            before_code = self.editor.get_before_text().strip()
            source_type = "text"

            if not before_code:
                QMessageBox.warning(self, "코드 없음", "Before 에디터에 C# 코드를 붙여넣어주세요.")
                return

        elif current_tab_index == 1:
            # 파일 업로드 모드
            selected_files = self.file_upload_widget.get_selected_files()

            if not selected_files:
                QMessageBox.warning(
                    self,
                    "파일 없음",
                    "파일 업로드 탭에서 분석할 C# 파일을 추가해주세요."
                )
                return

            # Day 11: 다중 파일 분석
            if len(selected_files) > 1:
                # 다중 파일 배치 분석
                self._analyze_multiple_files(selected_files)
                return

            # 단일 파일 분석 (기존 로직)
            first_file = selected_files[0]
            file_name = Path(first_file).name

            try:
                with open(first_file, 'r', encoding='utf-8') as f:
                    before_code = f.read().strip()

                source_type = "file"

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "파일 읽기 오류",
                    f"파일을 읽을 수 없습니다:\n{first_file}\n\n오류: {str(e)}"
                )
                return

            if not before_code:
                QMessageBox.warning(
                    self,
                    "빈 파일",
                    f"파일이 비어있습니다:\n{file_name}"
                )
                return

        if self.ollama_client is None:
            QMessageBox.warning(self, "연결 안 됨", "Ollama 클라이언트가 연결되지 않았습니다. 연결을 확인해주세요.")
            return

        # 프로그레스 다이얼로그 생성
        if source_type == "file":
            progress_title = f"AI 코드 분석 - {file_name}"
            initial_message = f"{file_name} 분석 중..."
        else:
            progress_title = "AI 코드 분석"
            initial_message = "코드 분석 중..."

        progress = QProgressDialog(initial_message, "취소", 0, 100, self)
        progress.setWindowTitle(progress_title)
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
                ReviewCategory.NAMING_CONVENTION,
                ReviewCategory.CODE_DOCUMENTATION
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

            # 파일 모드인 경우 Before 에디터에도 원본 코드 표시 (비교를 위해)
            if source_type == "file":
                self.editor.set_before_text(before_code)
                # 텍스트 입력 탭으로 자동 전환 (결과 확인을 위해)
                self.input_tabs.setCurrentIndex(0)

            # Step 4: 리포트 생성 및 표시 (90%)
            progress.setLabelText("리포트 생성 중...")
            progress.setValue(90)

            # Markdown 리포트 생성
            report_markdown = self.report_generator.generate_report(
                original_code=before_code,
                improved_code=improved_code,
                categories=[cat.value for cat in categories],
                model_name="phi3:mini"
            )

            # 분석 결과 저장 (리포트 생성용)
            self.last_analysis = {
                'original_code': before_code,
                'improved_code': improved_code,
                'categories': [cat.value for cat in categories],
                'report_markdown': report_markdown  # 생성된 리포트 저장
            }

            # ResultPanel에 리포트 표시
            self.result_panel.set_markdown(report_markdown)

            # Save 버튼 활성화
            self.save_button.setEnabled(True)

            # Step 5: 완료 (100%)
            progress.setValue(100)
            progress.close()

            # 파일 모드인 경우 자동 저장
            saved_paths_msg = ""
            if source_type == "file":
                try:
                    analysis_time = 0.0  # TODO: 실제 분석 시간 측정
                    md_path, html_path, record_id = self.report_saver.save_report(
                        filename=file_name,
                        original_code=before_code,
                        improved_code=improved_code,
                        report_markdown=report_markdown,
                        analysis_time=analysis_time,
                        success=True
                    )

                    saved_paths_msg = (
                        f"\n\n📁 리포트가 자동 저장되었습니다:\n"
                        f"• Markdown: {md_path}\n"
                        f"• HTML: {html_path}"
                    )

                except Exception as save_error:
                    print(f"리포트 자동 저장 실패: {save_error}")
                    saved_paths_msg = f"\n\n⚠️ 리포트 자동 저장 실패: {save_error}"

            # 성공 메시지
            if source_type == "file":
                status_msg = f"✅ {file_name} 분석 완료!"
                dialog_title = f"분석 완료 - {file_name}"
                dialog_msg = (
                    f"파일 분석이 완료되었습니다!\n\n"
                    f"파일: {file_name}\n\n"
                    f"적용된 리뷰 카테고리:\n"
                    f"• Null 참조 체크\n"
                    f"• Exception 처리\n"
                    f"• 리소스 관리\n"
                    f"• 성능 최적화\n"
                    f"• 보안\n"
                    f"• 네이밍 컨벤션\n"
                    f"• XML 문서 주석\n\n"
                    f"개선된 코드가 텍스트 입력 탭에 표시되었습니다."
                    f"{saved_paths_msg}"
                )
            else:
                status_msg = "✅ 코드 분석 완료!"
                dialog_title = "분석 완료"
                dialog_msg = (
                    f"코드 분석이 완료되었습니다!\n\n"
                    f"적용된 리뷰 카테고리:\n"
                    f"• Null 참조 체크\n"
                    f"• Exception 처리\n"
                    f"• 리소스 관리\n"
                    f"• 성능 최적화\n"
                    f"• 보안\n"
                    f"• 네이밍 컨벤션\n"
                    f"• XML 문서 주석\n\n"
                    f"개선된 코드가 After 에디터에 표시되었습니다.\n"
                    f"리포트를 저장하려면 '💾 Save Report' 버튼을 사용하세요."
                )

            self.statusBar().showMessage(status_msg, 5000)

            QMessageBox.information(self, dialog_title, dialog_msg)

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

    def _on_show_report_history(self):
        """리포트 히스토리 다이얼로그 표시"""
        from PySide6.QtWidgets import (
            QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
            QPushButton, QLabel, QHeaderView, QMessageBox
        )
        from PySide6.QtCore import Qt
        from datetime import datetime
        import webbrowser
        import os

        dialog = QDialog(self)
        dialog.setWindowTitle("📜 리포트 히스토리")
        dialog.resize(1000, 600)

        layout = QVBoxLayout()

        # 통계 정보
        stats = self.report_saver.db.get_statistics()
        stats_label = QLabel()
        stats_label.setTextFormat(Qt.TextFormat.RichText)
        stats_label.setText(
            f"<p><b>총 리포트:</b> {stats['total']}개 | "
            f"<b>성공:</b> {stats['success']}개 | "
            f"<b>실패:</b> {stats['failed']}개 | "
            f"<b>평균 분석 시간:</b> {stats['avg_analysis_time']:.2f}초</p>"
        )
        layout.addWidget(stats_label)

        # 테이블 위젯
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "파일명", "생성 시간", "상태", "분석 시간 (초)", "경로"])

        # 테이블 설정
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # 리포트 목록 조회
        reports = self.report_saver.db.get_all_reports(limit=100)  # 최근 100개

        table.setRowCount(len(reports))

        for row, record in enumerate(reports):
            # ID
            id_item = QTableWidgetItem(str(record.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 0, id_item)

            # 파일명
            filename_item = QTableWidgetItem(record.filename)
            table.setItem(row, 1, filename_item)

            # 생성 시간
            try:
                dt = datetime.fromisoformat(record.timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                time_str = record.timestamp
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 2, time_item)

            # 상태
            status_item = QTableWidgetItem("✅ 성공" if record.success else "❌ 실패")
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 3, status_item)

            # 분석 시간
            time_item = QTableWidgetItem(f"{record.analysis_time:.2f}")
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 4, time_item)

            # 경로
            path_item = QTableWidgetItem(record.html_path)
            table.setItem(row, 5, path_item)

        # 더블클릭 이벤트: HTML 파일 열기
        def on_double_click(row, col):
            if row >= 0:
                html_path = table.item(row, 5).text()
                if os.path.exists(html_path):
                    webbrowser.open(f"file://{html_path}")
                else:
                    QMessageBox.warning(
                        dialog,
                        "파일 없음",
                        f"리포트 파일을 찾을 수 없습니다:\n{html_path}"
                    )

        table.cellDoubleClicked.connect(on_double_click)

        layout.addWidget(table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 새로고침 버튼
        refresh_btn = QPushButton("🔄 새로고침")

        def refresh():
            dialog.close()
            self._on_show_report_history()

        refresh_btn.clicked.connect(refresh)
        button_layout.addWidget(refresh_btn)

        # 삭제 버튼
        delete_btn = QPushButton("🗑️ 선택 항목 삭제")

        def delete_selected():
            selected_rows = table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(dialog, "선택 없음", "삭제할 리포트를 선택하세요.")
                return

            row = selected_rows[0].row()
            report_id = int(table.item(row, 0).text())
            filename = table.item(row, 1).text()

            reply = QMessageBox.question(
                dialog,
                "삭제 확인",
                f"다음 리포트를 삭제하시겠습니까?\n\n"
                f"ID: {report_id}\n"
                f"파일: {filename}\n\n"
                f"(DB 레코드 및 파일 모두 삭제됩니다)",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.report_saver.db.delete_report_with_files(report_id)
                if success:
                    QMessageBox.information(dialog, "삭제 완료", "리포트가 삭제되었습니다.")
                    refresh()
                else:
                    QMessageBox.critical(dialog, "삭제 실패", "리포트 삭제 중 오류가 발생했습니다.")

        delete_btn.clicked.connect(delete_selected)
        button_layout.addWidget(delete_btn)

        button_layout.addStretch()

        # 닫기 버튼
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        # 도움말
        help_label = QLabel(
            "💡 리포트를 더블클릭하면 HTML 파일이 웹 브라우저에서 열립니다."
        )
        help_label.setStyleSheet("color: #858585; font-size: 12px;")
        layout.addWidget(help_label)

        dialog.setLayout(layout)
        dialog.exec()

    def _analyze_multiple_files(self, file_paths: List[str]):
        """
        다중 파일 배치 분석 (Day 11)

        Args:
            file_paths: 분석할 파일 경로 목록
        """
        if self.ollama_client is None:
            QMessageBox.warning(
                self,
                "연결 안 됨",
                "Ollama 클라이언트가 연결되지 않았습니다. 연결을 확인해주세요."
            )
            return

        # 배치 분석기 생성
        batch_analyzer = BatchAnalyzer(
            ollama_client=self.ollama_client,
            prompt_builder=self.prompt_builder
        )

        # 프로그레스 다이얼로그 생성
        progress = QProgressDialog(
            f"파일 분석 준비 중...",
            "취소",
            0,
            len(file_paths),
            self
        )
        progress.setWindowTitle(f"다중 파일 분석 - {len(file_paths)}개 파일")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        # 취소 플래그
        self._batch_cancelled = False

        def on_progress(current: int, total: int, file_name: str):
            """프로그레스 업데이트 콜백"""
            if progress.wasCanceled():
                self._batch_cancelled = True
                return

            progress.setLabelText(
                f"분석 중: {file_name}\n"
                f"진행률: {current + 1}/{total} 파일"
            )
            progress.setValue(current + 1)
            QApplication.processEvents()

        def is_cancelled():
            """취소 여부 확인 콜백"""
            return self._batch_cancelled or progress.wasCanceled()

        # 분석 중 버튼 비활성화
        self.analyze_button.setEnabled(False)

        try:
            # 배치 분석 실행
            self.statusBar().showMessage(f"🔄 {len(file_paths)}개 파일 분석 시작...", 3000)

            batch_result = batch_analyzer.analyze_files(
                file_paths=file_paths,
                progress_callback=on_progress,
                is_cancelled_callback=is_cancelled
            )

            progress.close()

            # 성공한 파일들의 리포트 자동 저장
            saved_count = 0
            for result in batch_result.results:
                if result.success:
                    try:
                        md_path, html_path, record_id = self.report_saver.save_report(
                            filename=result.file_name,
                            original_code=result.original_code,
                            improved_code=result.improved_code,
                            report_markdown=result.report_markdown,
                            analysis_time=result.analysis_time,
                            success=True
                        )
                        saved_count += 1
                    except Exception as save_error:
                        print(f"{result.file_name} 리포트 저장 실패: {save_error}")

            # 결과 요약 다이얼로그 표시
            self._show_batch_results_dialog(batch_result, saved_count)

            # 상태바 업데이트
            if batch_result.success_count > 0:
                self.statusBar().showMessage(
                    f"✅ 분석 완료: 성공 {batch_result.success_count}개, "
                    f"실패 {batch_result.failure_count}개, "
                    f"건너뜀 {batch_result.skipped_count}개 | "
                    f"리포트 {saved_count}개 저장됨",
                    10000
                )
            else:
                self.statusBar().showMessage(
                    f"❌ 모든 파일 분석 실패",
                    10000
                )

        except Exception as e:
            progress.close()

            self.statusBar().showMessage(f"❌ 배치 분석 실패: {str(e)}", 10000)

            QMessageBox.critical(
                self,
                "배치 분석 실패",
                f"다중 파일 분석 중 오류가 발생했습니다.\n\n"
                f"오류: {str(e)}\n\n"
                f"다음을 확인해주세요:\n"
                f"1. Ollama 서버가 실행 중인지\n"
                f"2. phi3:mini 모델이 다운로드되었는지\n"
                f"3. 네트워크 연결 상태"
            )

        finally:
            # 분석 완료 후 버튼 다시 활성화
            self.analyze_button.setEnabled(True)
            self._batch_cancelled = False

    def _show_batch_results_dialog(self, batch_result: BatchAnalysisResult, saved_count: int = 0):
        """
        배치 분석 결과 요약 다이얼로그 표시

        Args:
            batch_result: 배치 분석 결과
            saved_count: 저장된 리포트 개수
        """
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
        from PySide6.QtCore import Qt

        dialog = QDialog(self)
        dialog.setWindowTitle("다중 파일 분석 결과")
        dialog.resize(700, 600)

        layout = QVBoxLayout()

        # 요약 정보
        summary_label = QLabel()
        summary_label.setTextFormat(Qt.TextFormat.RichText)
        summary_label.setText(
            f"<h3>📊 분석 결과 요약</h3>"
            f"<p><b>총 파일:</b> {batch_result.total_files}개</p>"
            f"<p><b>✅ 성공:</b> {batch_result.success_count}개</p>"
            f"<p><b>❌ 실패:</b> {batch_result.failure_count}개</p>"
            f"<p><b>⏭️ 건너뜀:</b> {batch_result.skipped_count}개</p>"
            f"<p><b>⏱️ 총 소요 시간:</b> {batch_result.total_time:.2f}초</p>"
            f"<p><b>💾 자동 저장된 리포트:</b> {saved_count}개 (reports/markdown/, reports/html/)</p>"
        )
        layout.addWidget(summary_label)

        # 파일별 상세 결과
        details_label = QLabel("<h4>📝 파일별 상세 결과</h4>")
        layout.addWidget(details_label)

        details_text = QTextEdit()
        details_text.setReadOnly(True)

        # 결과 텍스트 생성
        details_content = []
        for i, result in enumerate(batch_result.results, 1):
            status_icon = "✅" if result.success else "❌"
            details_content.append(f"{i}. {status_icon} {result.file_name}")

            if result.success:
                details_content.append(f"   - 분석 시간: {result.analysis_time:.2f}초")
                if result.retry_count > 0:
                    details_content.append(f"   - 재시도 횟수: {result.retry_count}회")
                details_content.append(f"   - 개선된 코드: {len(result.improved_code)} 문자")
                details_content.append(f"   - 리포트: {len(result.report_markdown)} 문자")
            else:
                details_content.append(f"   - 오류: {result.error_message}")

            details_content.append("")  # 빈 줄

        details_text.setPlainText("\n".join(details_content))
        layout.addWidget(details_text)

        # 버튼
        button_layout = QHBoxLayout()

        # 성공한 결과 저장 버튼
        if batch_result.success_count > 0:
            save_btn = QPushButton("💾 성공 결과 저장")
            save_btn.clicked.connect(lambda: self._save_batch_results(batch_result))
            button_layout.addWidget(save_btn)

        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec()

    def _save_batch_results(self, batch_result: BatchAnalysisResult):
        """
        배치 분석 결과를 파일로 저장

        Args:
            batch_result: 배치 분석 결과
        """
        from PySide6.QtWidgets import QFileDialog
        import os

        # 저장할 디렉토리 선택
        directory = QFileDialog.getExistingDirectory(
            self,
            "결과 저장 위치 선택",
            "",
            QFileDialog.Option.ShowDirsOnly
        )

        if not directory:
            return

        try:
            saved_count = 0

            # 성공한 파일들의 결과만 저장
            for result in batch_result.results:
                if not result.success:
                    continue

                # 파일명에서 확장자 제거하고 _report.md 추가
                base_name = Path(result.file_name).stem
                report_file = os.path.join(directory, f"{base_name}_report.md")
                improved_file = os.path.join(directory, f"{base_name}_improved.cs")

                # 리포트 저장
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(result.report_markdown)

                # 개선된 코드 저장
                with open(improved_file, 'w', encoding='utf-8') as f:
                    f.write(result.improved_code)

                saved_count += 1

            QMessageBox.information(
                self,
                "저장 완료",
                f"✅ {saved_count}개 파일의 결과를 저장했습니다.\n\n"
                f"저장 위치: {directory}\n\n"
                f"각 파일당 2개 파일 생성:\n"
                f"• [파일명]_report.md (리포트)\n"
                f"• [파일명]_improved.cs (개선된 코드)"
            )

            self.statusBar().showMessage(f"✅ {saved_count}개 결과 저장 완료", 5000)

        except Exception as e:
            QMessageBox.critical(
                self,
                "저장 실패",
                f"결과 저장 중 오류가 발생했습니다.\n\n오류: {str(e)}"
            )
            self.statusBar().showMessage(f"❌ 저장 실패: {str(e)}", 5000)


# Test the main window
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
