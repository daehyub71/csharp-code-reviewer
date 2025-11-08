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

#### Day 2 (2025-01-09): Ollama 통합 및 Phi-3-mini 테스트
**목표**: LLM 백엔드 설정 및 동작 확인

**Tasks**:
- [ ] Ollama 설치 및 실행
  - [ ] `ollama pull phi3:mini` 모델 다운로드 (2.3GB)
  - [ ] `ollama serve` 백그라운드 실행 확인
- [ ] `app/core/ollama_client.py` 구현
  - [ ] Ollama Python SDK 초기화
  - [ ] 연결 테스트 함수
  - [ ] 프롬프트 전송 함수
  - [ ] 스트리밍 응답 처리
  - [ ] 에러 핸들링
- [ ] 테스트 스크립트 작성
  - [ ] 간단한 C# 코드 샘플
  - [ ] LLM 응답 확인 (Hello World 코드 리뷰)
- [ ] 성능 벤치마크
  - [ ] 100줄 코드 분석 시간 측정
  - [ ] 메모리 사용량 확인

**산출물**:
- Ollama 클라이언트 완성
- LLM 응답 시간 데이터 (목표: <5초)
- 연결 테스트 통과

---

#### Day 3 (2025-01-10): PySide6 기본 UI 및 Before/After 에디터
**목표**: 메인 윈도우 및 코드 에디터 구현

**Tasks**:
- [ ] `app/main.py` 작성
  - [ ] PySide6 QApplication 초기화
  - [ ] 메인 윈도우 생성
  - [ ] 이벤트 루프 실행
- [ ] `app/ui/main_window.py` 구현
  - [ ] 메인 윈도우 레이아웃
  - [ ] 메뉴바 (파일, 편집, 도움말)
  - [ ] 툴바 (분석 시작, 설정)
  - [ ] 상태바 (Ollama 상태 표시)
- [ ] `app/ui/before_after_editor.py` 구현
  - [ ] QPlainTextEdit 기반 코드 에디터
  - [ ] Before 에디터 (사용자 입력)
  - [ ] After 에디터 (읽기 전용)
  - [ ] Vertical Splitter (50:50 분할)
  - [ ] 복사 버튼 (Before/After 각각)
- [ ] 기본 스타일링
  - [ ] resources/styles/dark_theme.qss 작성
  - [ ] 폰트 설정 (Consolas, Monaco)

**산출물**:
- 메인 윈도우 UI 완성
- Before/After 에디터 동작 확인
- 기본 다크 테마 적용

---

#### Day 4 (2025-01-11): Syntax Highlighting 및 동기화 스크롤
**목표**: 코드 가독성 향상 및 UX 개선

**Tasks**:
- [ ] `app/utils/syntax_highlighter.py` 구현
  - [ ] QSyntaxHighlighter 상속
  - [ ] C# 키워드 정의 (class, public, void, if, etc.)
  - [ ] 정규식 기반 토큰 파싱
  - [ ] 색상 스키마 정의
    - 키워드: #569CD6 (파란색)
    - 문자열: #CE9178 (주황색)
    - 주석: #6A9955 (초록색)
    - 숫자: #B5CEA8 (연두색)
- [ ] Syntax Highlighter 적용
  - [ ] Before/After 에디터에 연결
  - [ ] 실시간 하이라이팅 확인
- [ ] 동기화 스크롤 구현
  - [ ] Before 에디터 스크롤 이벤트 감지
  - [ ] After 에디터 스크롤 위치 동기화
  - [ ] 토글 버튼 (동기화 ON/OFF)
- [ ] 추가 기능
  - [ ] 라인 번호 표시
  - [ ] 현재 줄 하이라이팅
  - [ ] Ctrl+A 전체 선택 단축키

**산출물**:
- C# Syntax Highlighting 완성
- 동기화 스크롤 동작 확인
- 사용자 친화적 에디터 완성

---

### Week 2: 코드 분석 엔진 (Day 5-8)

#### Day 5 (2025-01-12): Prompt Builder 및 6가지 리뷰 항목
**목표**: LLM 프롬프트 설계 및 최적화

**Tasks**:
- [ ] `app/core/prompt_builder.py` 구현
  - [ ] 프롬프트 템플릿 정의
  - [ ] 6가지 리뷰 항목 템플릿
    1. Null 참조 체크
    2. Exception 처리 누락
    3. 리소스 해제
    4. 성능 이슈
    5. 보안 취약점
    6. 네이밍 컨벤션
  - [ ] 코드 주석 생성 템플릿
  - [ ] 플로우 다이어그램 템플릿
- [ ] 프롬프트 변수 치환
  - [ ] `{user_code}` → 실제 C# 코드
  - [ ] `{review_options}` → 체크박스 선택 항목
