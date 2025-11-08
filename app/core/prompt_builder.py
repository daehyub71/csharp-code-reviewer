"""
C# 코드 리뷰를 위한 프롬프트 빌더

이 모듈은 LLM에 전달할 프롬프트를 생성하고 최적화합니다.
토큰 수를 최소화하면서 효과적인 코드 리뷰를 수행합니다.
"""

from typing import List, Dict, Any
from enum import Enum


class ReviewCategory(Enum):
    """코드 리뷰 카테고리"""
    NULL_REFERENCE = "null_reference"  # Null 참조 체크
    EXCEPTION_HANDLING = "exception_handling"  # Exception 처리 누락
    RESOURCE_MANAGEMENT = "resource_management"  # 리소스 해제
    PERFORMANCE = "performance"  # 성능 이슈
    SECURITY = "security"  # 보안 취약점
    NAMING_CONVENTION = "naming_convention"  # 네이밍 컨벤션


class OutputFormat(Enum):
    """출력 형식"""
    IMPROVED_CODE = "improved_code"  # 개선된 코드
    CODE_COMMENTS = "code_comments"  # 코드 주석
    FLOW_DIAGRAM = "flow_diagram"  # 플로우 다이어그램


class PromptBuilder:
    """
    LLM 프롬프트 빌더 클래스

    C# 코드 리뷰를 위한 최적화된 프롬프트를 생성합니다.
    Few-shot 예제를 포함하며, 토큰 수를 1500개 이하로 유지합니다.
    """

    # 시스템 프롬프트 (역할 정의)
    SYSTEM_PROMPT = """당신은 C# 코드 리뷰 전문가입니다. 주어진 코드를 분석하고 개선된 버전을 제공합니다.
다음 원칙을 따르세요:
1. 실용적이고 구체적인 개선 제안
2. C# 모범 사례 준수
3. 명확하고 간결한 코드
4. 성능과 가독성 균형"""

    # 6가지 리뷰 항목 템플릿
    REVIEW_TEMPLATES = {
        ReviewCategory.NULL_REFERENCE: {
            "name": "Null 참조 체크",
            "description": "null 참조 예외를 방지하는 검증 로직 추가",
            "rules": [
                "메서드 파라미터에 null 체크 추가",
                "null 조건 연산자 (?., ??) 활용",
                "ArgumentNullException 던지기"
            ]
        },
        ReviewCategory.EXCEPTION_HANDLING: {
            "name": "Exception 처리",
            "description": "적절한 예외 처리 및 에러 핸들링",
            "rules": [
                "try-catch 블록으로 예외 처리",
                "구체적인 예외 타입 사용",
                "예외 메시지 명확하게 작성",
                "finally 블록으로 정리 작업"
            ]
        },
        ReviewCategory.RESOURCE_MANAGEMENT: {
            "name": "리소스 관리",
            "description": "IDisposable 리소스의 올바른 해제",
            "rules": [
                "using 문으로 자동 해제",
                "IDisposable 구현 확인",
                "파일/DB 연결 명시적 닫기"
            ]
        },
        ReviewCategory.PERFORMANCE: {
            "name": "성능 최적화",
            "description": "불필요한 연산 제거 및 효율성 향상",
            "rules": [
                "LINQ 최적화 (ToList() 남용 방지)",
                "StringBuilder 사용 (문자열 연결)",
                "불필요한 반복문 제거",
                "캐싱 활용"
            ]
        },
        ReviewCategory.SECURITY: {
            "name": "보안",
            "description": "보안 취약점 제거",
            "rules": [
                "SQL Injection 방지 (파라미터화)",
                "입력 값 검증",
                "민감 정보 암호화",
                "권한 체크"
            ]
        },
        ReviewCategory.NAMING_CONVENTION: {
            "name": "네이밍 규칙",
            "description": "C# 네이밍 컨벤션 준수",
            "rules": [
                "PascalCase: 클래스, 메서드, 프로퍼티",
                "camelCase: 로컬 변수, 파라미터",
                "_camelCase: private 필드",
                "의미 있는 이름 사용"
            ]
        }
    }

    # Few-shot 예제 (토큰 최적화)
    FEW_SHOT_EXAMPLES = [
        {
            "category": ReviewCategory.NULL_REFERENCE,
            "before": """public void ProcessData(string data)
{
    var result = data.ToUpper();
    Console.WriteLine(result);
}""",
            "after": """public void ProcessData(string data)
{
    if (string.IsNullOrEmpty(data))
        throw new ArgumentNullException(nameof(data));

    var result = data.ToUpper();
    Console.WriteLine(result);
}"""
        },
        {
            "category": ReviewCategory.RESOURCE_MANAGEMENT,
            "before": """public void ReadFile(string path)
{
    StreamReader reader = new StreamReader(path);
    string content = reader.ReadToEnd();
    Console.WriteLine(content);
}""",
            "after": """public void ReadFile(string path)
{
    using (var reader = new StreamReader(path))
    {
        string content = reader.ReadToEnd();
        Console.WriteLine(content);
    }
}"""
        },
        {
            "category": ReviewCategory.EXCEPTION_HANDLING,
            "before": """public int Divide(int a, int b)
{
    return a / b;
}""",
            "after": """public int Divide(int a, int b)
{
    if (b == 0)
        throw new DivideByZeroException("제수는 0이 될 수 없습니다.");

    return a / b;
}"""
        }
    ]

    def __init__(self):
        """PromptBuilder 초기화"""
        self.system_prompt = self.SYSTEM_PROMPT

    def build_review_prompt(
        self,
        code: str,
        categories: List[ReviewCategory],
        output_format: OutputFormat = OutputFormat.IMPROVED_CODE,
        include_examples: bool = True
    ) -> str:
        """
        코드 리뷰 프롬프트 생성

        Args:
            code: 리뷰할 C# 코드
            categories: 리뷰 카테고리 목록
            output_format: 출력 형식
            include_examples: Few-shot 예제 포함 여부

        Returns:
            최적화된 프롬프트 문자열
        """
        prompt_parts = []

        # 1. 리뷰 카테고리 설명
        if categories:
            prompt_parts.append("다음 항목을 중점적으로 검토하세요:")
            for category in categories:
                template = self.REVIEW_TEMPLATES[category]
                prompt_parts.append(f"\n• {template['name']}: {template['description']}")

        # 2. Few-shot 예제 (선택한 카테고리만)
        if include_examples and categories:
            relevant_examples = [
                ex for ex in self.FEW_SHOT_EXAMPLES
                if ex["category"] in categories
            ]

            if relevant_examples:
                prompt_parts.append("\n\n예제:")
                for i, example in enumerate(relevant_examples[:2], 1):  # 최대 2개만
                    category_name = self.REVIEW_TEMPLATES[example["category"]]["name"]
                    prompt_parts.append(f"\n[{category_name}]")
                    prompt_parts.append(f"Before:\n{example['before']}")
                    prompt_parts.append(f"\nAfter:\n{example['after']}\n")

        # 3. 사용자 코드
        prompt_parts.append(f"\n분석할 코드:\n```csharp\n{code}\n```")

        # 4. 출력 형식 지시
        prompt_parts.append(f"\n{self._get_output_instruction(output_format)}")

        return "\n".join(prompt_parts)

    def build_comment_prompt(self, code: str) -> str:
        """
        코드 주석 생성 프롬프트

        Args:
            code: 주석을 추가할 C# 코드

        Returns:
            주석 생성 프롬프트
        """
        prompt = f"""다음 C# 코드에 XML 문서 주석을 추가하세요.

규칙:
- 클래스/메서드에 /// <summary> 추가
- 파라미터에 /// <param> 추가
- 반환값에 /// <returns> 추가
- 한글로 명확하게 작성

코드:
```csharp
{code}
```

주석이 추가된 코드를 출력하세요."""

        return prompt

    def build_flow_diagram_prompt(self, code: str) -> str:
        """
        플로우 다이어그램 생성 프롬프트

        Args:
            code: 플로우를 분석할 C# 코드

        Returns:
            플로우 다이어그램 프롬프트
        """
        prompt = f"""다음 C# 코드의 실행 흐름을 Mermaid 다이어그램으로 표현하세요.

코드:
```csharp
{code}
```

출력 형식:
```mermaid
graph TD
    A[시작] --> B[...]
    B --> C[...]
```

조건문, 반복문, 메서드 호출을 명확히 표시하세요."""

        return prompt

    def _get_output_instruction(self, output_format: OutputFormat) -> str:
        """
        출력 형식별 지시사항 반환

        Args:
            output_format: 출력 형식

        Returns:
            지시사항 문자열
        """
        instructions = {
            OutputFormat.IMPROVED_CODE: """개선된 C# 코드만 출력하세요.
설명이나 마크다운 없이 순수 코드만 작성하세요.""",

            OutputFormat.CODE_COMMENTS: """원본 코드에 XML 문서 주석을 추가하여 출력하세요.""",

            OutputFormat.FLOW_DIAGRAM: """Mermaid 형식의 플로우 다이어그램을 출력하세요."""
        }

        return instructions.get(output_format, instructions[OutputFormat.IMPROVED_CODE])

    def estimate_tokens(self, text: str) -> int:
        """
        대략적인 토큰 수 추정 (1 토큰 ≈ 4 글자)

        Args:
            text: 추정할 텍스트

        Returns:
            예상 토큰 수
        """
        # 간단한 추정: 공백 기준 단어 수 + 코드 특수문자 보정
        words = len(text.split())
        chars = len(text)

        # 평균적으로 영어 1단어 = 1.3토큰, 한글 1글자 = 0.5토큰
        estimated = (words * 1.3) + (chars * 0.1)

        return int(estimated)

    def optimize_prompt(self, prompt: str, max_tokens: int = 1500) -> str:
        """
        프롬프트를 토큰 제한 내로 최적화

        Args:
            prompt: 원본 프롬프트
            max_tokens: 최대 토큰 수

        Returns:
            최적화된 프롬프트
        """
        current_tokens = self.estimate_tokens(prompt)

        if current_tokens <= max_tokens:
            return prompt

        # 토큰 초과 시 예제 제거 또는 축약
        # 실제로는 더 정교한 최적화 필요
        lines = prompt.split('\n')

        # 예제 섹션 제거
        optimized_lines = []
        skip_example = False

        for line in lines:
            if '예제:' in line:
                skip_example = True
                continue
            if skip_example and line.startswith('['):
                continue
            if skip_example and ('Before:' in line or 'After:' in line):
                continue
            if skip_example and line.strip().startswith('```'):
                continue
            if skip_example and not line.strip():
                skip_example = False
                continue

            optimized_lines.append(line)

        return '\n'.join(optimized_lines)


