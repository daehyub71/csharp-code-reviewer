# C# Code Reviewer - 프로젝트 계획서

## 프로젝트 개요

### 목적
폐쇄망 VDI 환경에서 동작하는 C# 코드 리뷰 자동화 도구를 개발하여, 개발자의 코드 품질을 향상시키고 버그를 사전에 발견합니다.

### 핵심 가치
- **오프라인 완전 동작**: 인터넷 연결 없이 100% 로컬에서 실행
- **관리자 권한 불필요**: 포터블 EXE 형태로 압축 해제 후 바로 실행
- **AI 기반 리뷰**: Phi-3-mini LLM을 활용한 지능형 코드 분석
- **사용자 친화적 GUI**: PySide6 네이티브 인터페이스

### 대상 사용자
- 폐쇄망 VDI 환경에서 근무하는 C# 개발자
- 코드 리뷰 자동화를 원하는 팀
- 코딩 컨벤션 준수를 확인하고 싶은 개발자

---

## 기능 명세

### Phase 1: MVP (텍스트 에디터 모드)

#### 1. 코드 입력
- **Before/After Split Editor**
  - Before: 사용자가 C# 코드 붙여넣기
  - After: 분석 완료 후 개선 코드 자동 표시
  - C# Syntax Highlighting (Pygments)
  - 동기화 스크롤 (Before/After 동시 스크롤)

#### 2. 코드 리뷰 (6가지 항목)
1. **Null 참조 체크**
   - NullReferenceException 가능성 탐지
   - Null-conditional operator (`?.`) 사용 권장

2. **Exception 처리 누락**
   - try-catch 블록 적절성 검증
   - throw 구문 검토

3. **리소스 해제**
   - using 문 사용 확인
   - IDisposable 구현 검증
   - Dispose 패턴 검토

4. **성능 이슈**
   - 불필요한 루프 최적화
   - LINQ 쿼리 효율성 검증
   - StringBuilder vs String concatenation

5. **보안 취약점**
   - SQL Injection 가능성
   - XSS (Cross-Site Scripting) 취약점
   - Path Traversal 공격 위험
   - 하드코딩된 비밀번호/API 키

6. **네이밍 컨벤션**
   - 클래스/메서드: PascalCase
   - 지역 변수/매개변수: camelCase
   - private 필드: _camelCase
   - 상수: UPPER_CASE 또는 PascalCase
   - 인터페이스: IPascalCase

#### 3. 추가 기능
- **개선 코드 제안**: 리팩토링된 코드 자동 생성
- **주석 생성**: 함수/클래스 설명 주석 자동 작성
- **플로우 다이어그램**: Mermaid → PNG 변환하여 표시

#### 4. 결과 출력
- **Markdown 리포트**
  - GitHub 스타일 렌더링 (QTextBrowser)
  - 코드 하이라이팅 (Pygments)
  - PNG 다이어그램 임베딩
- **저장 기능**
  - Markdown 파일 저장
  - HTML 내보내기

---

### Phase 2: 파일 업로드 모드

#### 1. 파일 선택
- 단일/다중 파일 선택 (`.cs` 필터)
- 드래그 앤 드롭 지원
- 파일 목록 표시 (QListWidget)
- 개별 파일 제거 기능

#### 2. 분석 처리
- 파일별 개별 리포트 생성
- 프로그레스바 표시
- 현재 처리 중인 파일명 표시

#### 3. 결과 관리
- 파일별 Markdown 저장 (`{파일명}_리뷰_{타임스탬프}.md`)
- 리포트 히스토리 관리

---

### Phase 3: 폴더 선택 모드

#### 1. 폴더 탐색
- 트리 구조 표시 (QTreeView)
- 재귀적 `.cs` 파일 탐색
- 체크박스로 개별 파일 선택/해제

#### 2. 대용량 프로젝트 처리
- 최대 50개 파일 제한 (경고 표시)
- 배치 처리 (10개씩 순차 분석)