- [ ] 프롬프트 최적화
  - [ ] 토큰 수 최소화 (목표: <1500 토큰)
  - [ ] Few-shot 예제 추가
- [ ] 테스트
  - [ ] 샘플 코드 5개로 프롬프트 생성 확인

**산출물**:
- 프롬프트 템플릿 완성
- 토큰 사용량 분석 (목표 <1500)
- Few-shot 예제 3개 작성

---

#### Day 6 (2025-01-13): Report Generator 및 Markdown 생성
**목표**: LLM 응답을 Markdown 리포트로 변환

**Tasks**:
- [ ] `app/core/report_generator.py` 구현
  - [ ] LLM 응답 파싱
  - [ ] Markdown 구조화
    - 요약 섹션 (발견 이슈 개수)
    - 이슈별 상세 (심각도, 위치, 개선 코드)
    - 플로우 다이어그램
    - 잘된 점
  - [ ] After 코드 추출 (개선 코드)
  - [ ] 메타데이터 추가 (분석 시각, 모델명)
- [ ] Markdown 템플릿
  - [ ] resources/templates/report_template.md
  - [ ] GitHub 스타일 형식
  - [ ] 코드 블록 (```csharp```)
- [ ] 파일 저장 기능
  - [ ] 파일명 자동 생성 (코드리뷰_{타임스탬프}.md)
  - [ ] 저장 위치 선택 다이얼로그
  - [ ] 덮어쓰기 경고

**산출물**:
- Report Generator 완성
- Markdown 템플릿 작성
- 파일 저장 기능 동작 확인

---

#### Day 7 (2025-01-14): QTextBrowser 렌더링 및 Pygments 통합
**목표**: Markdown을 HTML로 변환하여 표시

**Tasks**:
- [ ] `app/utils/markdown_renderer.py` 구현
  - [ ] python-markdown 라이브러리 사용
  - [ ] Extensions 설정
    - fenced_code (코드 블록)
    - tables (표)
    - codehilite (코드 하이라이팅)
  - [ ] Pygments 통합
    - C# lexer 설정
    - Monokai 색상 테마
  - [ ] GitHub 스타일 CSS
    - resources/styles/github_markdown.css
- [ ] `app/ui/result_panel.py` 구현
  - [ ] QTextBrowser 초기화
  - [ ] HTML 설정 (setHtml)
  - [ ] CSS 로드 및 적용
  - [ ] 스크롤 위치 복원
- [ ] 테스트
  - [ ] 샘플 Markdown 렌더링 확인
  - [ ] 코드 블록 하이라이팅 확인
  - [ ] 표 및 링크 동작 확인

**산출물**:
- Markdown → HTML 렌더러 완성
- QTextBrowser 결과 패널 완성
- GitHub 스타일 적용 확인

---

#### Day 8 (2025-01-15): Mermaid 다이어그램 PNG 변환
**목표**: 플로우 다이어그램 시각화

**Tasks**:
- [ ] Mermaid CLI 설치
  - [ ] npm install -g @mermaid-js/mermaid-cli
  - [ ] mmdc 명령어 확인
- [ ] `app/core/diagram_converter.py` 구현
  - [ ] Mermaid 코드 추출 (Markdown에서)
  - [ ] 임시 .mmd 파일 생성
  - [ ] mmdc 명령어 실행 (subprocess)
  - [ ] PNG 이미지 생성
  - [ ] 이미지 Base64 인코딩
  - [ ] Markdown에 이미지 삽입 (<img src="data:image/png;base64,...">)
- [ ] 에러 처리
  - [ ] mmdc 실행 실패 시 텍스트 폴백
  - [ ] 타임아웃 설정 (10초)
- [ ] 테스트
  - [ ] 간단한 플로우차트 생성 확인
  - [ ] 복잡한 다이어그램 테스트

**산출물**:
- Mermaid → PNG 변환기 완성
- 다이어그램 표시 확인
- 에러 핸들링 구현

---

### Week 3: 파일 업로드 모드 (Day 9-11)

#### Day 9 (2025-01-16): 파일 선택 UI 및 드래그 앤 드롭
**목표**: 파일 업로드 인터페이스 구현

**Tasks**:
- [ ] `app/ui/file_upload_widget.py` 구현
  - [ ] QListWidget (파일 목록 표시)
  - [ ] "파일 추가" 버튼 (QFileDialog)
  - [ ] "선택 제거" 버튼
  - [ ] 파일 카운터 (총 N개 파일)
- [ ] 드래그 앤 드롭 지원
  - [ ] dragEnterEvent 오버라이드
  - [ ] dropEvent 오버라이드
  - [ ] `.cs` 파일만 필터링
  - [ ] 드롭 영역 하이라이팅
