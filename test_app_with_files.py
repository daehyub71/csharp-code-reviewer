"""
메인 앱 테스트 (파일 업로드 모드 포함)

파일 업로드 모드와 텍스트 입력 모드를 모두 테스트합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 PYTHONPATH에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main():
    """메인 앱 실행"""
    print("=" * 80)
    print("C# Code Reviewer - 파일 업로드 모드 테스트")
    print("=" * 80)
    print()
    print("📌 테스트 방법:")
    print("   1. '📁 파일 업로드' 탭을 클릭하세요")
    print("   2. test_files 폴더의 .cs 파일들을 드래그 앤 드롭하거나 '파일 추가' 버튼으로 추가하세요")
    print("   3. '▶ Analyze Code' 버튼을 클릭하세요")
    print("   4. 파일 분석이 완료되면 '텍스트 입력' 탭에 Before/After 코드가 표시됩니다")
    print("   5. 오른쪽 패널에 Markdown 리포트가 표시됩니다")
    print("   6. '💾 Save Report' 버튼으로 리포트를 저장할 수 있습니다")
    print()
    print("🔍 확인 사항:")
    print("   ✓ 파일 업로드 모드에서 분석 가능")
    print("   ✓ 다중 파일 선택 시 첫 번째 파일만 분석 (안내 메시지 표시)")
    print("   ✓ 분석 완료 후 텍스트 입력 탭으로 자동 전환")
    print("   ✓ Before/After 코드 비교 가능")
    print("   ✓ Markdown 리포트 표시")
    print()

    app = QApplication(sys.argv)

    # MainWindow 생성
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
