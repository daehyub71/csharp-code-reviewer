"""
Performance Benchmark Tests for Ollama Client

This script tests the performance of the Ollama client with different code sizes.
"""

import sys
import time
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.ollama_client import OllamaClient, OllamaClientError


# Test code samples
SMALL_CODE = """
public class HelloWorld
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
"""

MEDIUM_CODE = """
using System;
using System.Collections.Generic;

public class DataProcessor
{
    private List<string> data;

    public DataProcessor()
    {
        data = new List<string>();
    }

    public void AddData(string item)
    {
        if (item != null)
        {
            data.Add(item);
        }
    }

    public void ProcessData()
    {
        foreach (var item in data)
        {
            var result = item.ToUpper();
            Console.WriteLine(result);
        }
    }

    public int GetCount()
    {
        return data.Count;
    }

    public void Clear()
    {
        data.Clear();
    }
}
"""

LARGE_CODE = """
using System;
using System.Collections.Generic;
using System.Linq;

namespace CodeReviewExample
{
    public class UserManager
    {
        private Dictionary<int, User> users;
        private int nextId;

        public UserManager()
        {
            users = new Dictionary<int, User>();
            nextId = 1;
        }

        public int CreateUser(string name, string email)
        {
            var user = new User
            {
                Id = nextId++,
                Name = name,
                Email = email,
                CreatedAt = DateTime.Now
            };

            users[user.Id] = user;
            return user.Id;
        }

        public User GetUser(int id)
        {
            if (users.ContainsKey(id))
            {
                return users[id];
            }
            return null;
        }

        public List<User> GetAllUsers()
        {
            return users.Values.ToList();
        }

        public bool UpdateUser(int id, string name, string email)
        {
            if (users.ContainsKey(id))
            {
                users[id].Name = name;
                users[id].Email = email;
                users[id].UpdatedAt = DateTime.Now;
                return true;
            }
            return false;
        }

        public bool DeleteUser(int id)
        {
            return users.Remove(id);
        }

        public List<User> SearchUsers(string query)
        {
            return users.Values
                .Where(u => u.Name.Contains(query) || u.Email.Contains(query))
                .ToList();
        }
    }

    public class User
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }
    }
}
"""


def create_review_prompt(code: str) -> str:
    """Create a code review prompt."""
    return f"""
당신은 C# 코드 리뷰 전문가입니다. 다음 코드를 분석하고 주요 문제점을 간단히 나열해주세요.

코드:
```csharp
{code.strip()}
```

다음 항목을 검토해주세요:
1. Null 참조 가능성
2. Exception 처리
3. 리소스 해제
4. 성능 이슈
5. 보안 취약점
6. 네이밍 컨벤션

주요 문제점만 간단히 나열해주세요 (최대 5줄).
"""


def measure_performance(client: OllamaClient, code: str, code_name: str) -> dict:
    """
    Measure performance of code analysis.

    Args:
        client: OllamaClient instance
        code: Code to analyze
        code_name: Name of the code sample

    Returns:
        dict: Performance metrics
    """
    prompt = create_review_prompt(code)
    prompt_length = len(prompt)
    code_lines = len(code.strip().split('\n'))

    print(f"\n{'='*60}")
    print(f"Testing: {code_name}")
    print(f"Code lines: {code_lines}")
    print(f"Prompt length: {prompt_length} chars")
    print(f"{'='*60}\n")

    # Measure streaming response time
    start_time = time.time()
    response_tokens = 0

    try:
        for token in client.analyze_code(prompt, stream=True):
            response_tokens += 1
            # Print first 100 chars
            if response_tokens == 1:
                print("Response preview:", end=" ")
            if response_tokens <= 50:
                print(token, end='', flush=True)

        print("...\n")

        elapsed = time.time() - start_time

        return {
            'code_name': code_name,
            'code_lines': code_lines,
            'prompt_length': prompt_length,
            'response_tokens': response_tokens,
            'elapsed_time': elapsed,
            'success': True
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n✗ Error: {e}\n")

        return {
            'code_name': code_name,
            'code_lines': code_lines,
            'prompt_length': prompt_length,
            'response_tokens': 0,
            'elapsed_time': elapsed,
            'success': False,
            'error': str(e)
        }


def print_summary(results: list):
    """Print performance summary."""
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60 + "\n")

    print(f"{'Test':<20} {'Lines':<8} {'Time (s)':<12} {'Tokens':<10} {'Status':<10}")
    print("-" * 60)

    total_time = 0
    successful = 0

    for result in results:
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        print(f"{result['code_name']:<20} "
              f"{result['code_lines']:<8} "
              f"{result['elapsed_time']:>8.2f}    "
              f"{result['response_tokens']:>8}  "
              f"{status:<10}")

        if result['success']:
            total_time += result['elapsed_time']
            successful += 1

    print("-" * 60)
    print(f"\nSuccessful tests: {successful}/{len(results)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time: {total_time/successful if successful > 0 else 0:.2f}s")

    # Check performance targets
    print("\n" + "="*60)
    print("PERFORMANCE TARGETS")
    print("="*60)

    targets_met = True

    for result in results:
        if not result['success']:
            continue

        if result['code_lines'] <= 10:
            target = 2.0
            status = "✓" if result['elapsed_time'] <= target else "✗"
            targets_met = targets_met and (result['elapsed_time'] <= target)
            print(f"{status} {result['code_name']}: {result['elapsed_time']:.2f}s (target: <{target}s)")

        elif result['code_lines'] <= 50:
            target = 5.0
            status = "✓" if result['elapsed_time'] <= target else "✗"
            targets_met = targets_met and (result['elapsed_time'] <= target)
            print(f"{status} {result['code_name']}: {result['elapsed_time']:.2f}s (target: <{target}s)")

        elif result['code_lines'] <= 100:
            target = 20.0
            status = "✓" if result['elapsed_time'] <= target else "✗"
            targets_met = targets_met and (result['elapsed_time'] <= target)
            print(f"{status} {result['code_name']}: {result['elapsed_time']:.2f}s (target: <{target}s)")

    print("\n" + "="*60)
    if targets_met and successful == len(results):
        print("✓ ALL PERFORMANCE TARGETS MET!")
    else:
        print("✗ Some targets not met or tests failed")
    print("="*60 + "\n")


def main():
    """Run performance benchmarks."""
    print("="*60)
    print("OLLAMA CLIENT PERFORMANCE BENCHMARK")
    print("="*60)

    # Initialize client
    try:
        client = OllamaClient(model_name="phi3:mini")
        print("\n✓ OllamaClient initialized")

        # Test connection
        client.test_connection()
        print("✓ Connection test passed")

    except OllamaClientError as e:
        print(f"\n✗ Initialization failed: {e}")
        return 1

    # Run benchmarks
    results = []

    # Small code (~10 lines)
    result = measure_performance(client, SMALL_CODE, "Small (10 lines)")
    results.append(result)

    # Medium code (~40 lines)
    result = measure_performance(client, MEDIUM_CODE, "Medium (40 lines)")
    results.append(result)

    # Large code (~100 lines)
    result = measure_performance(client, LARGE_CODE, "Large (100 lines)")
    results.append(result)

    # Print summary
    print_summary(results)

    # Return exit code
    all_passed = all(r['success'] for r in results)
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