#### 3. 통합 리포트
- 프로젝트 전체 요약 리포트
- 파일별 상세 리포트 링크

---

## 기술 스택

### LLM
- **Phi-3-mini** (3.8B 파라미터)
  - 모델 크기: ~2.3GB (GGUF 양자화)
  - 추론 속도: 1-2초/응답 (CPU, 4코어 8GB 기준)
  - Microsoft 공식 모델 (C# 특화)
  - Ollama 지원 (`ollama pull phi3:mini`)

### 백엔드
- **Python 3.11+**
- **Ollama SDK** (LLM 통신)
- **Markdown** (python-markdown)
- **Pygments** (코드 하이라이팅)
- **Mermaid CLI** (다이어그램 PNG 변환)

### 프론트엔드
- **PySide6** (Qt6 Python 바인딩)
  - 라이선스: LGPL (상업용 무료)
  - 크로스 플랫폼: Windows/macOS/Linux
- **QTextBrowser** (Markdown 렌더링, Phase 1)
- **QPlainTextEdit** (코드 에디터)

### 패키징
- **PyInstaller** (Python → EXE 변환)
- **Ollama Portable** (실행 파일 + 모델 번들)
- **InnoSetup** (선택적, 설치 마법사)

---

## 시스템 아키텍처

### 전체 구조

```
┌─────────────────────────────────────────┐
│       PySide6 GUI (Main Window)         │
├─────────────────────────────────────────┤
│  Input Panel   │   Result Panel          │
│  (QStackedWidget)│  (QTextBrowser)        │
│                │                         │
│  - Before Editor│  - Markdown Viewer     │
│  - After Editor │  - Syntax Highlighting │
│                │  - Diagram Display      │
└────────┬────────┴──────────┬─────────────┘
         │                   │
         ▼                   ▼
┌─────────────────┐  ┌──────────────────┐
│ Code Analyzer   │  │ Report Generator │
│                 │  │                  │
│ - Prompt Builder│  │ - Markdown Format│
│ - LLM Caller    │  │ - Pygments Style │
└────────┬────────┘  └──────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│       Ollama Local Server               │
│       (Phi-3-mini Model)                │
└─────────────────────────────────────────┘
```

### 프로세스 흐름

```
1. 사용자 입력
   ├─ 텍스트 붙여넣기 (Phase 1)
   ├─ 파일 업로드 (Phase 2)
   └─ 폴더 선택 (Phase 3)

2. 전처리
   ├─ Syntax 검증
   ├─ 파일 인코딩 확인
   └─ 코드 정규화

3. LLM 분석
   ├─ 프롬프트 생성 (6가지 리뷰 항목)
   ├─ Ollama API 호출
   ├─ 응답 파싱 (Markdown)
   └─ After 코드 추출

4. 결과 생성
   ├─ Markdown 리포트 작성
   ├─ Mermaid → PNG 변환
   ├─ Pygments 코드 하이라이팅
   └─ QTextBrowser 렌더링

5. 출력
   ├─ Before/After 에디터 업데이트
   ├─ Result Panel 표시
   └─ 파일 저장 (선택적)
```

---

## 디렉토리 구조

```
csharp-code-reviewer/
├── app/
│   ├── __init__.py
│   ├── main.py                    # PySide6 메인 윈도우
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py         # 메인 윈도우 UI
│   │   ├── input_panel.py         # 입력 패널 (QStackedWidget)
│   │   ├── before_after_editor.py # Before/After 에디터
│   │   ├── file_upload_widget.py  # 파일 업로드 UI
│   │   ├── folder_select_widget.py# 폴더 선택 UI
│   │   └── result_panel.py        # 결과 표시 패널
│   ├── core/
│   │   ├── __init__.py
│   │   ├── analyzer.py            # 코드 분석 로직
│   │   ├── ollama_client.py       # Ollama API 클라이언트
│   │   ├── prompt_builder.py      # LLM 프롬프트 생성
│   │   ├── report_generator.py    # Markdown 리포트 생성
│   │   └── diagram_converter.py   # Mermaid → PNG 변환
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── syntax_highlighter.py  # C# Syntax Highlighting
│   │   ├── markdown_renderer.py   # Markdown → HTML
│   │   └── file_handler.py        # 파일 입출력
│   └── config/
│       ├── __init__.py
│       └── settings.py            # 애플리케이션 설정
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_ollama_client.py
│   └── test_report_generator.py
├── resources/
│   ├── icons/                     # 애플리케이션 아이콘
│   ├── styles/                    # QSS 스타일시트
│   └── templates/                 # Markdown 템플릿
├── scripts/
│   ├── build_exe.py               # PyInstaller 빌드 스크립트
│   └── bundle_ollama.py           # Ollama 번들링 스크립트
├── docs/
│   ├── PROJECT_PLAN.md            # 이 문서
│   ├── DEVELOPMENT_TIMELINE.md    # 개발 일정
│   ├── TECHNICAL_SPECIFICATION.md # 기술 명세
│   ├── USER_GUIDE.md              # 사용자 가이드
│   └── API_REFERENCE.md           # 내부 API 문서
├── requirements.txt               # Python 의존성
├── pyproject.toml                 # 프로젝트 메타데이터
├── .gitignore
└── README.md                      # 프로젝트 소개
```

---

## 개발 일정

### Week 1: 기본 구조 및 LLM 통합 (Phase 1 Part 1)
- Day 1: 프로젝트 설정, PySide6 기본 UI
- Day 2: Ollama 통합, Phi-3-mini 테스트
- Day 3: Before/After 에디터 구현
- Day 4: Syntax Highlighting, 동기화 스크롤

### Week 2: 코드 분석 엔진 (Phase 1 Part 2)
- Day 5: Prompt Builder, 6가지 리뷰 항목
- Day 6: Report Generator, Markdown 생성
- Day 7: QTextBrowser 렌더링, Pygments 통합
- Day 8: Mermaid 다이어그램 PNG 변환

### Week 3: 파일 업로드 (Phase 2)
- Day 9: 파일 선택 UI, 드래그 앤 드롭
- Day 10: 다중 파일 분석, 프로그레스바
- Day 11: 파일별 리포트 생성

### Week 4: 폴더 선택 (Phase 3)
- Day 12: 트리 구조 UI, 재귀 탐색
- Day 13: 대용량 프로젝트 처리, 배치 분석
- Day 14: 통합 리포트

### Week 5: 포터블 패키징
- Day 15: PyInstaller EXE 빌드
- Day 16: Ollama 포터블 번들링
- Day 17: 설치 없는 실행 테스트

### Week 6: 테스트 및 최적화
- Day 18: 단위 테스트 (Pytest)
- Day 19: 통합 테스트, VDI 환경 테스트
- Day 20: 성능 최적화, 메모리 사용량 감소
- Day 21: 문서화, 사용자 가이드 작성

**총 개발 기간**: 6주 (42일)

---

## 환경 요구사항

### VDI 환경
- **OS**: Windows 11 (64-bit)
- **CPU**: 4코어 이상 (권장)
- **RAM**: 8GB 이상 (권장: 16GB)
- **디스크 공간**: 5GB 이상 (프로그램 + 모델)
- **권한**: 관리자 권한 불필요 (포터블)

### 포터블 패키지 구성
```
CodeReviewer_Portable/
├── CodeReviewer.exe           # PyInstaller로 패키징된 메인 프로그램 (약 50MB)
├── ollama_portable/
│   ├── ollama.exe             # Ollama 실행 파일 (약 100MB)
│   └── models/
│       └── phi3-mini.gguf     # Phi-3-mini 모델 (2.3GB)
├── config/
│   └── settings.json          # 사용자 설정
├── logs/                      # 애플리케이션 로그
└── README.txt                 # 빠른 시작 가이드

총 크기: 약 2.5GB (압축 시 약 1.5GB)
```

---

## 위험 관리

### 기술적 위험

#### 1. Ollama 포터블 실행 문제
**위험**: VDI 환경에서 Ollama가 관리자 권한 없이 실행되지 않을 수 있음
**대응책**:
- Ollama 대신 `llama.cpp` 사용 (더 가볍고 포터블)
- Python에서 직접 GGUF 모델 로드 (`llama-cpp-python`)

#### 2. PyInstaller 번들 크기
**위험**: EXE 파일이 너무 커질 수 있음 (PySide6 포함 시 100MB+)
**대응책**:
- UPX 압축 사용
- 불필요한 모듈 제외 (`--exclude-module`)
- Qt 플러그인 최소화

#### 3. Phi-3-mini 성능
**위험**: 저사양 VDI에서 추론 속도가 너무 느릴 수 있음
**대응책**:
- 양자화 레벨 조정 (Q4_K_M → Q5_K_M)
- 프롬프트 최적화 (토큰 수 감소)
- 배치 처리 대신 스트리밍 응답

#### 4. QTextBrowser Markdown 제약
**위험**: Mermaid 다이어그램이 제대로 렌더링되지 않을 수 있음
**대응책**:
- Mermaid CLI로 PNG 이미지 변환 (구현 완료)
- 다이어그램 생성 실패 시 텍스트로 폴백

### 일정 위험

#### Week 1-2 지연
**대응책**: Phase 2-3 기능 제외, MVP만 완성

#### Week 3-4 지연
**대응책**: 폴더 선택 기능 제외, 파일 업로드만 구현

#### Week 5 패키징 이슈
**대응책**: 포터블 대신 Python 스크립트 배포 (사용자가 Python 설치 필요)

---

## 성공 지표

### 기능적 지표
- ✅ 6가지 코드 리뷰 항목 모두 동작
- ✅ Markdown 리포트 생성 성공률 >95%
- ✅ 플로우 다이어그램 생성 성공률 >90%

### 성능 지표
- ✅ 100줄 코드 분석 시간 <5초
- ✅ 500줄 코드 분석 시간 <20초
- ✅ 메모리 사용량 <3GB (모델 로드 포함)

### 사용자 경험
- ✅ 설치 없이 더블클릭으로 실행 가능
- ✅ 첫 실행 시 초기화 시간 <30초
- ✅ UI 응답성: 버튼 클릭 후 <200ms 반응

### 안정성
- ✅ 크래시 발생률 <1%
- ✅ 에러 복구 기능 100% 구현
- ✅ 로그 기록 및 디버깅 지원

---

## 향후 확장 계획 (Phase 4+)

### 1. 다중 언어 지원
- Python, Java, JavaScript 코드 리뷰
- 언어별 프롬프트 템플릿

### 2. 커스텀 규칙
- 사용자 정의 리뷰 항목
- 회사 코딩 컨벤션 적용

### 3. Git 통합
- Git Diff 자동 분석
- Pre-commit Hook 연동

### 4. 팀 협업
- 리뷰 결과 공유 (JSON 내보내기)
- 통계 대시보드 (리뷰 히스토리)

### 5. LLM 모델 교체
- Llama 3.1, CodeLlama 등 다양한 모델 지원
- 모델 다운로드 UI

---

## 라이선스

- **프로젝트 라이선스**: MIT License
- **PySide6**: LGPL v3 (상업용 무료)
- **Phi-3-mini**: MIT License
- **Ollama**: MIT License

---

**작성일**: 2025-01-08
**작성자**: AI Assistant + 사용자 협업
**버전**: 1.0
**다음 리뷰**: Week 1 종료 후