- [ ] 파일 검증
  - [ ] 파일 존재 여부 확인
  - [ ] 파일 크기 제한 (최대 1MB)
  - [ ] UTF-8 인코딩 확인
- [ ] UI 개선
  - [ ] 파일 아이콘 표시
  - [ ] 파일 크기 표시
  - [ ] 더블클릭 시 미리보기

**산출물**:
- 파일 업로드 위젯 완성
- 드래그 앤 드롭 동작 확인
- 파일 검증 로직 구현

---

#### Day 10 (2025-01-17): 다중 파일 분석 및 프로그레스바
**목표**: 여러 파일 순차 분석 및 진행 상태 표시

**Tasks**:
- [ ] 다중 파일 분석 로직
  - [ ] 파일 목록 순회
  - [ ] 각 파일 읽기 (UTF-8)
  - [ ] LLM 호출 (파일별)
  - [ ] After 코드 및 리포트 생성
- [ ] 프로그레스 다이얼로그
  - [ ] QProgressDialog 사용
  - [ ] 진행률 표시 (N/M 파일)
  - [ ] 현재 파일명 표시
  - [ ] "취소" 버튼 (분석 중단)
- [ ] 에러 복구
  - [ ] 파일 읽기 실패 시 스킵
  - [ ] LLM 오류 시 재시도 (최대 3회)
  - [ ] 에러 로그 기록
- [ ] 결과 집계
  - [ ] 성공/실패 파일 개수
  - [ ] 총 소요 시간
  - [ ] 요약 다이얼로그 표시

**산출물**:
- 다중 파일 분석 엔진 완성
- 프로그레스바 동작 확인
- 에러 복구 로직 테스트

---

#### Day 11 (2025-01-18): 파일별 리포트 생성 및 관리
**목표**: 파일별 개별 리포트 저장 및 히스토리 관리

**Tasks**:
- [ ] 파일별 리포트 생성
  - [ ] 파일명 기반 리포트명 ({파일명}_리뷰_{타임스탬프}.md)
  - [ ] 자동 저장 경로 (./reports/)
  - [ ] Markdown + HTML 동시 저장
- [ ] 리포트 히스토리
  - [ ] SQLite DB 생성 (reports.db)
  - [ ] 테이블 스키마 (id, filename, timestamp, report_path)
  - [ ] 리포트 목록 조회
- [ ] 히스토리 UI
  - [ ] "리포트 히스토리" 메뉴
  - [ ] 파일별 리포트 목록 표시
  - [ ] 더블클릭 시 리포트 열기
  - [ ] 삭제 기능
- [ ] 테스트
  - [ ] 5개 파일 동시 분석
  - [ ] 리포트 파일 생성 확인
  - [ ] 히스토리 DB 쿼리 확인

**산출물**:
- 파일별 리포트 저장 완성
- 리포트 히스토리 DB 구현
- 히스토리 UI 완성

---

### Week 4: 폴더 선택 모드 (Day 12-14)

#### Day 12 (2025-01-19): 트리 구조 UI 및 재귀 탐색
**목표**: 폴더 구조를 트리로 표시

**Tasks**:
- [ ] `app/ui/folder_select_widget.py` 구현
  - [ ] QTreeView 초기화
  - [ ] "폴더 선택" 버튼 (QFileDialog)
  - [ ] 트리 모델 생성 (QStandardItemModel)
  - [ ] 체크박스 항목 (Qt.ItemIsUserCheckable)
- [ ] 재귀 탐색 로직
  - [ ] os.walk() 사용
  - [ ] `.cs` 파일만 필터링
  - [ ] 숨김 폴더 제외 (.git, .vs, bin, obj)
  - [ ] 파일 개수 카운팅
- [ ] 트리 UI 개선
  - [ ] 폴더 아이콘/파일 아이콘
  - [ ] 확장/축소 애니메이션
  - [ ] "전체 선택" / "전체 해제" 버튼
- [ ] 테스트
  - [ ] 중첩된 폴더 구조 표시 확인
  - [ ] 체크박스 선택 동작 확인

**산출물**:
- 폴더 선택 위젯 완성
- 재귀 탐색 로직 구현
- 트리 UI 동작 확인

---

#### Day 13 (2025-01-20): 대용량 프로젝트 처리 및 배치 분석
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

#### Day 14 (2025-01-21): 통합 리포트 및 Week 4 마무리
**목표**: 프로젝트 전체 요약 리포트 생성

