#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub英语学习系统 - 统一API入口
整合所有模块的API接口
"""

from pathlib import Path
from typing import Dict, List, Optional

# 导入各模块API
from backend.vocabulary_learning import VocabularyLearningAPI
from backend.reading_comprehension import ReadingComprehensionAPI
from backend.test_assessment import TestAssessmentAPI
from services.review_scheduler import ReviewScheduler
from algorithms.forgetting_curve import ForgettingCurveAlgorithm

DB_PATH = Path(__file__).parent / "data" / "github_english_learning.db"

class GitHubEnglishLearningAPI:
    """GitHub英语学习系统统一API"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        
        # 初始化各模块API
        self.vocabulary = VocabularyLearningAPI(self.db_path)
        self.reading = ReadingComprehensionAPI(self.db_path)
        self.test = TestAssessmentAPI(self.db_path)
        self.scheduler = ReviewScheduler(self.db_path)
        self.algorithm = ForgettingCurveAlgorithm()
    
    def close(self):
        """关闭所有连接"""
        self.vocabulary.close()
        self.reading.close()
        self.test.close()
        self.scheduler.close()
    
    # ==================== 词汇学习API ====================
    
    def get_word(self, word_id: int) -> Optional[Dict]:
        """获取词汇详情"""
        return self.vocabulary.get_word(word_id)
    
    def get_learning_words(self, user_id: int, mode: str = 'new', limit: int = 20) -> List[Dict]:
        """获取学习词汇"""
        return self.vocabulary.get_learning_words(user_id, mode, limit)
    
    def submit_learning_result(self, user_id: int, word_id: int, is_correct: bool) -> Dict:
        """提交学习结果"""
        return self.vocabulary.submit_learning_result(user_id, word_id, is_correct)
    
    def get_learning_stats(self, user_id: int) -> Dict:
        """获取学习统计"""
        return self.vocabulary.get_learning_stats(user_id)
    
    def search_words(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """搜索词汇"""
        return self.vocabulary.search_words(query, category)
    
    # ==================== 阅读理解API ====================
    
    def get_readme_exercises(self, difficulty: int = 1, limit: int = 10) -> List[Dict]:
        """获取README练习"""
        return self.reading.get_readme_exercises(difficulty, limit)
    
    def get_issue_pr_exercises(self, difficulty: int = 1, limit: int = 10) -> List[Dict]:
        """获取Issue/PR练习"""
        return self.reading.get_issue_pr_exercises(difficulty, limit)
    
    def get_code_comment_exercises(self, difficulty: int = 1, limit: int = 10) -> List[Dict]:
        """获取代码注释练习"""
        return self.reading.get_code_comment_exercises(difficulty, limit)
    
    def get_random_exercise(self, difficulty: int = 1, limit: int = 1) -> Dict:
        """获取随机练习"""
        return self.reading.get_random_exercise(difficulty, limit)
    
    # ==================== 测试评估API ====================
    
    def generate_vocabulary_test(self, user_id: int, category: Optional[str] = None, 
                                 difficulty: Optional[int] = None, count: int = 20) -> Dict:
        """生成词汇测试"""
        return self.test.generate_vocabulary_test(user_id, category, difficulty, count)
    
    def generate_reading_test(self, difficulty: int = 1, count: int = 10) -> Dict:
        """生成阅读测试"""
        return self.test.generate_reading_test(difficulty, count)
    
    def generate_comprehensive_test(self, user_id: int, category: Optional[str] = None) -> Dict:
        """生成综合考核"""
        return self.test.generate_comprehensive_test(user_id, category)
    
    def submit_test(self, user_id: int, test_type: str, answers: List[int], time_spent: int = 0) -> Dict:
        """提交测试"""
        return self.test.submit_test(user_id, test_type, answers, time_spent)
    
    def get_test_history(self, user_id: int, test_type: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """获取测试历史"""
        return self.test.get_test_history(user_id, test_type, limit)
    
    def get_test_statistics(self, user_id: int) -> Dict:
        """获取测试统计"""
        return self.test.get_test_statistics(user_id)
    
    # ==================== 复习计划API ====================
    
    def generate_daily_plan(self, user_id: int, daily_goal: int = 350) -> Dict:
        """生成每日计划"""
        return self.scheduler.generate_daily_plan(user_id, daily_goal)
    
    def get_today_plan(self, user_id: int) -> Dict:
        """获取今日计划"""
        return self.scheduler.get_today_plan(user_id)
    
    def generate_learning_report(self, user_id: int, days: int = 7) -> Dict:
        """生成学习报告"""
        return self.scheduler.generate_learning_report(user_id, days)
    
    # ==================== 遗忘曲线算法API ====================
    
    def calculate_next_review(self, current_index: int, review_result: str, algorithm: str = 'ebbinghaus') -> Dict:
        """计算下次复习时间"""
        next_time, new_index, new_ease = self.algorithm.calculate_next_review_time(
            current_index, 2.5, review_result, algorithm
        )
        return {
            "next_review_time": next_time.isoformat(),
            "new_interval_index": new_index,
            "ease_factor": new_ease
        }
    
    def calculate_mastery_level(self, review_count: int, correct_count: int, interval_index: int) -> int:
        """计算掌握等级"""
        return self.algorithm.calculate_mastery_level(review_count, correct_count, interval_index)
    
    def identify_weak_words(self, learning_records: List[Dict]) -> List[int]:
        """识别弱项词汇"""
        return self.algorithm.identify_weak_words(learning_records)


# 综合测试
if __name__ == "__main__":
    print("=" * 60)
    print("GitHub English Learning System - API Test")
    print("=" * 60)
    
    api = GitHubEnglishLearningAPI()
    
    try:
        # 测试1: 词汇学习
        print("\n[Test 1] Vocabulary Learning")
        words = api.get_learning_words(user_id=1, mode='new', limit=5)
        print(f"New words: {len(words)}")
        
        if words:
            word = words[0]
            print(f"Sample: {word['word']} - {word['chinese']}")
        
        # 测试2: 阅读理解
        print("\n[Test 2] Reading Comprehension")
        exercises = api.get_readme_exercises(difficulty=1)
        print(f"README exercises: {len(exercises)}")
        
        if exercises:
            ex = exercises[0]
            print(f"Title: {ex['title']}")
        
        # 测试3: 测试评估
        print("\n[Test 3] Test Assessment")
        test = api.generate_vocabulary_test(user_id=1, count=5)
        print(f"Vocabulary test: {test['question_count']} questions")
        
        # 测试4: 复习计划
        print("\n[Test 4] Review Plan")
        plan = api.get_today_plan(user_id=1)
        print(f"Today's plan: {plan['total_words']} words")
        
        # 测试5: 学习统计
        print("\n[Test 5] Learning Statistics")
        stats = api.get_learning_stats(user_id=1)
        print(f"Learned: {stats['learned_words']}, Mastered: {stats['mastered_words']}")
        
        # 测试6: 遗忘曲线
        print("\n[Test 6] Forgetting Curve")
        result = api.calculate_next_review(0, 'correct', 'ebbinghaus')
        print(f"Next review: {result['new_interval_index']} intervals later")
        
        print("\n" + "=" * 60)
        print("All API tests passed!")
        print("=" * 60)
        
    finally:
        api.close()
