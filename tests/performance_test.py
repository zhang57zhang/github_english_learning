#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub英语学习系统 - 性能测试
Phase 7: 性能优化测试
"""

import sys
import time
import statistics
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import GitHubEnglishLearningAPI


class PerformanceTest:
    """性能测试类"""
    
    def __init__(self):
        self.api = GitHubEnglishLearningAPI()
        self.user_id = 1
        self.results = {}
    
    def measure_time(self, func, *args, **kwargs):
        """测量函数执行时间"""
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, (end - start) * 1000  # 转换为毫秒
    
    def test_vocabulary_learning_performance(self):
        """测试词汇学习性能"""
        print("\n📊 测试词汇学习性能...")
        
        times = []
        
        # 测试10次获取词汇
        for i in range(10):
            _, elapsed = self.measure_time(
                self.api.get_learning_words,
                self.user_id,
                mode='new',
                limit=10
            )
            times.append(elapsed)
        
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        
        self.results['vocabulary_learning'] = {
            'avg_ms': avg_time,
            'min_ms': min_time,
            'max_ms': max_time,
            'target_ms': 500
        }
        
        print(f"  ✓ 平均: {avg_time:.2f}ms")
        print(f"  ✓ 最小: {min_time:.2f}ms")
        print(f"  ✓ 最大: {max_time:.2f}ms")
        print(f"  ✓ 目标: <500ms")
        
        if avg_time < 500:
            print("  ✅ 性能达标")
        else:
            print("  ⚠️ 性能需要优化")
    
    def test_reading_exercises_performance(self):
        """测试阅读练习性能"""
        print("\n📊 测试阅读练习性能...")
        
        # 测试README练习
        _, readme_time = self.measure_time(
            self.api.get_readme_exercises,
            difficulty=1,
            limit=1
        )
        
        # 测试Issue/PR练习
        _, issue_time = self.measure_time(
            self.api.get_issue_pr_exercises,
            difficulty=1,
            limit=1
        )
        
        # 测试代码注释练习
        _, code_time = self.measure_time(
            self.api.get_code_comment_exercises,
            difficulty=1,
            limit=1
        )
        
        self.results['reading_exercises'] = {
            'readme_ms': readme_time,
            'issue_ms': issue_time,
            'code_ms': code_time,
            'target_ms': 500
        }
        
        print(f"  ✓ README练习: {readme_time:.2f}ms")
        print(f"  ✓ Issue/PR练习: {issue_time:.2f}ms")
        print(f"  ✓ 代码注释练习: {code_time:.2f}ms")
        print(f"  ✓ 目标: <500ms")
        
        if max(readme_time, issue_time, code_time) < 500:
            print("  ✅ 性能达标")
        else:
            print("  ⚠️ 性能需要优化")
    
    def test_test_generation_performance(self):
        """测试生成测试性能"""
        print("\n📊 测试生成测试性能...")
        
        # 测试词汇测试生成
        _, vocab_time = self.measure_time(
            self.api.generate_vocabulary_test,
            self.user_id,
            category=None,
            difficulty=2,
            count=20
        )
        
        # 测试阅读测试生成
        _, reading_time = self.measure_time(
            self.api.generate_reading_test,
            difficulty=2,
            count=10
        )
        
        # 测试综合考核生成
        _, comprehensive_time = self.measure_time(
            self.api.generate_comprehensive_test,
            self.user_id,
            category=None
        )
        
        self.results['test_generation'] = {
            'vocab_ms': vocab_time,
            'reading_ms': reading_time,
            'comprehensive_ms': comprehensive_time,
            'target_ms': 1000  # 生成测试可以稍慢
        }
        
        print(f"  ✓ 词汇测试: {vocab_time:.2f}ms")
        print(f"  ✓ 阅读测试: {reading_time:.2f}ms")
        print(f"  ✓ 综合考核: {comprehensive_time:.2f}ms")
        print(f"  ✓ 目标: <1000ms")
        
        if max(vocab_time, reading_time, comprehensive_time) < 1000:
            print("  ✅ 性能达标")
        else:
            print("  ⚠️ 性能需要优化")
    
    def test_statistics_performance(self):
        """测试统计功能性能"""
        print("\n📊 测试统计功能性能...")
        
        # 测试学习统计
        _, stats_time = self.measure_time(
            self.api.get_learning_stats,
            self.user_id
        )
        
        # 测试测试统计
        _, test_stats_time = self.measure_time(
            self.api.get_test_statistics,
            self.user_id
        )
        
        # 测试学习报告
        _, report_time = self.measure_time(
            self.api.generate_learning_report,
            self.user_id,
            days=7
        )
        
        self.results['statistics'] = {
            'stats_ms': stats_time,
            'test_stats_ms': test_stats_time,
            'report_ms': report_time,
            'target_ms': 300
        }
        
        print(f"  ✓ 学习统计: {stats_time:.2f}ms")
        print(f"  ✓ 测试统计: {test_stats_time:.2f}ms")
        print(f"  ✓ 学习报告: {report_time:.2f}ms")
        print(f"  ✓ 目标: <300ms")
        
        if max(stats_time, test_stats_time, report_time) < 300:
            print("  ✅ 性能达标")
        else:
            print("  ⚠️ 性能需要优化")
    
    def test_concurrent_requests(self):
        """测试并发请求性能（模拟）"""
        print("\n📊 测试并发请求性能...")
        
        # 模拟10次并发请求
        times = []
        
        for i in range(10):
            # 模拟用户同时进行多个操作
            start = time.time()
            
            # 同时执行3个操作
            self.api.get_learning_stats(self.user_id)
            self.api.get_today_plan(self.user_id)
            self.api.get_learning_words(self.user_id, mode='new', limit=5)
            
            end = time.time()
            times.append((end - start) * 1000)
        
        avg_time = statistics.mean(times)
        
        self.results['concurrent'] = {
            'avg_ms': avg_time,
            'target_ms': 800
        }
        
        print(f"  ✓ 平均: {avg_time:.2f}ms")
        print(f"  ✓ 目标: <800ms")
        
        if avg_time < 800:
            print("  ✅ 性能达标")
        else:
            print("  ⚠️ 性能需要优化")
    
    def generate_report(self):
        """生成性能测试报告"""
        print("\n" + "=" * 60)
        print("性能测试报告")
        print("=" * 60)
        
        all_passed = True
        
        for test_name, data in self.results.items():
            print(f"\n{test_name.upper()}:")
            
            if 'target_ms' in data:
                target = data['target_ms']
                
                if 'avg_ms' in data:
                    actual = data['avg_ms']
                    status = "✅ 达标" if actual < target else "⚠️ 需优化"
                    print(f"  平均响应时间: {actual:.2f}ms (目标: <{target}ms) {status}")
                    if actual >= target:
                        all_passed = False
                
                for key, value in data.items():
                    if key != 'target_ms' and key != 'avg_ms':
                        if isinstance(value, (int, float)):
                            print(f"  {key}: {value:.2f}ms")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ 所有性能指标达标！")
        else:
            print("⚠️ 部分性能指标需要优化")
        print("=" * 60)
        
        return all_passed
    
    def run_all_tests(self):
        """运行所有性能测试"""
        print("=" * 60)
        print("GitHub英语学习系统 - 性能测试")
        print("=" * 60)
        
        self.test_vocabulary_learning_performance()
        self.test_reading_exercises_performance()
        self.test_test_generation_performance()
        self.test_statistics_performance()
        self.test_concurrent_requests()
        
        return self.generate_report()


def main():
    """主函数"""
    tester = PerformanceTest()
    all_passed = tester.run_all_tests()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