# 사용 예제
if __name__ == "__main__":
    # PromptBuilder 생성
    builder = PromptBuilder()

    # 테스트 코드
    test_code = """public void ProcessData(string data)
{
    var result = data.ToUpper();
    Console.WriteLine(result);
}"""

    # 1. 코드 리뷰 프롬프트 생성
    review_prompt = builder.build_review_prompt(
        code=test_code,
        categories=[
            ReviewCategory.NULL_REFERENCE,
            ReviewCategory.EXCEPTION_HANDLING
        ],
        output_format=OutputFormat.IMPROVED_CODE,
        include_examples=True
    )

    print("=== 코드 리뷰 프롬프트 ===")
    print(review_prompt)
    print(f"\n예상 토큰 수: {builder.estimate_tokens(review_prompt)}")

    # 2. 주석 생성 프롬프트
    print("\n\n=== 주석 생성 프롬프트 ===")
    comment_prompt = builder.build_comment_prompt(test_code)
    print(comment_prompt)
    print(f"\n예상 토큰 수: {builder.estimate_tokens(comment_prompt)}")

    # 3. 플로우 다이어그램 프롬프트
    print("\n\n=== 플로우 다이어그램 프롬프트 ===")
    flow_prompt = builder.build_flow_diagram_prompt(test_code)
    print(flow_prompt)
    print(f"\n예상 토큰 수: {builder.estimate_tokens(flow_prompt)}")
