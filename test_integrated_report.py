"""
통합 리포트 생성기 테스트

배치 분석 결과를 시뮬레이션하고 통합 리포트를 생성합니다.
"""

from datetime import datetime
from pathlib import Path
import sys

# BatchAnalysisResult와 FileAnalysisResult를 위해 임포트
from app.core.batch_analyzer import BatchAnalysisResult, FileAnalysisResult
from app.core.integrated_report_generator import IntegratedReportGenerator


def create_mock_batch_result() -> BatchAnalysisResult:
    """모의 배치 분석 결과 생성"""
    results = []

    # 성공한 파일들 (다양한 카테고리 이슈 포함)
    mock_files = [
        ("User.cs", "Null 참조 체크", "Exception 처리"),
        ("Product.cs", "리소스 관리", "성능 최적화"),
        ("Order.cs", "보안", "네이밍 컨벤션"),
        ("Database.cs", "리소스 관리", "Exception 처리"),
        ("Config.cs", "하드코딩 → Config 파일", "보안"),
        ("Logger.cs", "Exception 처리", "Null 참조 체크"),
        ("Service.cs", "성능 최적화", "네이밍 컨벤션"),
        ("Controller.cs", "Null 참조 체크", "Exception 처리"),
        ("Model.cs", "XML 문서 주석", "네이밍 컨벤션"),
        ("Helper.cs", "성능 최적화", "리소스 관리"),
        ("Repository.cs", "Exception 처리", "보안"),
        ("Validator.cs", "Null 참조 체크", "Exception 처리"),
        ("Mapper.cs", "성능 최적화", "네이밍 컨벤션"),
        ("Factory.cs", "Null 참조 체크", "리소스 관리"),
        ("Util.cs", "네이밍 컨벤션", "XML 문서 주석"),
        ("Manager.cs", "Exception 처리", "리소스 관리"),
        ("Handler.cs", "보안", "Null 참조 체크"),
        ("Provider.cs", "성능 최적화", "Exception 처리"),
        ("Builder.cs", "네이밍 컨벤션", "Null 참조 체크"),
        ("Processor.cs", "리소스 관리", "Exception 처리"),
    ]

    for i, (file_name, category1, category2) in enumerate(mock_files, 1):
        # 모의 리포트 마크다운 생성
        report = f"""# C# 코드 리뷰 리포트

## 파일 정보
- **파일명**: {file_name}
- **분석 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 적용된 리뷰 카테고리

- ✅ **{category1}**
- ✅ **{category2}**

## 📝 코드 비교

### Before (원본 코드)

```csharp
public class Example {{
    public void Process() {{
        // Original code with issues
        var data = GetData(); // {category1} issue
        data.Execute(); // {category2} issue
    }}
}}
```

### After (개선된 코드)

```csharp
public class Example {{
    public void Process() {{
        // Improved code
        var data = GetData();
        if (data != null) {{
            data.Execute();
        }}
    }}
}}
```

## 💡 개선 사항

### {category1}
- 개선 사항 1
- 개선 사항 2

### {category2}
- 개선 사항 1
- 개선 사항 2
"""

        results.append(FileAnalysisResult(
            file_path=f"/project/{file_name}",
            file_name=file_name,
            success=True,
            original_code=f"// Original code for {file_name}",
            improved_code=f"// Improved code for {file_name}",
            report_markdown=report,
            analysis_time=2.5 + (i * 0.1)
        ))

    # 실패한 파일 2개 추가
    results.append(FileAnalysisResult(
        file_path="/project/Error1.cs",
        file_name="Error1.cs",
        success=False,
        error_message="파일 읽기 실패",
        analysis_time=0.1
    ))

    results.append(FileAnalysisResult(
        file_path="/project/Error2.cs",
        file_name="Error2.cs",
        success=False,
        error_message="인코딩 오류",
        analysis_time=0.1
    ))

    start_time = datetime.now()
    total_time = sum(r.analysis_time for r in results)

    return BatchAnalysisResult(
        total_files=len(results),
        success_count=20,
        failure_count=2,
        skipped_count=0,
        total_time=total_time,
        results=results,
        start_time=start_time,
        end_time=datetime.now()
    )


def main():
    """테스트 실행"""
    print("=" * 80)
    print("통합 리포트 생성기 테스트")
    print("=" * 80)
    print()

    # 1. 모의 배치 결과 생성
    print("📊 1단계: 모의 배치 분석 결과 생성...")
    batch_result = create_mock_batch_result()
    print(f"   ✅ 총 {batch_result.total_files}개 파일 (성공: {batch_result.success_count}, 실패: {batch_result.failure_count})")
    print()

    # 2. 통합 리포트 생성
    print("📝 2단계: 통합 리포트 생성...")
    generator = IntegratedReportGenerator()
    report_markdown = generator.generate_integrated_report(
        batch_result,
        project_name="테스트 프로젝트"
    )
    print("   ✅ 통합 리포트 생성 완료")
    print()

    # 3. 리포트 저장
    output_file = "test_integrated_report.md"
    print(f"💾 3단계: 리포트 저장 ({output_file})...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_markdown)
    print(f"   ✅ 저장 완료: {output_file}")
    print()

    # 4. 차트 생성
    print("📈 4단계: 카테고리별 이슈 분포 차트 생성...")
    from app.core.integrated_report_generator import IntegratedReportData, CategoryStatistics

    # 통합 데이터 수집
    report_data = generator._collect_report_data(batch_result, "테스트 프로젝트")

    chart_file = "test_integrated_report.png"
    chart_success = generator.generate_chart(report_data, chart_file)

    if chart_success:
        print(f"   ✅ 차트 생성 완료: {chart_file}")
    else:
        print("   ⚠️  차트 생성 실패 (matplotlib 없음 또는 오류)")
    print()

    # 5. 결과 요약
    print("=" * 80)
    print("📊 통합 리포트 요약")
    print("=" * 80)
    print()
    print(f"프로젝트명: {report_data.project_name}")
    print(f"분석 일시: {report_data.analysis_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"전체 파일: {report_data.total_files}개")
    print(f"성공: {report_data.success_files}개 | 실패: {report_data.failure_files}개")
    print(f"소요 시간: {report_data.total_time:.1f}초")
    print()

    print("📈 카테고리별 이슈:")
    for stat in report_data.category_stats:
        if stat.issue_count > 0:
            print(f"   • {stat.category_name}: {stat.issue_count}개 파일 ({stat.percentage:.1f}%)")
    print()

    print("🎯 개선 우선순위 (상위 3개):")
    for i, rec in enumerate(report_data.priority_recommendations[:3], 1):
        print(f"   {i}. {rec}")
    print()

    print("=" * 80)
    print("✅ 테스트 완료!")
    print("=" * 80)
    print()
    print(f"생성된 파일:")
    print(f"   • {output_file} (Markdown 리포트)")
    if chart_success:
        print(f"   • {chart_file} (차트 이미지)")
    print()


if __name__ == "__main__":
    main()
