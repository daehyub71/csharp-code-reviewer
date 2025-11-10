# Development Timeline - C# Code Reviewer

## 6주 개발 일정 상세

---

### Week 1: 기본 구조 및 LLM 통합 (Day 1-4)

#### Day 1 (2025-01-08): 프로젝트 초기 설정 ✅
**목표**: 개발 환경 구축 및 프로젝트 구조 생성

**Tasks**:
- [x] 프로젝트 계획서 작성
  - [x] PROJECT_PLAN.md
  - [x] DEVELOPMENT_TIMELINE.md
  - [x] README.md
  - [x] TECHNICAL_SPECIFICATION.md
  - [x] CLAUDE.md (추가)
- [x] Git 저장소 생성
  - [x] `.gitignore` 설정 (Python, PySide6)
  - [x] 초기 커밋
- [x] 프로젝트 디렉토리 구조 생성
  - [x] app/ui/, app/core/, app/utils/, app/config/
  - [x] tests/, docs/, resources/, scripts/
  - [x] __init__.py 파일 생성 (Python 패키지)
- [x] Python 가상환경 설정
  - [x] venv 생성 (Python 3.13.7)
  - [x] requirements.txt 작성
  - [x] 기본 의존성 설치
    - PySide6 (6.10.0)
    - ollama (0.6.0)
    - markdown (3.10)
    - pygments (2.19.2)
    - pytest (8.4.2)
    - pytest-qt (4.5.0)
    - pytest-cov (7.0.0)
    - PyInstaller (6.16.0)
    - python-dotenv (1.2.1)

**산출물**: ✅
- 프로젝트 구조 완성
- 가상환경 및 의존성 설치 완료
- 문서화 (5개 주요 문서: PROJECT_PLAN, DEVELOPMENT_TIMELINE, README, TECHNICAL_SPECIFICATION, CLAUDE)
- Git 저장소 초기화 및 첫 커밋 완료

---

#### Day 2 (2025-01-09): Ollama 통합 및 Phi-3-mini 테스트 ✅
**목표**: LLM 백엔드 설정 및 동작 확인

**Tasks**:
- [x] Ollama 설치 및 실행
  - [x] `ollama pull phi3:mini` 모델 다운로드 (2.2GB, Q4_0 양자화)
  - [x] `ollama serve` 백그라운드 실행 확인 (localhost:11434)
- [x] `app/core/ollama_client.py` 구현
  - [x] Ollama Python SDK 초기화 (v0.6.0)
  - [x] 연결 테스트 함수 (test_connection)
  - [x] 프롬프트 전송 함수 (analyze_code)
  - [x] 스트리밍 응답 처리 (_stream_response)
  - [x] 에러 핸들링 (OllamaConnectionError, ModelNotFoundError, 재시도 로직)
- [x] 테스트 스크립트 작성
  - [x] 간단한 C# 코드 샘플 (3가지 크기: Small/Medium/Large)
  - [x] LLM 응답 확인 (Hello World 코드 리뷰 성공)
  - [x] tests/test_ollama_performance.py 작성
- [x] 성능 벤치마크
  - [x] 10줄 코드: 22.4초 (목표 2초, ✗ 초과)
  - [x] 40줄 코드: 14.6초 (목표 5초, ✗ 초과)
  - [x] 100줄 코드: 18.1초 (목표 20초, ✓ 달성)
  - [x] 평균 응답 시간: 18.3초
  - [x] 메모리 사용량: ~3GB (Ollama + 모델)

**산출물**: ✅
- Ollama 클라이언트 완성 (app/core/ollama_client.py, 250+ lines)
- LLM 응답 시간 데이터 수집 (3가지 코드 크기 테스트)
- 연결 테스트 통과 (phi3:mini, 3.8B params)
- 성능 벤치마크 스크립트 작성 (tests/test_ollama_performance.py)
- **성능 이슈**: CPU 기반 추론으로 인해 작은 코드도 14~22초 소요 (프롬프트 최적화 필요)

---

#### Day 3 (2025-01-10): PySide6 기본 UI 및 Before/After 에디터 ✅
**목표**: 메인 윈도우 및 코드 에디터 구현

**Tasks**:
- [x] `app/main.py` 작성
  - [x] PySide6 QApplication 초기화
  - [x] 메인 윈도우 생성
  - [x] 이벤트 루프 실행
  - [x] High DPI scaling 지원
  - [x] 다크 테마 스타일시트 로드
- [x] `app/ui/main_window.py` 구현 (370+ lines)
  - [x] 메인 윈도우 레이아웃 (1400x800)
  - [x] 메뉴바 (파일, 편집, 도구, 도움말)
    - 파일: New, Open, Save, Exit
    - 편집: Copy Before/After, Clear All
    - 도구: Analyze Code, Test Ollama Connection
    - 도움말: About
  - [x] 툴바 (Analyze, Clear, Settings 버튼)
  - [x] 상태바 (Ollama 상태 실시간 표시, 모델 정보)
  - [x] Ollama 연결 테스트 및 자동 상태 업데이트
- [x] `app/ui/before_after_editor.py` 구현 (260+ lines)
  - [x] QPlainTextEdit 기반 CodeEditor 클래스
  - [x] EditorPanel (제목 + 에디터 + 복사 버튼)
  - [x] Before 에디터 (편집 가능, placeholder 텍스트)
  - [x] After 에디터 (읽기 전용)
  - [x] Horizontal Splitter (50:50 분할, 드래그 가능)
  - [x] 복사 버튼 (📋 Copy) 및 클립보드 기능
  - [x] Signal/Slot 연결 (text_changed 이벤트)