**Tasks**:
- [ ] 통합 리포트 생성
  - [ ] 프로젝트명 및 분석 시각
  - [ ] 전체 파일 개수 (성공/실패)
  - [ ] 카테고리별 이슈 통계
    - Null 참조: N건
    - Exception: N건
    - 리소스 해제: N건
    - 성능: N건
    - 보안: N건
    - 네이밍: N건
  - [ ] 파일별 상세 리포트 링크
  - [ ] 개선 우선순위 권장
- [ ] 통합 리포트 UI
  - [ ] "프로젝트 요약" 탭 추가
  - [ ] 차트 표시 (matplotlib)
  - [ ] 카테고리별 이슈 분포 (원형 차트)
- [ ] 테스트
  - [ ] 20개 파일 프로젝트 분석
  - [ ] 통합 리포트 생성 확인
  - [ ] 차트 렌더링 확인

**산출물**:
- 통합 리포트 생성기 완성
- 차트 UI 완성
- Week 4 완료 리포트 작성

---

### Week 5: 포터블 패키징 (Day 15-17)

#### Day 15 (2025-01-22): PyInstaller EXE 빌드
**목표**: Python 스크립트를 단일 EXE로 패키징

**Tasks**:
- [ ] PyInstaller 설정
  - [ ] `pip install pyinstaller`
  - [ ] spec 파일 생성 (`pyinstaller --name=CodeReviewer app/main.py`)
- [ ] spec 파일 수정
  - [ ] --onefile 옵션 (단일 EXE)
  - [ ] --windowed 옵션 (콘솔 숨김)
  - [ ] --icon 옵션 (아이콘 설정)
  - [ ] --add-data (리소스 파일 포함)
  - [ ] --exclude-module (불필요 모듈 제외)
- [ ] 빌드 스크립트 작성
  - [ ] scripts/build_exe.py
  - [ ] UPX 압축 (선택적)
  - [ ] 서명 (선택적)
- [ ] 테스트
  - [ ] EXE 실행 확인
  - [ ] 의존성 누락 확인
  - [ ] 에러 로그 확인

**산출물**:
- CodeReviewer.exe 생성 (약 50-100MB)
- 빌드 스크립트 완성
- 실행 테스트 통과

---

#### Day 16 (2025-01-23): Ollama 포터블 번들링
**목표**: Ollama + Phi-3-mini를 포터블 패키지에 포함

**Tasks**:
- [ ] Ollama 포터블 버전 준비
  - [ ] Ollama Windows 바이너리 다운로드
  - [ ] ollama.exe 추출
  - [ ] 모델 파일 경로 설정
- [ ] 모델 파일 번들링
  - [ ] Phi-3-mini GGUF 파일 다운로드
  - [ ] ollama_portable/models/ 폴더에 복사
- [ ] 자동 실행 스크립트
  - [ ] scripts/bundle_ollama.py
  - [ ] CodeReviewer.exe 실행 시 Ollama 자동 시작
  - [ ] 백그라운드 실행 (subprocess.Popen)
  - [ ] 종료 시 Ollama 프로세스 종료
- [ ] 환경 변수 설정
  - [ ] OLLAMA_MODELS 경로 설정
  - [ ] OLLAMA_HOST 설정 (localhost:11434)
- [ ] 테스트
  - [ ] 포터블 패키지 압축 해제
  - [ ] 더블클릭으로 실행 확인
  - [ ] Ollama 자동 시작 확인

**산출물**:
- Ollama 포터블 패키지 완성
- 자동 실행 스크립트 구현
- 통합 테스트 통과

---

#### Day 17 (2025-01-24): 설치 없는 실행 테스트 및 최적화
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

### Week 6: 테스트 및 최적화 (Day 18-21)

#### Day 18 (2025-01-25): 단위 테스트 (Pytest)
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

#### Day 19 (2025-01-26): 통합 테스트 및 VDI 환경 테스트
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

#### Day 20 (2025-01-27): 성능 최적화 및 메모리 관리
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

#### Day 21 (2025-01-28): 문서화 및 사용자 가이드 작성
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
| **Week 2** | Day 5-8 | 코드 분석 엔진 | ✅ 6가지 리뷰 항목, Markdown 리포트 생성 |
| **Week 3** | Day 9-11 | 파일 업로드 모드 | ✅ 다중 파일 분석, 프로그레스바 |
| **Week 4** | Day 12-14 | 폴더 선택 모드 | ✅ 트리 UI, 통합 리포트 |
| **Week 5** | Day 15-17 | 포터블 패키징 | ✅ EXE + Ollama 번들, VDI 실행 |
| **Week 6** | Day 18-21 | 테스트 및 문서화 | ✅ 단위 테스트 >80%, 사용자 가이드 |

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

**마지막 업데이트**: 2025-01-08
**다음 리뷰**: Week 1 종료 후 (Day 4)
**프로젝트 완료 목표**: 2025-02-18 (6주 후)
