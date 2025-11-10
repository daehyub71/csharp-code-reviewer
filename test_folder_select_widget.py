"""
FolderSelectWidget 테스트 스크립트

폴더 선택 위젯의 기능을 테스트합니다.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from app.ui.folder_select_widget import FolderSelectWidget


class TestWindow(QMainWindow):
    """테스트용 메인 윈도우"""

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("FolderSelectWidget 테스트")
        self.resize(1000, 700)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 테스트 안내
        info_label = QLabel(
            "=" * 80 + "\n"
            "FolderSelectWidget 테스트\n"
            "=" * 80 + "\n\n"
            "📌 테스트 방법:\n"
            "   1. '📂 폴더 선택' 버튼을 클릭하여 C# 프로젝트 폴더를 선택하세요\n"
            "   2. 트리 구조로 폴더/파일이 표시됩니다\n"
            "   3. 체크박스를 클릭하여 파일을 선택하세요\n"
            "   4. 폴더를 체크하면 하위 파일이 모두 선택됩니다\n"
            "   5. '✅ 전체 선택' / '❌ 전체 해제' 버튼을 사용하세요\n\n"
            "🔍 기대 동작:\n"
            "   - C# 파일(.cs)만 표시됨\n"
            "   - .git, .vs, bin, obj 폴더는 제외됨\n"
            "   - 최대 100개 파일까지 표시됨\n"
            "   - 폴더 아이콘(📁)과 파일 아이콘(📄) 구분\n"
            "   - 파일 개수와 크기 표시\n"
            "   - 체크박스 상태가 부모/자식 간 연동됨\n\n"
        )
        info_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 15px;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 9pt;
            }
        """)
        layout.addWidget(info_label)

        # 폴더 선택 위젯
        self.folder_widget = FolderSelectWidget()
        self.folder_widget.files_changed.connect(self._on_files_changed)
        layout.addWidget(self.folder_widget)

        # 선택된 파일 개수 레이블
        self.selected_label = QLabel("✅ 선택된 파일: 0개")
        self.selected_label.setStyleSheet("""
            QLabel {
                background-color: #0e639c;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 10pt;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.selected_label)

        # 다크 테마 적용
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)

    def _on_files_changed(self, file_paths: list):
        """선택된 파일 목록이 변경될 때 호출"""
        count = len(file_paths)
        self.selected_label.setText(f"✅ 선택된 파일: {count}개")

        print("\n" + "=" * 80)
        print(f"파일 목록 변경: {count}개 파일 선택됨")
        print("=" * 80)

        if count > 0 and count <= 10:
            print("\n선택된 파일:")
            for i, path in enumerate(file_paths, 1):
                print(f"   {i}. {path}")
        elif count > 10:
            print(f"\n선택된 파일 (처음 10개만 표시):")
            for i, path in enumerate(file_paths[:10], 1):
                print(f"   {i}. {path}")
            print(f"   ... (나머지 {count - 10}개)")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 폰트 설정
    app.setStyle("Fusion")

    window = TestWindow()
    window.show()

    sys.exit(app.exec())