- [x] 기본 스타일링
  - [x] resources/styles/dark_theme.qss 작성 (VS Code Dark+ 테마)
  - [x] 폰트 설정 (Monaco, Consolas, Courier New - monospace)
  - [x] 색상 스키마 (#1e1e1e 배경, #d4d4d4 텍스트)
  - [x] 버튼, 메뉴, 스크롤바, Splitter 스타일링

**산출물**: ✅
- 메인 윈도우 UI 완성 (app/main.py, app/ui/main_window.py)
- Before/After 에디터 동작 확인 (app/ui/before_after_editor.py)
- VS Code Dark+ 스타일 다크 테마 적용 (resources/styles/dark_theme.qss)
- Ollama 연결 상태 실시간 모니터링
- 파일 열기/저장 기능 구현
- 키보드 단축키 지원 (F5: Analyze, Ctrl+O: Open, Ctrl+S: Save, etc.)
- **GUI 테스트 성공**: 모든 윈도우 정상 실행 확인

---

#### Day 4 (2025-01-11): Syntax Highlighting 및 동기화 스크롤
**목표**: 코드 가독성 향상 및 UX 개선

**Tasks**:
- [x] `app/utils/syntax_highlighter.py` 구현
  - [x] QSyntaxHighlighter 상속
  - [x] C# 키워드 정의 (class, public, void, if, etc.)
  - [x] 정규식 기반 토큰 파싱
  - [x] 색상 스키마 정의
    - 키워드: #569CD6 (파란색)
    - 문자열: #CE9178 (주황색)
    - 주석: #6A9955 (초록색)
    - 숫자: #B5CEA8 (연두색)
- [x] Syntax Highlighter 적용
  - [x] Before/After 에디터에 연결
  - [x] 실시간 하이라이팅 확인
- [x] 동기화 스크롤 구현
  - [x] Before 에디터 스크롤 이벤트 감지
  - [x] After 에디터 스크롤 위치 동기화
  - [x] 토글 버튼 (동기화 ON/OFF)
- [x] 추가 기능
  - [x] 라인 번호 표시
  - [x] 현재 줄 하이라이팅
  - [x] Ctrl+A 전체 선택 단축키 (기본 QPlainTextEdit 기능으로 지원됨)

**산출물**:
- C# Syntax Highlighting 완성 ✅
- 동기화 스크롤 동작 확인 ✅
- 사용자 친화적 에디터 완성 ✅

**완료일**: 2025-01-11

---

### Week 2: 코드 분석 엔진 (Day 5-8)

#### Day 5 (2025-01-12): Prompt Builder 및 6가지 리뷰 항목
**목표**: LLM 프롬프트 설계 및 최적화

**Tasks**:
- [x] `app/core/prompt_builder.py` 구현
  - [x] 프롬프트 템플릿 정의
  - [x] 6가지 리뷰 항목 템플릿
    1. Null 참조 체크
    2. Exception 처리 누락
    3. 리소스 해제
    4. 성능 이슈
    5. 보안 취약점
    6. 네이밍 컨벤션
  - [x] 코드 주석 생성 템플릿
  - [x] 플로우 다이어그램 템플릿
- [x] 프롬프트 변수 치환
  - [x] `{user_code}` → 실제 C# 코드
  - [x] `{review_options}` → 체크박스 선택 항목
- [x] 프롬프트 최적화
  - [x] 토큰 수 최소화 (목표: <1500 토큰)
  - [x] Few-shot 예제 추가
- [x] 테스트
  - [x] 샘플 코드 5개로 프롬프트 생성 확인

**산출물**:
- 프롬프트 템플릿 완성 ✅
- 토큰 사용량 분석 (평균: 212, 최대: 295, 목표: <1500) ✅
- Few-shot 예제 3개 작성 ✅

**테스트 결과**:
- ✅ Sample 1 (간단한 데이터 처리): 163 토큰
- ✅ Sample 2 (파일 읽기): 270 토큰
- ✅ Sample 3 (데이터베이스 연결): 295 토큰
- ✅ Sample 4 (데이터 변환): 131 토큰
- ✅ Sample 5 (사용자 검증): 203 토큰
- **평균 토큰 수**: 212 토큰
- **최대 토큰 수**: 295 토큰
- **목표 달성**: ✅ 모든 프롬프트 < 1500 토큰

**완료일**: 2025-01-12

---

#### Day 6 (2025-01-13): Report Generator 및 Markdown 생성
**목표**: LLM 응답을 Markdown 리포트로 변환

**Tasks**:
- [x] `app/core/report_generator.py` 구현
  - [x] LLM 응답 파싱
  - [x] Markdown 구조화
    - 요약 섹션 (줄 수, 추가 줄, 카테고리)
    - 적용된 리뷰 카테고리
    - Before/After 코드 비교
    - 주요 개선 사항 (휴리스틱 분석)
  - [x] After 코드 추출 (마크다운 블록 제거)
  - [x] 메타데이터 추가 (분석 시각, 모델명)
- [x] Markdown 템플릿
  - [x] resources/templates/report_template.md
  - [x] GitHub 스타일 형식
  - [x] 코드 블록 (```csharp```)
- [x] 파일 저장 기능
  - [x] 파일명 자동 생성 (code_review_{타임스탬프}.md)
  - [x] 저장 위치 선택 다이얼로그
  - [x] 프로그레스 다이얼로그
- [x] MainWindow 통합
  - [x] 분석 중 프로그레스바 표시
  - [x] 분석 결과 저장 (last_analysis)
  - [x] 리포트 저장 기능 개선
  - [x] 한글 UI 메시지

**산출물**:
- Report Generator 완성 ✅
- Markdown 템플릿 작성 ✅
- 파일 저장 기능 동작 확인 ✅

**테스트 결과**:
- ✅ 리포트 생성 테스트 (모든 섹션 검증 통과)
- ✅ 파일 저장 테스트 (임시 디렉토리 저장 확인)
- ✅ 파일명 생성 테스트 (타임스탬프 형식 확인)
- ✅ 코드 추출 테스트 (마크다운 블록 제거)

**완료일**: 2025-01-13

---

#### Day 7 (2025-01-14): QTextBrowser 렌더링 및 Pygments 통합
**목표**: Markdown을 HTML로 변환하여 표시

**Tasks**:
- ✅ `app/utils/markdown_renderer.py` 구현
  - ✅ python-markdown 라이브러리 사용
  - ✅ Extensions 설정
    - ✅ fenced_code (코드 블록)
    - ✅ tables (표)
    - ✅ codehilite (코드 하이라이팅)
  - ✅ Pygments 통합
    - ✅ C# lexer 설정
    - ✅ Monokai 색상 테마
  - ✅ GitHub 스타일 CSS
    - ✅ resources/styles/github_markdown.css
- ✅ `app/ui/result_panel.py` 구현
  - ✅ QTextBrowser 초기화
  - ✅ HTML 설정 (setHtml)
  - ✅ CSS 로드 및 적용
  - ✅ 스크롤 위치 복원
  - ✅ 툴바 기능 (확대/축소, 스크롤 이동)
- ✅ 테스트
  - ✅ 샘플 Markdown 렌더링 확인
  - ✅ 코드 블록 하이라이팅 확인 (Pygments Monokai 테마)
  - ✅ 표 및 링크 동작 확인
  - ✅ ReportGenerator 통합 테스트

**산출물**:
- Markdown → HTML 렌더러 완성 (308줄)
- QTextBrowser 결과 패널 완성 (268줄)
- GitHub Dark 스타일 CSS 완성
- 종합 테스트 스크립트 (test_markdown_rendering.py)

**완료일**: 2025-01-14

---

#### Day 8 (2025-01-15): Mermaid 다이어그램 PNG 변환
**목표**: 플로우 다이어그램 시각화

**Tasks**:
- ✅ Mermaid CLI 설치
  - ✅ npm install -g @mermaid-js/mermaid-cli (v11.12.0)
  - ✅ mmdc 명령어 확인
- ✅ `app/core/diagram_converter.py` 구현
  - ✅ Mermaid 코드 추출 (Markdown에서)
  - ✅ 임시 .mmd 파일 생성
  - ✅ mmdc 명령어 실행 (subprocess)
  - ✅ PNG 이미지 생성
  - ✅ 이미지 Base64 인코딩
  - ✅ Markdown에 이미지 삽입 (<img src="data:image/png;base64,...">)
- ✅ 에러 처리
  - ✅ mmdc 실행 실패 시 텍스트 폴백
  - ✅ 타임아웃 설정 (10초)
- ✅ 테스트
  - ✅ 간단한 플로우차트 생성 확인
  - ✅ 복잡한 다이어그램 테스트 (시퀀스, 클래스 다이어그램)
  - ✅ 에러 처리 테스트 (잘못된 문법)
- ✅ MainWindow 통합
  - ✅ ResultPanel 추가 (QSplitter로 레이아웃)
  - ✅ 리포트 자동 생성 및 표시

**산출물**:
- Mermaid → PNG 변환기 완성 (243줄)
- 다이어그램 표시 확인 (Base64 임베딩)
- 에러 핸들링 구현 (폴백 처리)
- 종합 테스트 스크립트 (test_diagram_converter.py, 6개 테스트 모두 통과)
- MainWindow에 ResultPanel 통합

**완료일**: 2025-01-15

---

#### Day 8.5 (2025-01-15): XML 문서 주석 자동 생성
**목표**: C# XML 문서 주석 자동 생성 기능 추가

**Tasks**:
- ✅ ReviewCategory에 CODE_DOCUMENTATION 추가
- ✅ PromptBuilder에 XML 주석 규칙 추가
  - ✅ `<summary>`: 한 줄 요약
  - ✅ `<param>`: 매개변수 설명
  - ✅ `<returns>`: 반환값 설명
  - ✅ `<exception>`: 발생 가능한 예외
  - ✅ `<remarks>`: 상세 설명 (옵션)
  - ✅ `<example>`: 사용 예제 (옵션)
- ✅ Few-shot 예제 추가
  - ✅ 클래스 주석 예제
  - ✅ 메서드 주석 예제
- ✅ MainWindow categories에 CODE_DOCUMENTATION 추가
- ✅ ReportGenerator에 카테고리 이름 추가

**XML 주석 템플릿**:
```csharp
/// <summary>
/// TODO: 한 줄 요약 — 이 메서드가 하는 일
/// </summary>
/// <param name="param1">TODO: param1 설명</param>
/// <param name="param2">TODO: param2 설명 (옵션/범위 등)</param>
/// <returns>TODO: 반환값 설명</returns>
/// <exception cref="ArgumentNullException">param1이 null인 경우</exception>
/// <remarks>
/// TODO: 상세 설명 (부작용, 복잡도, 참고할 점 등)
/// </remarks>
public ReturnType MethodName(Type param1, Type param2) { ... }
```

**산출물**:
- 7번째 리뷰 카테고리 추가 (총 7개)
- XML 문서 주석 자동 생성 기능
- Few-shot 예제 (UserService 클래스)

**완료일**: 2025-01-15

---

#### Day 9 (2025-01-16): Markdown 기반 리뷰 규칙 관리 시스템
**목표**: 리뷰 규칙을 Markdown 파일로 외부화하여 유지보수성 향상

**Tasks**:
- ✅ Markdown 파일 기반 카테고리 시스템 설계
  - ✅ `resources/templates/review_categories/` 디렉토리 생성
  - ✅ 7개 카테고리 Markdown 파일 작성
    - ✅ `code_documentation.md` (8가지 케이스: 클래스, 메서드, 프로퍼티, 인터페이스, Enum, Delegate, Event, Generic)
    - ✅ `null_reference.md` (Null 참조 체크)
    - ✅ `exception_handling.md` (Exception 처리)
    - ✅ `resource_management.md` (리소스 관리)
    - ✅ `performance.md` (성능 최적화)
    - ✅ `security.md` (보안)
    - ✅ `naming_convention.md` (네이밍 컨벤션)
- ✅ `app/utils/markdown_parser.py` 구현 (231줄)
  - ✅ `ReviewCategoryParser` 클래스
    - ✅ `_extract_title()`: # 제목 추출
    - ✅ `_extract_description()`: ## 설명 섹션 추출
    - ✅ `_extract_rules()`: ## 규칙 리스트 추출
    - ✅ `_extract_examples()`: Before/After 예제 추출
  - ✅ `CategoryLoader` 클래스
    - ✅ `load_all()`: 모든 카테고리 파일 로드
    - ✅ `load_category()`: 특정 카테고리 파일 로드
- ✅ `app/core/prompt_builder.py` 리팩토링
  - ✅ `__init__(use_markdown=True)` 파라미터 추가
  - ✅ `_build_templates_from_markdown()` 메서드 추가
  - ✅ `_build_examples_from_markdown()` 메서드 추가
  - ✅ `build_review_prompt()` 메서드 수정 (동적 템플릿 사용)
  - ✅ 하드코딩 모드 호환성 유지 (use_markdown=False)
- ✅ 통합 테스트
  - ✅ test_markdown_integration.py 작성
  - ✅ 7개 카테고리 로드 확인
  - ✅ 프롬프트 생성 테스트 (1967자)
  - ✅ 하드코딩 모드 호환성 테스트

**Markdown 파일 구조**:
```markdown
# 카테고리 이름

## 설명
카테고리 설명 텍스트

## 규칙
- 규칙 1
- 규칙 2
- 규칙 3

## Before 예제
```csharp
// 개선 전 코드
```

## After 예제
```csharp
// 개선 후 코드
```
```

**산출물**:
- 7개 Markdown 카테고리 파일 (총 50개 이상의 규칙, 8개 예제 케이스)
- Markdown 파서 구현 (231줄)
- PromptBuilder 동적 로딩 시스템
- 통합 테스트 스크립트 (모든 테스트 통과)

**주요 개선 사항**:
- ✅ **유지보수성**: 리뷰 규칙을 코드 수정 없이 Markdown 파일로 관리
- ✅ **확장성**: 새로운 케이스 추가 시 Markdown 파일만 수정
- ✅ **가독성**: 규칙과 예제를 구조화된 형식으로 관리
- ✅ **협업**: 비개발자도 Markdown 파일 편집 가능
- ✅ **버전 관리**: Markdown diff로 규칙 변경 이력 추적 용이

**완료일**: 2025-01-16

---

### Week 3: 파일 업로드 모드 (Day 10-12)

#### Day 10 (2025-01-17): 파일 선택 UI 및 드래그 앤 드롭
**목표**: 파일 업로드 인터페이스 구현

**Tasks**:
- ✅ `app/ui/file_upload_widget.py` 구현 (600+ lines)
  - ✅ QListWidget (파일 목록 표시)
  - ✅ "파일 추가" 버튼 (QFileDialog)
  - ✅ "선택 제거" / "전체 제거" 버튼
  - ✅ 파일 카운터 (총 N개 파일)
- ✅ 드래그 앤 드롭 지원
  - ✅ dragEnterEvent 오버라이드
  - ✅ dropEvent 오버라이드
  - ✅ `.cs` 파일만 필터링
  - ✅ 드롭 영역 하이라이팅 (파란색 강조)
- ✅ 파일 검증
  - ✅ 파일 존재 여부 확인
  - ✅ 파일 크기 제한 (최대 1MB)
  - ✅ UTF-8 인코딩 확인
  - ✅ 중복 파일 체크
- ✅ UI 개선
  - ✅ 파일 아이콘 표시 (📄)
  - ✅ 파일 크기 표시 (자동 포맷팅: B/KB/MB/GB)
  - ✅ 더블클릭 시 미리보기 (FilePreviewDialog)
  - ✅ 툴팁에 전체 경로 표시
  - ✅ VS Code Dark 테마 스타일
- ✅ MainWindow 통합
  - ✅ QTabWidget으로 "텍스트 입력" / "파일 업로드" 모드 전환
  - ✅ Import 추가 및 레이아웃 수정
- ✅ 테스트
  - ✅ tests/test_file_upload_widget.py 작성 (13개 테스트)
  - ✅ 단위 테스트 (FileUploadWidget, FileListWidget)
  - ✅ 통합 테스트 (전체 워크플로우)
  - ✅ 모든 테스트 통과 (13/13)

**산출물**:
- ✅ FileUploadWidget 완성 (600+ lines)
  - FileListWidget: 드래그 앤 드롭 지원 리스트
  - FilePreviewDialog: 파일 미리보기 다이얼로그
  - 파일 검증 로직 (크기, 인코딩, 확장자)
- ✅ MainWindow 탭 통합
- ✅ 13개 단위/통합 테스트 (100% 통과)
- ✅ 테스트용 C# 파일 3개 (test_files/)

**주요 기능**:
- 📂 **파일 추가**: QFileDialog 또는 드래그 앤 드롭
- 🗑️ **파일 제거**: 선택 제거 / 전체 제거
- 🔍 **파일 검증**: .cs 확장자, 1MB 이하, UTF-8 인코딩
- 📄 **파일 미리보기**: 더블클릭으로 코드 내용 확인
- 🎨 **UX**: 파일 크기 표시, 드래그 시 배경 강조, 플레이스홀더

**완료일**: 2025-01-17

---

#### Day 11 (2025-01-18): 다중 파일 분석 및 프로그레스바 ✅
**목표**: 여러 파일 순차 분석 및 진행 상태 표시

**Tasks**:
- [x] 다중 파일 분석 로직
  - [x] 파일 목록 순회
  - [x] 각 파일 읽기 (UTF-8)
  - [x] LLM 호출 (파일별)
  - [x] After 코드 및 리포트 생성
- [x] 프로그레스 다이얼로그
  - [x] QProgressDialog 사용
  - [x] 진행률 표시 (N/M 파일)
  - [x] 현재 파일명 표시
  - [x] "취소" 버튼 (분석 중단)
- [x] 에러 복구
  - [x] 파일 읽기 실패 시 스킵
  - [x] LLM 오류 시 재시도 (최대 3회, 1초 간격)
  - [x] 에러 로그 기록 (콘솔 출력)
- [x] 결과 집계
  - [x] 성공/실패/건너뜀 파일 개수
  - [x] 총 소요 시간
  - [x] 요약 다이얼로그 표시 (파일별 상세 결과 포함)
  - [x] 성공 결과 일괄 저장 기능

**산출물**:
- ✅ `app/core/batch_analyzer.py` - BatchAnalyzer 클래스 (320줄)
  - FileAnalysisResult, BatchAnalysisResult 데이터클래스
  - 재시도 로직 (MAX_RETRIES=3), 에러 복구, 진행률 콜백
- ✅ `app/ui/main_window.py` - 다중 파일 분석 통합
  - `_analyze_multiple_files()` 메서드 (106줄)
  - `_show_batch_results_dialog()` 메서드 (73줄)
  - `_save_batch_results()` 메서드 (63줄)
- ✅ `tests/test_batch_analyzer.py` - 단위 테스트 (345줄)
  - 10개 테스트 케이스 (모두 통과)
  - 재시도 로직, 취소 기능, 프로그레스 콜백 검증

**마지막 업데이트**: 2025-01-18

---

#### Day 12 (2025-01-19): 파일별 리포트 생성 및 관리 ✅
**목표**: 파일별 개별 리포트 저장 및 히스토리 관리

**Tasks**:
- [x] 파일별 리포트 생성
  - [x] 파일명 기반 리포트명 ({파일명}_review_{YYYYMMDD_HHMMSS}.md)
  - [x] 자동 저장 경로 (./reports/markdown/, ./reports/html/)
  - [x] Markdown + HTML 동시 저장
- [x] 리포트 히스토리
  - [x] SQLite DB 생성 (reports/reports.db)
  - [x] 테이블 스키마 (id, filename, report_name, timestamp, markdown_path, html_path, success, error_message, analysis_time)
  - [x] 리포트 목록 조회 (get_all_reports, get_reports_by_filename, get_report_by_id)
  - [x] 통계 조회 (get_statistics)
- [x] 히스토리 UI
  - [x] View 메뉴에 "📜 리포트 히스토리" 추가 (Ctrl+H)
  - [x] QTableWidget으로 리포트 목록 표시 (ID, 파일명, 생성 시간, 상태, 분석 시간, 경로)
  - [x] 더블클릭 시 HTML 리포트 브라우저에서 열기
  - [x] 삭제 기능 (DB 레코드 + 파일)
  - [x] 새로고침 버튼
  - [x] 통계 정보 표시
- [x] 자동 저장 통합
  - [x] 단일 파일 분석 후 자동 저장
  - [x] 배치 분석 후 성공한 파일들 자동 저장
  - [x] 저장 결과 사용자에게 알림
- [x] 테스트
  - [x] ReportHistoryDB 테스트 (8개 테스트, 모두 통과)
  - [x] ReportSaver 테스트 (8개 테스트, 모두 통과)

**산출물**:
- ✅ `app/db/report_history.py` - ReportHistoryDB 클래스 (320줄)
  - ReportRecord 데이터클래스
  - CRUD 작업 (add, get, delete), 통계 조회
- ✅ `app/services/report_saver.py` - ReportSaver 클래스 (240줄)
  - save_report() 메서드 (MD + HTML 저장)
  - Markdown → HTML 변환 (VS Code Dark 테마 스타일)
  - 타임스탬프 기반 파일명 생성
- ✅ `app/ui/main_window.py` - 자동 저장 및 히스토리 UI 통합
  - ReportSaver 초기화
  - 단일/배치 분석 후 자동 저장
  - `_on_show_report_history()` 메서드 (163줄)
- ✅ `tests/test_report_history.py` - 단위 테스트 (185줄)
  - 8개 테스트 케이스 (모두 통과)
- ✅ 디렉토리 구조:
  - reports/markdown/ (Markdown 리포트 저장)
  - reports/html/ (HTML 리포트 저장)
  - reports/reports.db (SQLite 데이터베이스)

**마지막 업데이트**: 2025-01-19

---

### Week 4: 폴더 선택 모드 (Day 13-15)

#### Day 13 (2025-01-20): 트리 구조 UI 및 재귀 탐색 ✅ **완료**
**목표**: 폴더 구조를 트리로 표시

**Tasks**:
- [x] `app/ui/folder_select_widget.py` 구현
  - [x] QTreeView 초기화
  - [x] "폴더 선택" 버튼 (QFileDialog)
  - [x] 트리 모델 생성 (QStandardItemModel)
  - [x] 체크박스 항목 (Qt.ItemIsUserCheckable)
- [x] 재귀 탐색 로직
  - [x] os.walk() 사용
  - [x] `.cs` 파일만 필터링
  - [x] 숨김 폴더 제외 (.git, .vs, bin, obj)
  - [x] 파일 개수 카운팅
- [x] 트리 UI 개선
  - [x] 폴더 아이콘/파일 아이콘
  - [x] 확장/축소 애니메이션
  - [x] "전체 선택" / "전체 해제" 버튼
- [x] 테스트
  - [x] 중첩된 폴더 구조 표시 확인
  - [x] 체크박스 선택 동작 확인

**산출물**:
- ✅ 폴더 선택 위젯 완성 (app/ui/folder_select_widget.py)
- ✅ 재귀 탐색 로직 구현 (_scan_folder, _build_tree_recursive)
- ✅ 트리 UI 동작 확인 (test_folder_select_widget.py)

**구현 내역**:
- 637줄 완전 구현 (QTreeView, QStandardItemModel, 체크박스, 시그널)
- 제외 폴더: .git, .vs, .vscode, bin, obj, node_modules, packages
- 최대 100개 파일 제한
- 실시간 선택 개수 표시
- 부모/자식 간 체크 상태 연동 (PartiallyChecked 지원)
- files_changed 시그널로 외부 통합 준비 완료

---

#### Day 14 (2025-01-21): 대용량 프로젝트 처리 및 배치 분석
**목표**: 많은 파일을 효율적으로 처리

**Tasks**:
- [ ] 파일 개수 제한
  - [ ] 50개 초과 시 경고 다이얼로그
  - [ ] "그래도 계속" / "취소" 선택
  - [ ] 선택된 파일 개수 표시
- [ ] 배치 처리
  - [ ] 10개씩 묶어서 분석
  - [ ] 배치 간 1초 대기 (LLM 과부하 방지)
  - [ ] 프로그레스바 업데이트 (배치별)
- [ ] 메모리 관리
  - [ ] 분석 완료된 파일 메모리 해제
  - [ ] 대용량 파일 (>500KB) 경고
- [ ] 성능 최적화
  - [ ] 비동기 파일 읽기 (QThread)
  - [ ] LLM 응답 캐싱 (동일 코드 재분석 방지)

**산출물**:
- 대용량 프로젝트 처리 로직 완성
- 배치 처리 동작 확인
- 메모리 사용량 측정

---

#### Day 15 (2025-01-22): 통합 리포트 및 Week 4 마무리 ✅ **완료**
**목표**: 프로젝트 전체 요약 리포트 생성

**Tasks**:
- [x] 통합 리포트 생성
  - [x] 프로젝트명 및 분석 시각
  - [x] 전체 파일 개수 (성공/실패)
  - [x] 카테고리별 이슈 통계
    - Null 참조: N건
    - Exception: N건
    - 리소스 해제: N건
    - 성능: N건
    - 보안: N건
    - 네이밍: N건
  - [x] 파일별 상세 리포트 링크 (파일명 목록)
  - [x] 개선 우선순위 권장 (가중치 기반)
- [x] 통합 리포트 차트
  - [x] 차트 생성 (matplotlib)
  - [x] 카테고리별 이슈 분포 (원형 차트)
  - [ ] "프로젝트 요약" 탭 추가 (UI 통합은 Day 14)
- [x] 테스트
  - [x] 20개 파일 프로젝트 분석 (모의 데이터)
  - [x] 통합 리포트 생성 확인 (Markdown)
  - [x] 차트 렌더링 확인 (PNG)

**산출물**:
- ✅ 통합 리포트 생성기 완성 (app/core/integrated_report_generator.py)
- ✅ 카테고리별 이슈 통계 분석 (CategoryStatistics)
- ✅ 우선순위 권장 알고리즘 (가중치: 보안 10, 리소스 관리 9, Exception 8...)
- ✅ matplotlib 차트 생성 (원형 차트, 한글 지원)
- ✅ 테스트 스크립트 (test_integrated_report.py)

**구현 내역**:
- IntegratedReportGenerator 클래스 (440줄)
  - generate_integrated_report(): Markdown 리포트 생성
  - _analyze_category_statistics(): 카테고리별 통계 분석
  - _generate_priority_recommendations(): 우선순위 알고리즘
  - generate_chart(): matplotlib 원형 차트 생성
- 카테고리별 가중치 시스템 (보안 > 리소스 > Exception > Null > ...)
- 퍼센티지 바 생성 (█░ 그래프)
- 테이블 형식 통계 출력
- matplotlib 의존성 추가 (requirements.txt)

---

### Week 5: 포터블 패키징 (Day 16-18)

#### Day 16 (2025-01-23): PyInstaller EXE 빌드 ✅
**목표**: Python 스크립트를 단일 EXE로 패키징

**Tasks**:
- [x] PyInstaller 설정
  - [x] `pip install pyinstaller` (requirements.txt에 포함)
  - [x] spec 파일 생성 (`CodeReviewer.spec`)
- [x] spec 파일 수정
  - [x] --onefile 옵션 (단일 EXE)
  - [x] --windowed 옵션 (콘솔 숨김)
  - [x] --icon 옵션 (TODO로 표시, 향후 추가 예정)
  - [x] --add-data (리소스 파일 포함: styles, templates)
  - [x] --exclude-module (불필요 모듈 제외: tkinter, tests, PIL, scipy, pandas)
- [x] 빌드 스크립트 작성
  - [x] scripts/build_exe.py (213줄)
  - [x] UPX 압축 활성화 (upx=True)
  - [x] 서명 (TODO로 표시, 향후 추가 예정)
- [x] 테스트 스크립트
  - [x] scripts/test_exe.py (171줄)
  - [x] 4가지 테스트 (파일 존재, Ollama 체크, 리소스 확인, 실행 테스트)
- [x] 문서화
  - [x] docs/BUILD_GUIDE.md (345줄 - 빌드 가이드)

**산출물**:
- ✅ `CodeReviewer.spec` - PyInstaller 설정 파일 (87줄)
  - PySide6, matplotlib, ollama 등 hiddenimports 설정
  - 리소스 파일 번들링 설정
  - UPX 압축 활성화
  - console=False (GUI 모드)
- ✅ `scripts/build_exe.py` - 자동화 빌드 스크립트 (213줄)
  - 사전 체크 (spec 파일, entry point, 리소스 존재 확인)
  - 빌드 아티팩트 정리 (--clean 옵션)
  - PyInstaller 실행
  - 사후 검증 (EXE 파일, 크기 확인)
- ✅ `scripts/test_exe.py` - EXE 테스트 스크립트 (171줄)
  - 파일 존재 및 크기 확인
  - Ollama 서버 접근 확인
  - 리소스 번들 확인
  - EXE 실행 테스트
- ✅ `docs/BUILD_GUIDE.md` - 빌드 가이드 문서 (345줄)
  - 빌드 전 체크리스트
  - 빌드 프로세스 설명
  - 트러블슈팅 가이드
  - 최적화 팁
  - 배포 가이드

**빌드 사용법**:
```bash
# 기본 빌드
python scripts/build_exe.py

# 클린 빌드 (이전 빌드 아티팩트 삭제 후)
python scripts/build_exe.py --clean

# 디버그 빌드 (콘솔 창 표시)
python scripts/build_exe.py --debug

# EXE 테스트
python scripts/test_exe.py
```

**예상 EXE 크기**:
- 압축 전: ~100-150 MB
- UPX 압축 후: ~50-100 MB

**다음 단계**: Day 17 - Ollama 포터블 번들링

**마지막 업데이트**: 2025-01-19

---

#### Day 17 (2025-01-24): Ollama 포터블 번들링 ✅
**목표**: Ollama + Phi-3-mini를 포터블 패키지에 포함

**Tasks**:
- [x] Ollama 포터블 버전 준비
  - [x] Ollama Windows 바이너리 다운로드 가이드
  - [x] ollama.exe 추출 가이드
  - [x] 모델 파일 경로 설정 (OLLAMA_MODELS 환경 변수)
- [x] 모델 파일 번들링
  - [x] Phi-3-mini GGUF 파일 다운로드 가이드
  - [x] ollama_portable/models/ 폴더 구조
  - [x] Modelfile 생성 가이드
- [x] 자동 실행 스크립트
  - [x] scripts/bundle_ollama.py (400줄)
  - [x] app/services/ollama_manager.py (260줄)
  - [x] CodeReviewer.exe 실행 시 Ollama 자동 시작
  - [x] 백그라운드 실행 (subprocess.Popen, 콘솔 숨김)
  - [x] 종료 시 Ollama 프로세스 종료 (graceful + force kill)
- [x] 환경 변수 설정
  - [x] OLLAMA_MODELS 경로 자동 설정
  - [x] OLLAMA_HOST 설정 (localhost:11434)
  - [x] 포터블 모드 자동 감지
- [x] 통합 및 테스트
  - [x] app/main.py에 OllamaManager 통합
  - [x] 시작 메시지 다이얼로그
  - [x] 로깅 시스템 (logs/app.log)
  - [x] 정상 종료 시 cleanup 훅

**산출물**:
- ✅ `app/services/ollama_manager.py` - Ollama 프로세스 관리자 (260줄)
  - is_running(): 서버 상태 확인
  - has_model(): 모델 존재 확인
  - start(): 포터블/시스템 Ollama 시작 (Windows 콘솔 숨김)
  - _wait_for_ready(): 30초 타임아웃으로 Ready 대기
  - stop(): graceful shutdown (5초 타임아웃 후 force kill)
  - Context manager 지원

- ✅ `scripts/bundle_ollama.py` - 포터블 패키지 번들러 (400줄)
  - 디렉토리 구조 자동 생성
  - ollama.exe 준비 가이드
  - Phi-3-mini 모델 준비 가이드
  - README.txt 자동 생성
  - settings.json 자동 생성
  - 번들 검증 및 크기 계산

- ✅ `app/main.py` - Ollama 자동 시작 통합 (178줄)
  - 포터블 Ollama 자동 감지 (EXE/스크립트 모드)
  - "Starting Ollama..." 다이얼로그
  - OllamaManager 통합 (시작/종료)
  - 실패 시 사용자 알림
  - 로깅 시스템

- ✅ `docs/PORTABLE_GUIDE.md` - 포터블 배포 가이드 (600줄)
  - 완전한 번들링 프로세스 (Step 1-6)
  - Ollama 바이너리 추출 가이드
  - Phi-3-mini 모델 복사 가이드
  - Modelfile 생성 방법
  - VDI 배포 체크리스트
  - 트러블슈팅 (5가지 문제)
  - 성능 튜닝 및 유지보수

- ✅ logs/ 디렉토리 생성
- ✅ requirements.txt - requests 의존성 추가

**사용법**:
```bash
# 포터블 패키지 생성
python scripts/bundle_ollama.py --output-dir CodeReviewer_Portable

# 수동 파일 복사 후 검증
python scripts/bundle_ollama.py --output-dir CodeReviewer_Portable
```

**주요 기능**:
- 포터블 모드 자동 감지
- 자동 시작/종료
- Windows 콘솔 숨김
- Graceful shutdown
- Health check (30초 타임아웃)

**다음 단계**: Day 18 - 설치 없는 실행 테스트

**마지막 업데이트**: 2025-01-19

---

#### Day 18 (2025-01-25): 설치 없는 실행 테스트 및 최적화
**목표**: 완전한 포터블 패키지 검증

**Tasks**:
- [ ] 포터블 패키지 구조 확인
  ```
  CodeReviewer_Portable/
  ├── CodeReviewer.exe
  ├── ollama_portable/
  │   ├── ollama.exe
  │   └── models/
  │       └── phi3-mini.gguf
  ├── config/
  │   └── settings.json
  ├── logs/
  └── README.txt
  ```
- [ ] 다양한 VDI 환경 테스트
  - [ ] Windows 11 (64-bit)
  - [ ] 관리자 권한 없는 계정
  - [ ] 방화벽 활성화 환경
  - [ ] 인터넷 연결 차단 환경
- [ ] 성능 최적화
  - [ ] EXE 압축 (UPX)
  - [ ] 리소스 파일 최소화
  - [ ] 초기 로딩 시간 단축
- [ ] 에러 복구 테스트
  - [ ] Ollama 실행 실패 시 재시도
  - [ ] 모델 로드 실패 시 안내 메시지
  - [ ] 포트 충돌 시 대체 포트 사용
- [ ] README.txt 작성
  - [ ] 빠른 시작 가이드
  - [ ] 문제 해결 (Troubleshooting)
  - [ ] 시스템 요구사항

**산출물**:
- 최종 포터블 패키지 (약 2.5GB, 압축 시 1.5GB)
- VDI 환경 테스트 완료
- README.txt 작성

---

### Week 6: 테스트 및 최적화 (Day 19-22)

#### Day 19 (2025-01-26): 단위 테스트 (Pytest)
**목표**: 핵심 모듈 단위 테스트 작성

**Tasks**:
- [ ] Pytest 설정
  - [ ] `pip install pytest pytest-qt pytest-cov`
  - [ ] pytest.ini 설정
- [ ] 단위 테스트 작성
  - [ ] tests/test_ollama_client.py (LLM 통신)
  - [ ] tests/test_prompt_builder.py (프롬프트 생성)
  - [ ] tests/test_report_generator.py (리포트 생성)
  - [ ] tests/test_diagram_converter.py (Mermaid 변환)
  - [ ] tests/test_syntax_highlighter.py (하이라이팅)
- [ ] Mock 객체 사용
  - [ ] unittest.mock.Mock
  - [ ] LLM 응답 Mock
  - [ ] 파일 시스템 Mock
- [ ] 커버리지 측정
  - [ ] pytest --cov=app --cov-report=html
  - [ ] 목표: >80% 커버리지
- [ ] 테스트 실행
  - [ ] pytest -v
  - [ ] 모든 테스트 통과 확인

**산출물**:
- 단위 테스트 30개+ 작성
- 코드 커버리지 >80%
- 테스트 리포트 (HTML)

---

#### Day 20 (2025-01-27): 통합 테스트 및 VDI 환경 테스트
**목표**: 전체 워크플로우 통합 테스트

**Tasks**:
- [ ] 통합 테스트 시나리오
  - [ ] Scenario 1: 텍스트 입력 → 분석 → 리포트 생성
  - [ ] Scenario 2: 파일 업로드 → 다중 분석 → 리포트 저장
  - [ ] Scenario 3: 폴더 선택 → 배치 분석 → 통합 리포트
- [ ] E2E 테스트 (pytest-qt)
  - [ ] UI 이벤트 시뮬레이션
  - [ ] 버튼 클릭, 텍스트 입력
  - [ ] 다이얼로그 자동 응답
- [ ] VDI 환경 테스트
  - [ ] 실제 VDI에 포터블 패키지 배포
  - [ ] 더블클릭 실행 확인
  - [ ] 100줄 코드 분석 시간 측정
  - [ ] 메모리 사용량 측정
- [ ] 성능 벤치마크
  - [ ] 10줄: <2초
  - [ ] 100줄: <5초
  - [ ] 500줄: <20초

**산출물**:
- 통합 테스트 10개 작성
- VDI 환경 테스트 리포트
- 성능 벤치마크 데이터

---

#### Day 21 (2025-01-28): 성능 최적화 및 메모리 관리
**목표**: 응답 속도 및 메모리 사용량 최적화

**Tasks**:
- [ ] LLM 응답 속도 개선
  - [ ] 프롬프트 토큰 수 감소
  - [ ] 스트리밍 응답 활성화
  - [ ] 캐싱 적용 (동일 코드 재분석 방지)
- [ ] 메모리 사용량 감소
  - [ ] 대용량 파일 청크 단위 읽기
  - [ ] 분석 완료 후 메모리 해제
  - [ ] QThread 종료 시 리소스 정리
- [ ] UI 응답성 개선
  - [ ] 분석 중 UI 프리즈 방지 (QThread)
  - [ ] 프로그레스바 실시간 업데이트
  - [ ] 취소 버튼 즉시 반응
- [ ] 프로파일링
  - [ ] cProfile 사용
  - [ ] 병목 구간 확인
  - [ ] 최적화 전/후 비교

**산출물**:
- 응답 시간 20% 감소
- 메모리 사용량 30% 감소
- 프로파일링 리포트

---

#### Day 22 (2025-01-29): 문서화 및 사용자 가이드 작성
**목표**: 최종 문서 작성 및 프로젝트 완료

**Tasks**:
- [ ] `README.md` 최종 업데이트
  - [ ] 프로젝트 소개
  - [ ] 주요 기능 (스크린샷)
  - [ ] 시스템 요구사항
  - [ ] 빠른 시작 가이드
  - [ ] 다운로드 링크
- [ ] `docs/USER_GUIDE.md` 작성
  - [ ] "처음 사용자" 튜토리얼
  - [ ] 주요 기능 설명
  - [ ] 키보드 단축키
  - [ ] FAQ
- [ ] `docs/TECHNICAL_SPECIFICATION.md` 작성
  - [ ] 아키텍처 다이어그램
  - [ ] 프롬프트 템플릿 상세
  - [ ] API 레퍼런스
- [ ] `docs/TROUBLESHOOTING.md` 작성
  - [ ] Ollama 실행 실패
  - [ ] 모델 로드 오류
  - [ ] 메모리 부족 에러
- [ ] 라이선스 파일 추가 (LICENSE.md)
  - [ ] MIT License
- [ ] GitHub 저장소 공개 (선택적)
- [ ] **Week 6 완료 리포트 작성**

**산출물**:
- 완전한 문서화 (5개 문서)
- 사용자 가이드 완성
- 프로젝트 완료 🎉

---

## 마일스톤 요약

| 주차 | 기간 | 목표 | 완료 기준 |
|------|------|------|-----------|
| **Week 1** | Day 1-4 | 기본 구조 및 LLM 통합 | ✅ Ollama 연동, Before/After 에디터 동작 |
| **Week 2** | Day 5-9 | 코드 분석 엔진 + Markdown 관리 | ✅ 7가지 리뷰 항목, Markdown 리포트, 규칙 외부화 |
| **Week 3** | Day 10-12 | 파일 업로드 모드 | 🔜 다중 파일 분석, 프로그레스바 |
| **Week 4** | Day 13-15 | 폴더 선택 모드 | 🔜 트리 UI, 통합 리포트 |
| **Week 5** | Day 16-18 | 포터블 패키징 | 🔜 EXE + Ollama 번들, VDI 실행 |
| **Week 6** | Day 19-22 | 테스트 및 문서화 | 🔜 단위 테스트 >80%, 사용자 가이드 |

---

## 위험 관리 및 대응책

### 일정 지연 대응
- **Week 1-2 지연**: Phase 2-3 제외, MVP만 완성
- **Week 3-4 지연**: 폴더 선택 기능 제외
- **Week 5 패키징 이슈**: Python 스크립트 배포

### 기술적 문제 대응
- **Ollama 포터블 실행 실패**: llama-cpp-python으로 전환
- **PyInstaller 번들 과대**: 의존성 최소화, UPX 압축
- **Phi-3-mini 성능 부족**: 프롬프트 최적화, 양자화 조정
- **QTextBrowser 제약**: QWebEngineView로 전환 (선택적)

---

**마지막 업데이트**: 2025-01-16
**다음 리뷰**: Week 3 시작 전 (Day 10)
**프로젝트 완료 목표**: 2025-02-19 (6주 후, Day 9 추가로 인한 +1일)
