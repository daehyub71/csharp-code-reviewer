# C# Code Reviewer

> AI 기반 C# 코드 리뷰 자동화 도구 - 폐쇄망 VDI 환경 완벽 지원

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![Phi-3-mini](https://img.shields.io/badge/LLM-Phi--3--mini-purple.svg)](https://ollama.com/library/phi3)

---

## 프로젝트 소개

**C# Code Reviewer**는 폐쇄망 VDI 환경에서 완전히 오프라인으로 동작하는 AI 기반 코드 리뷰 도구입니다. Microsoft의 경량 LLM인 **Phi-3-mini**를 활용하여 6가지 핵심 리뷰 항목을 자동으로 분석하고, 개선 코드를 제안합니다.

### 주요 특징

- ✅ **완전 오프라인**: 인터넷 연결 없이 100% 로컬에서 실행
- ✅ **관리자 권한 불필요**: 포터블 EXE 형태로 압축 해제 후 바로 실행
- ✅ **AI 기반 리뷰**: Phi-3-mini LLM을 활용한 지능형 코드 분석
- ✅ **7가지 리뷰 항목**: Null 참조, Exception, 리소스 관리, 성능, 보안, 네이밍 컨벤션, XML 문서 주석
- ✅ **3가지 입력 모드**: 텍스트 입력, 파일 업로드 (드래그 앤 드롭), 폴더 선택
- ✅ **다중 파일 분석**: 배치 분석, 프로그레스바, 에러 복구 (최대 3회 재시도)
- ✅ **리포트 자동 저장**: Markdown + HTML 동시 생성, SQLite DB 히스토리 관리
- ✅ **사용자 친화적 GUI**: PySide6 네이티브 인터페이스 (탭 UI, VS Code Dark 테마)

---

## 스크린샷

### 메인 화면 (탭 UI + Before/After Split Editor)
```
┌─────────────────────────────────────────────────────────┐
│  C# Code Reviewer - Phi-3-mini                    [-][□][X] │
├─────────────────────────────────────────────────────────┤
│ File  Edit  View  Tools  Help                           │
├─────────────────────────────────────────────────────────┤
│ [✏️ 텍스트 입력] [📁 파일 업로드]                         │
├───────────────────────┬─────────────────────────────────┤
│  Before (원본 코드)    │   📋 리포트 미리보기             │
├───────────────────────┤   (VS Code Dark 테마)            │
│ using System;         │                                 │
│                       │   # 코드 리뷰 결과               │
│ public class Test     │                                 │
│ {                     │   ## 🔍 발견된 이슈              │
│     var x = null;     │   ### [심각] Null 참조 (Line 5) │
│     Console.Write(x); │   - myObject?.ToString()        │
│ }                     │                                 │
│                       │   ## ✅ 개선 코드                │
├───────────────────────┤   ```csharp                     │
│  After (개선 코드)     │   var x = "value";              │
├───────────────────────┤   Console.Write(x);             │
│ using System;         │   ```                           │
│                       │                                 │
│ public class Test     │   [💾 Save Report]               │
│ {                     │   [📜 리포트 히스토리]            │
│     var x = "value";  │                                 │
│     Console.Write(x); │                                 │
│ }                     │                                 │
└───────────────────────┴─────────────────────────────────┘
│ ✅ 분석 완료 | Ollama: 실행 중 | 메모리: 2.3GB            │
└─────────────────────────────────────────────────────────┘
```

### 파일 업로드 모드
```
┌─────────────────────────────────────────────────────────┐
│ [✏️ 텍스트 입력] [📁 파일 업로드]                         │
├─────────────────────────────────────────────────────────┤
│ 📂 파일 목록 (총 3개 파일)                    [전체 제거] │
├─────────────────────────────────────────────────────────┤
│ ├─ 📄 UserService.cs (2.5 KB)                           │
│ ├─ 📄 FileReader.cs (1.8 KB)                            │
│ └─ 📄 Calculator.cs (1.2 KB)                            │
│                                                          │
│ 💡 드래그 앤 드롭으로 파일을 추가하세요                  │
├─────────────────────────────────────────────────────────┤
│ [파일 추가] [선택 제거] [🔍 Analyze Code]                │
└─────────────────────────────────────────────────────────┘

### 리포트 히스토리 (Ctrl+H)
┌─────────────────────────────────────────────────────────┐
│ 📜 리포트 히스토리                                       │
├─────────────────────────────────────────────────────────┤
│ 총 리포트: 15개 | 성공: 14개 | 평균 분석 시간: 2.5초     │
├──┬───────────────┬────────────────┬────────┬───────────┤
│ID│ 파일명        │ 생성 시간       │ 상태   │ 분석 시간 │
├──┼───────────────┼────────────────┼────────┼───────────┤
│15│ UserService   │ 2025-01-19 14:30│ ✅ 성공│ 2.3초     │
│14│ FileReader    │ 2025-01-19 14:25│ ✅ 성공│ 1.8초     │
│13│ Calculator    │ 2025-01-19 14:20│ ❌ 실패│ 0.5초     │
└──┴───────────────┴────────────────┴────────┴───────────┘
│ 💡 리포트를 더블클릭하면 HTML 파일이 열립니다             │
│ [🔄 새로고침] [🗑️ 선택 항목 삭제] [닫기]                  │
└─────────────────────────────────────────────────────────┘
```

---

## 시스템 요구사항

### 최소 사양
- **OS**: Windows 11 (64-bit)
- **CPU**: 4코어 (Intel i5 이상 권장)
- **RAM**: 8GB
- **디스크 공간**: 5GB (프로그램 + 모델)
- **권한**: 일반 사용자 (관리자 권한 불필요)

### 권장 사양
- **CPU**: 8코어 (Intel i7 이상)
- **RAM**: 16GB
- **디스크**: SSD 권장

---

## 빠른 시작 (5분)

### 1. 다운로드 및 압축 해제

```bash
# 포터블 패키지 다운로드 (약 1.5GB, 압축 시)
# 압축 해제 후 크기: 약 2.5GB

CodeReviewer_Portable/
├── CodeReviewer.exe           # 메인 프로그램
├── ollama_portable/
│   ├── ollama.exe             # Ollama 실행 파일
│   └── models/
│       └── phi3-mini.gguf     # Phi-3-mini 모델 (2.3GB)
├── config/
├── logs/
└── README.txt
```

### 2. 실행

1. **CodeReviewer.exe 더블클릭**
2. 첫 실행 시 초기화 (10-20초)
   - Ollama 백그라운드 실행
   - Phi-3-mini 모델 로드
   - "준비 완료" 메시지 표시

### 3. 코드 분석

**방법 1: 텍스트 붙여넣기 (가장 빠름)**
1. C# 코드를 Before 에디터에 붙여넣기
2. 분석 옵션 선택 (코드 리뷰, 개선 제안, 주석, 다이어그램)
3. **[분석 시작]** 버튼 클릭
4. 1-2초 후 결과 확인
   - After 에디터: 개선 코드
   - Result Panel: Markdown 리포트

**방법 2: 파일 업로드**
1. 입력 방식: "파일 업로드" 선택
2. **[파일 추가]** 버튼 또는 드래그 앤 드롭
3. 여러 파일 선택 가능 (`.cs` 필터)
4. **[분석 시작]** → 진행률 표시
5. 파일별 개별 리포트 저장

**방법 3: 폴더 선택**
1. 입력 방식: "폴더 선택" 선택
2. **[폴더 선택]** 버튼
3. 트리 구조에서 분석할 파일 체크
4. **[분석 시작]** → 통합 리포트 생성

---

## 주요 기능

### 1. 6가지 코드 리뷰 항목

#### 1) Null 참조 체크
```csharp
// ❌ 문제
var result = myObject.ToString();

// ✅ 개선
var result = myObject?.ToString() ?? "N/A";
```

#### 2) Exception 처리 누락
```csharp
// ❌ 문제
public void ReadFile(string path)
{
    var content = File.ReadAllText(path);
}

// ✅ 개선
public void ReadFile(string path)
{
    try
    {
        var content = File.ReadAllText(path);
    }
    catch (FileNotFoundException ex)
    {
        Console.WriteLine($"File not found: {ex.Message}");
    }
}
```

#### 3) 리소스 해제
```csharp
// ❌ 문제
var stream = new FileStream("file.txt", FileMode.Open);
// stream.Dispose() 누락

// ✅ 개선
using (var stream = new FileStream("file.txt", FileMode.Open))
{
    // 자동 해제
}
```

#### 4) 성능 이슈
```csharp
// ❌ 문제 (문자열 반복 연결)
string result = "";
for (int i = 0; i < 1000; i++)
{
    result += i.ToString();
}

// ✅ 개선 (StringBuilder 사용)
var sb = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    sb.Append(i);
}
string result = sb.ToString();
```

#### 5) 보안 취약점
```csharp
// ❌ 문제 (SQL Injection 위험)
string query = $"SELECT * FROM Users WHERE Name = '{userName}'";

// ✅ 개선 (Parameterized Query)
string query = "SELECT * FROM Users WHERE Name = @name";
cmd.Parameters.AddWithValue("@name", userName);
```

#### 6) 네이밍 컨벤션
```csharp
// ❌ 문제
public class userService  // 소문자 시작
{
    private string Logger;  // private인데 PascalCase
}

// ✅ 개선
public class UserService  // PascalCase
{
    private string _logger;  // _camelCase
}
```

### 2. 개선 코드 자동 생성

LLM이 분석 결과를 바탕으로 리팩토링된 코드를 자동 생성합니다.
- After 에디터에 실시간 표시
- 복사 버튼으로 간편하게 적용

### 3. 주석 자동 생성

```csharp
/// <summary>
/// 사용자 이름의 유효성을 검증합니다.
/// </summary>
/// <param name="name">검증할 사용자 이름</param>
/// <returns>유효하면 true, 그렇지 않으면 false</returns>
public bool ValidateUserName(string name)
{
    return !string.IsNullOrEmpty(name) && name.Length >= 3;
}
```

### 4. 플로우 다이어그램 (Mermaid → PNG)

```mermaid
graph TD
    A[Start] --> B{User != null?}
    B -->|No| C[Return false]
    B -->|Yes| D{Role == Admin?}
    D -->|Yes| E[Return true]
    D -->|No| F[Check Permissions]
    F --> G[Return result]
```

자동으로 PNG 이미지로 변환하여 리포트에 포함합니다.

---

## Markdown 리포트 예시

```markdown
# C# 코드 리뷰 리포트

**분석 대상:** MyClass.cs
**분석 시각:** 2025-01-08 14:30:22
**모델:** Phi-3-mini

---

## 📊 요약

| 항목 | 발견 수 |
|------|---------|
| 🔴 심각 | 2 |
| 🟡 경고 | 3 |
| 🟢 제안 | 1 |
| **총합** | **6** |

---

## 🔍 발견된 이슈

### [심각] Null 참조 가능성 (Line 42)

**원본 코드:**
```csharp
var result = myObject.ToString();
```

**문제점:** myObject가 null일 경우 NullReferenceException 발생

**개선 코드:**
```csharp
var result = myObject?.ToString() ?? "N/A";
```

---

## ✅ 잘된 점

- Exception 처리가 적절함
- 네이밍 컨벤션 준수
```

---

## 개발 로드맵

### Phase 1: MVP ✅ 완료 (Week 1-2)
- [x] Before/After Split Editor
- [x] 7가지 코드 리뷰 카테고리
- [x] Markdown 리포트 생성
- [x] Phi-3-mini 통합
- [x] 텍스트/파일 모드 탭 UI
- [x] 리포트 자동 저장 (Markdown + HTML)
- [x] 리포트 히스토리 DB

### Phase 2: 파일 업로드 ✅ 완료 (Week 3)
- [x] 파일 선택 UI
- [x] 다중 파일 분석 (배치 모드)
- [x] 드래그 앤 드롭
- [x] 프로그레스 다이얼로그
- [x] 에러 복구 (3회 재시도)
- [x] 분석 결과 요약

### Phase 3: 폴더 선택 (현재 - Week 4)
- [ ] 트리 구조 UI
- [ ] 대용량 프로젝트 처리
- [ ] 통합 리포트

### Phase 4: 포터블 패키징 (Week 5)
- [ ] PyInstaller EXE 빌드
- [ ] Ollama 포터블 번들링
- [ ] VDI 환경 테스트

### Phase 5: 최적화 (Week 6)
- [ ] 성능 최적화
- [ ] 단위 테스트 (>80% 커버리지)
- [ ] 사용자 가이드 작성

---

## 기술 스택

- **LLM**: Phi-3-mini (3.8B 파라미터, 2.3GB GGUF)
- **Backend**: Python 3.11 + Ollama SDK
- **Frontend**: PySide6 (Qt6 Python 바인딩)
- **Markdown**: python-markdown + Pygments
- **Diagram**: Mermaid CLI
- **Packaging**: PyInstaller

---

## 문서

- [프로젝트 계획서](docs/PROJECT_PLAN.md)
- [개발 일정](docs/DEVELOPMENT_TIMELINE.md)
- [기술 명세서](docs/TECHNICAL_SPECIFICATION.md)
- [사용자 가이드](docs/USER_GUIDE.md)
- [문제 해결](docs/TROUBLESHOOTING.md)

---

## 라이선스

이 프로젝트는 MIT License 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

- **PySide6**: LGPL v3 (상업용 무료)
- **Phi-3-mini**: MIT License
- **Ollama**: MIT License

---

## 기여하기

버그 리포트, 기능 제안, Pull Request를 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 문의

문제가 발생하거나 질문이 있으시면 [GitHub Issues](https://github.com/yourusername/csharp-code-reviewer/issues)에 등록해주세요.

---

**작성일**: 2025-01-08
**버전**: 1.0.0
**개발 기간**: 6주 (2025-01-08 ~ 2025-02-18)
