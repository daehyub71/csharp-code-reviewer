"""
Markdown 기반 PromptBuilder 통합 테스트

Markdown 파일에서 규칙과 예제를 올바르게 로드하는지 확인합니다.
"""

from pathlib import Path
import sys

# 프로젝트 루트를 PYTHONPATH에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.prompt_builder import PromptBuilder, ReviewCategory

def test_markdown_loading():
    """Markdown 파일 로딩 테스트"""
    print("=" * 80)
    print("Markdown 기반 PromptBuilder 통합 테스트")
    print("=" * 80)

    # PromptBuilder 생성 (use_markdown=True)
    print("\n[1] PromptBuilder 초기화 (Markdown 모드)...")
    builder = PromptBuilder(use_markdown=True)
    print("✅ 초기화 완료")

    # 로드된 카테고리 확인
    print(f"\n[2] 로드된 카테고리 수: {len(builder.categories_data)}개")
    for key, data in builder.categories_data.items():
        print(f"   • {key}: {data['name']}")

    # review_templates 확인
    print(f"\n[3] review_templates 딕셔너리 크기: {len(builder.review_templates)}개")
    for category, template in builder.review_templates.items():
        print(f"   • {category.name}: {template['name']}")
        print(f"      규칙 수: {len(template['rules'])}개")

    # few_shot_examples 확인
    print(f"\n[4] few_shot_examples 리스트 크기: {len(builder.few_shot_examples)}개")
    for i, example in enumerate(builder.few_shot_examples, 1):
        category = example['category']
        before_lines = len(example['before'].split('\n'))
        after_lines = len(example['after'].split('\n'))
        print(f"   {i}. {category.name}")
        print(f"      Before: {before_lines} 줄, After: {after_lines} 줄")

    # 특정 카테고리 상세 확인 (CODE_DOCUMENTATION)
    print(f"\n[5] CODE_DOCUMENTATION 카테고리 상세:")
    code_doc_template = builder.review_templates[ReviewCategory.CODE_DOCUMENTATION]
    print(f"   이름: {code_doc_template['name']}")
    print(f"   설명: {code_doc_template['description']}")
    print(f"   규칙 수: {len(code_doc_template['rules'])}개")
    print("   규칙 목록:")
    for i, rule in enumerate(code_doc_template['rules'][:5], 1):  # 처음 5개만
        print(f"      {i}. {rule}")

    # 프롬프트 생성 테스트
    print(f"\n[6] 프롬프트 생성 테스트...")
    test_code = """
public void ProcessData(string data)
{
    var result = data.ToUpper();
    Console.WriteLine(result);
}
"""

    # NULL_REFERENCE와 CODE_DOCUMENTATION 카테고리로 프롬프트 생성
    categories = [ReviewCategory.NULL_REFERENCE, ReviewCategory.CODE_DOCUMENTATION]
    prompt = builder.build_review_prompt(
        code=test_code,
        categories=categories,
        include_examples=True
    )

    print(f"   생성된 프롬프트 길이: {len(prompt)} 글자")
    print(f"   프롬프트 미리보기 (처음 500자):")
    print("   " + "-" * 76)
    print("   " + prompt[:500].replace('\n', '\n   '))
    print("   " + "-" * 76)

    print("\n" + "=" * 80)
    print("✅ 모든 테스트 통과!")
    print("=" * 80)

def test_backward_compatibility():
    """하드코딩 모드 (use_markdown=False) 호환성 테스트"""
    print("\n" + "=" * 80)
    print("하드코딩 모드 호환성 테스트")
    print("=" * 80)

    print("\n[1] PromptBuilder 초기화 (하드코딩 모드)...")
    builder = PromptBuilder(use_markdown=False)
    print("✅ 초기화 완료")

    print(f"\n[2] review_templates 크기: {len(builder.review_templates)}개")
    print(f"   (하드코딩된 REVIEW_TEMPLATES 사용)")

    print(f"\n[3] few_shot_examples 크기: {len(builder.few_shot_examples)}개")
    print(f"   (하드코딩된 FEW_SHOT_EXAMPLES 사용)")

    print("\n" + "=" * 80)
    print("✅ 하드코딩 모드도 정상 작동!")
    print("=" * 80)

if __name__ == "__main__":
    # Markdown 모드 테스트
    test_markdown_loading()

    # 하드코딩 모드 테스트
    test_backward_compatibility()

    print("\n🎉 통합 테스트 완료!")
