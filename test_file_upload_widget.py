"""
FileUploadWidget 테스트 스크립트

파일 업로드 위젯의 기능을 테스트합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 PYTHONPATH에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.ui.file_upload_widget import FileUploadWidget


def test_file_upload_widget():
    """FileUploadWidget 테스트"""
    print("=" * 80)
    print("FileUploadWidget 테스트")
    print("=" * 80)

    app = QApplication(sys.argv)

    # FileUploadWidget 생성
    widget = FileUploadWidget()
    widget.setWindowTitle("📁 파일 업로드 위젯 테스트")
    widget.resize(700, 600)

    # 파일 변경 시그널 연결
    def on_files_changed(files):
        print(f"\n✅ 파일 목록 변경:")
        print(f"   총 {len(files)}개 파일")
        for i, file_path in enumerate(files, 1):
            print(f"   {i}. {Path(file_path).name} ({file_path})")

    widget.files_changed.connect(on_files_changed)

    # 윈도우 표시
    widget.show()

    print("\n📌 테스트 방법:")
    print("   1. '파일 추가' 버튼을 클릭하여 test_files/*.cs 파일을 선택하세요")
    print("   2. 또는 test_files 폴더에서 .cs 파일을 드래그 앤 드롭하세요")
    print("   3. 파일을 더블클릭하여 미리보기를 확인하세요")
    print("   4. '선택 제거' 버튼으로 파일을 제거하세요")
    print("   5. '전체 제거' 버튼으로 모든 파일을 삭제하세요")
    print("\n🔍 기대 동작:")
    print("   - .cs 파일만 추가 가능")
    print("   - 1MB 이상 파일은 거부됨")
    print("   - UTF-8 인코딩이 아닌 파일은 거부됨")
    print("   - 중복 파일은 건너뛰기")
    print("   - 파일 아이콘과 크기 표시")
    print("   - 드래그 시 배경색 변경 (파란색)")
    print("\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    test_file_upload_widget()
