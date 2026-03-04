#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub英语学习系统 - 前端功能测试
Phase 7: 测试与优化
"""

import sys
import pytest
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import GitHubEnglishLearningAPI


class TestFrontendFeatures:
    """前端功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前准备"""
        self.api = GitHubEnglishLearningAPI()
        self.user_id = 1
        yield
        # 测试后清理（如果需要）
    
    def test_01_vocabulary_learning_mode(self):
        """测试词汇学习模式"""
        # 测试新词汇获取
        new_words = self.api.get_learning_words(self.user_id, mode='new', limit=5)
        assert isinstance(new_words, list), "新词汇应该是列表"
        assert len(new_words) <= 5, "新词汇数量应不超过5"
        
        # 测试复习词汇获取
        review_words = self.api.get_learning_words(self.user_id, mode='review', limit=5)
        assert isinstance(review_words, list), "复习词汇应该是列表"
        
        # 测试弱项词汇获取
        weak_words = self.api.get_learning_words(self.user_id, mode='weak', limit=5)
        assert isinstance(weak_words, list), "弱项词汇应该是列表"
        
        print("✅ 词汇学习模式测试通过")
    
    def test_02_vocabulary_details(self):
        """测试词汇详情"""
        words = self.api.get_learning_words(self.user_id, mode='new', limit=1)
        
        if words:
            word = words[0]
            
            # 检查必要字段
            assert 'word' in word, "词汇应包含word字段"
            assert 'chinese' in word, "词汇应包含chinese字段"
            assert 'id' in word, "词汇应包含id字段"
            
            # 检查可选字段（增强版功能）
            optional_fields = ['phonetic', 'example', 'github_context', 'difficulty']
            for field in optional_fields:
                if field in word:
                    print(f"  ✓ 词汇包含{field}字段")
            
            print(f"✅ 词汇详情测试通过: {word['word']}")
        else:
            print("⚠️ 没有新词汇，跳过详情测试")
    
    def test_03_learning_result_submission(self):
        """测试学习结果提交"""
        words = self.api.get_learning_words(self.user_id, mode='new', limit=1)
        
        if words:
            word = words[0]
            
            # 测试正确答案
            result_correct = self.api.submit_learning_result(
                self.user_id,
                word['id'],
                True
            )
            assert 'mastery_level' in result_correct, "应返回掌握度"
            assert result_correct['mastery_level'] >= 0, "掌握度应>=0"
            
            # 测试错误答案
            result_wrong = self.api.submit_learning_result(
                self.user_id,
                word['id'],
                False
            )
            assert 'mastery_level' in result_wrong, "应返回掌握度"
            
            print("✅ 学习结果提交测试通过")
        else:
            print("⚠️ 没有新词汇，跳过提交测试")
    
    def test_04_reading_exercises(self):
        """测试阅读练习"""
        # 测试README练习
        readme_exercises = self.api.get_readme_exercises(difficulty=1, limit=1)
        assert isinstance(readme_exercises, list), "README练习应该是列表"
        
        if readme_exercises:
            exercise = readme_exercises[0]
            assert 'title' in exercise, "练习应包含title字段"
            assert 'content' in exercise, "练习应包含content字段"
            assert 'questions' in exercise, "练习应包含questions字段"
            print(f"  ✓ README练习: {exercise['title']}")
        
        # 测试Issue/PR练习
        issue_exercises = self.api.get_issue_pr_exercises(difficulty=1, limit=1)
        assert isinstance(issue_exercises, list), "Issue/PR练习应该是列表"
        
        # 测试代码注释练习
        code_exercises = self.api.get_code_comment_exercises(difficulty=1, limit=1)
        assert isinstance(code_exercises, list), "代码注释练习应该是列表"
        
        print("✅ 阅读练习测试通过")
    
    def test_05_test_generation(self):
        """测试生成测试"""
        # 测试词汇测试
        vocab_test = self.api.generate_vocabulary_test(
            self.user_id,
            category=None,
            difficulty=2,
            count=5
        )
        assert 'questions' in vocab_test, "词汇测试应包含questions字段"
        assert 'test_type' in vocab_test, "词汇测试应包含test_type字段"
        assert len(vocab_test['questions']) == 5, "词汇测试应有5题"
        
        # 测试阅读测试
        reading_test = self.api.generate_reading_test(difficulty=2, count=3)
        assert 'questions' in reading_test, "阅读测试应包含questions字段"
        
        # 测试综合考核
        comprehensive_test = self.api.generate_comprehensive_test(
            self.user_id,
            category=None
        )
        assert 'questions' in comprehensive_test, "综合考核应包含questions字段"
        
        print("✅ 测试生成功能测试通过")
    
    def test_06_test_submission(self):
        """测试提交测试"""
        # 生成测试
        test = self.api.generate_vocabulary_test(
            self.user_id,
            category=None,
            difficulty=2,
            count=5
        )
        
        # 准备答案（全选A）
        answers = [0] * 5
        
        # 提交测试
        result = self.api.submit_test(
            self.user_id,
            test['test_type'],
            answers,
            time_spent=120
        )
        
        assert 'score' in result, "应返回分数"
        assert 'passed' in result, "应返回是否通过"
        assert 'correct_count' in result, "应返回正确数量"
        
        print(f"✅ 测试提交功能测试通过（得分: {result['score']}）")
    
    def test_07_learning_stats(self):
        """测试学习统计"""
        stats = self.api.get_learning_stats(self.user_id)
        
        assert 'learned_words' in stats, "应包含已学词汇数"
        assert 'mastered_words' in stats, "应包含已掌握词汇数"
        assert 'avg_mastery' in stats, "应包含平均掌握度"
        assert 'total_reviews' in stats, "应包含总复习次数"
        
        print(f"✅ 学习统计测试通过（已学: {stats['learned_words']}词）")
    
    def test_08_test_statistics(self):
        """测试测试统计"""
        test_stats = self.api.get_test_statistics(self.user_id)
        
        assert 'total_tests' in test_stats, "应包含总测试次数"
        assert 'avg_score' in test_stats, "应包含平均分"
        assert 'passed_tests' in test_stats, "应包含通过次数"
        
        print(f"✅ 测试统计功能测试通过（总测试: {test_stats['total_tests']}次）")
    
    def test_09_today_plan(self):
        """测试今日学习计划"""
        plan = self.api.get_today_plan(self.user_id)
        
        assert 'total_words' in plan, "应包含总词汇数"
        assert 'completed_words' in plan, "应包含已完成词汇数"
        
        print(f"✅ 今日学习计划测试通过（目标: {plan['total_words']}词）")
    
    def test_10_learning_report(self):
        """测试学习报告"""
        report = self.api.generate_learning_report(self.user_id, days=7)
        
        assert 'total_words_learned' in report, "应包含总学习词汇数"
        assert 'total_reviews' in report, "应包含总复习次数"
        assert 'average_accuracy' in report, "应包含平均正确率"
        
        print(f"✅ 学习报告测试通过（7天学习: {report['total_words_learned']}词）")


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("GitHub英语学习系统 - 前端功能测试")
    print("=" * 60)
    print()
    
    # 运行pytest
    exit_code = pytest.main([__file__, "-v", "-s", "--tb=short"])
    
    print()
    print("=" * 60)
    if exit_code == 0:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(run_tests())
