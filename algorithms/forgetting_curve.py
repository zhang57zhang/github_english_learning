#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遗忘曲线算法模块
实现艾宾浩斯记忆曲线和SM-2算法
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import math

class ForgettingCurveAlgorithm:
    """遗忘曲线算法"""
    
    # 艾宾浩斯遗忘曲线标准间隔（天）
    EBBINGHAUS_INTERVALS = [1, 2, 4, 7, 15, 30, 60, 120]
    
    # SM-2算法参数
    MIN_EASE_FACTOR = 1.3
    DEFAULT_EASE_FACTOR = 2.5
    
    def __init__(self):
        """初始化算法"""
        pass
    
    def calculate_next_review_time(
        self,
        current_interval_index: int,
        ease_factor: float = 2.5,
        review_result: str = 'correct',
        algorithm: str = 'ebbinghaus'
    ) -> Tuple[datetime, int, float]:
        """
        计算下次复习时间
        
        Args:
            current_interval_index: 当前间隔索引
            ease_factor: 难度因子（SM-2算法）
            review_result: 复习结果 ('correct', 'wrong', 'partial')
            algorithm: 算法类型 ('ebbinghaus', 'sm2')
        
        Returns:
            (next_review_time, new_interval_index, new_ease_factor)
        """
        if algorithm == 'ebbinghaus':
            return self._ebbinghaus_algorithm(
                current_interval_index, review_result
            )
        elif algorithm == 'sm2':
            return self._sm2_algorithm(
                current_interval_index, ease_factor, review_result
            )
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def _ebbinghaus_algorithm(
        self,
        current_interval_index: int,
        review_result: str
    ) -> Tuple[datetime, int, float]:
        """
        艾宾浩斯遗忘曲线算法
        
        标准间隔：1, 2, 4, 7, 15, 30, 60, 120天
        
        规则：
        - 正确：进入下一个间隔
        - 部分正确：保持当前间隔
        - 错误：回退1-2个间隔
        """
        if review_result == 'correct':
            # 进入下一个间隔
            new_index = min(current_interval_index + 1, 
                          len(self.EBBINGHAUS_INTERVALS) - 1)
            interval_days = self.EBBINGHAUS_INTERVALS[new_index]
        
        elif review_result == 'partial':
            # 保持当前间隔
            new_index = current_interval_index
            interval_days = self.EBBINGHAUS_INTERVALS[new_index]
        
        else:  # wrong
            # 回退1-2个间隔
            new_index = max(0, current_interval_index - 2)
            interval_days = self.EBBINGHAUS_INTERVALS[new_index]
        
        next_review_time = datetime.now() + timedelta(days=interval_days)
        
        return next_review_time, new_index, self.DEFAULT_EASE_FACTOR
    
    def _sm2_algorithm(
        self,
        current_interval_index: int,
        ease_factor: float,
        review_result: str
    ) -> Tuple[datetime, int, float]:
        """
        SM-2算法（SuperMemo 2）
        
        基于难度因子动态调整复习间隔
        
        规则：
        - 正确：interval = previous_interval * ease_factor
        - 部分正确：interval保持不变，ease_factor略微降低
        - 错误：interval重置为1天，ease_factor大幅降低
        """
        # 根据复习结果调整难度因子
        if review_result == 'correct':
            # 增加难度因子
            quality = 5  # 完美回忆
            new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            new_ease_factor = max(self.MIN_EASE_FACTOR, new_ease_factor)
            
            # 计算新间隔
            if current_interval_index == 0:
                interval_days = 1
            elif current_interval_index == 1:
                interval_days = 6
            else:
                # 从上一次的间隔计算
                prev_interval = self.EBBINGHAUS_INTERVALS[min(current_interval_index - 1, 
                                                               len(self.EBBINGHAUS_INTERVALS) - 1)]
                interval_days = int(prev_interval * new_ease_factor)
            
            new_index = current_interval_index + 1
        
        elif review_result == 'partial':
            # 轻微降低难度因子
            quality = 3  # 勉强回忆
            new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            new_ease_factor = max(self.MIN_EASE_FACTOR, new_ease_factor)
            
            # 保持间隔不变
            interval_days = self.EBBINGHAUS_INTERVALS[current_interval_index]
            new_index = current_interval_index
        
        else:  # wrong
            # 大幅降低难度因子
            quality = 0  # 完全忘记
            new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            new_ease_factor = max(self.MIN_EASE_FACTOR, new_ease_factor)
            
            # 重置间隔为1天
            interval_days = 1
            new_index = 0
        
        next_review_time = datetime.now() + timedelta(days=interval_days)
        
        return next_review_time, new_index, new_ease_factor
    
    def calculate_mastery_level(
        self,
        review_count: int,
        correct_count: int,
        current_interval_index: int
    ) -> int:
        """
        计算掌握等级 (0-5)
        
        掌握等级规则：
        - Level 0: 未学习
        - Level 1: 学习1次
        - Level 2: 正确率>50% 或 复习>3次
        - Level 3: 正确率>70% 或 间隔索引>=2
        - Level 4: 正确率>85% 或 间隔索引>=4
        - Level 5: 正确率>95% 且 间隔索引>=6 (已掌握)
        
        Args:
            review_count: 复习次数
            correct_count: 正确次数
            current_interval_index: 当前间隔索引
        
        Returns:
            掌握等级 (0-5)
        """
        if review_count == 0:
            return 0
        
        # 计算正确率
        accuracy = correct_count / review_count if review_count > 0 else 0
        
        # 根据规则计算掌握等级
        if current_interval_index >= 6 and accuracy > 0.95:
            return 5  # 已掌握
        elif current_interval_index >= 4 and accuracy > 0.85:
            return 4  # 接近掌握
        elif current_interval_index >= 2 and accuracy > 0.70:
            return 3  # 熟悉
        elif review_count > 3 and accuracy > 0.50:
            return 2  # 理解
        elif review_count >= 1:
            return 1  # 初学
        else:
            return 0  # 未学习
    
    def identify_weak_words(
        self,
        learning_records: List[Dict]
    ) -> List[int]:
        """
        识别弱项词汇
        
        弱项词汇判定标准：
        1. 正确率 < 60%
        2. 连续错误次数 >= 3
        3. 复习次数 >= 5 但掌握等级 < 3
        4. 长期停留在低间隔索引
        
        Args:
            learning_records: 学习记录列表
        
        Returns:
            弱项词汇ID列表
        """
        weak_words = []
        
        for record in learning_records:
            word_id = record.get('word_id')
            review_count = record.get('review_count', 0)
            correct_count = record.get('correct_count', 0)
            wrong_count = record.get('wrong_count', 0)
            mastery_level = record.get('mastery_level', 0)
            current_interval_index = record.get('current_interval_index', 0)
            
            # 计算正确率
            accuracy = correct_count / review_count if review_count > 0 else 0
            
            # 判定是否为弱项
            is_weak = False
            
            # 标准1: 正确率 < 60%
            if review_count >= 3 and accuracy < 0.60:
                is_weak = True
            
            # 标准2: 连续错误次数 >= 3
            if wrong_count >= 3 and correct_count == 0:
                is_weak = True
            
            # 标准3: 复习次数 >= 5 但掌握等级 < 3
            if review_count >= 5 and mastery_level < 3:
                is_weak = True
            
            # 标准4: 复习次数 >= 10 但间隔索引仍为0
            if review_count >= 10 and current_interval_index == 0:
                is_weak = True
            
            if is_weak:
                weak_words.append(word_id)
        
        return weak_words
    
    def generate_review_plan(
        self,
        user_id: int,
        daily_goal: int = 350,
        algorithm: str = 'ebbinghaus'
    ) -> Dict:
        """
        生成每日复习计划
        
        策略：
        1. 优先复习到期词汇（next_review_time <= today）
        2. 混合新词汇学习
        3. 包含弱项词汇强化
        4. 总量控制在daily_goal
        
        Args:
            user_id: 用户ID
            daily_goal: 每日目标词汇数
            algorithm: 算法类型
        
        Returns:
            {
                'review_words': [word_ids],  # 复习词汇
                'new_words': [word_ids],      # 新词汇
                'weak_words': [word_ids],     # 弱项词汇
                'total_count': int            # 总词汇数
            }
        """
        # 这里需要从数据库查询，暂时返回示例
        # 实际实现时需要连接数据库
        
        plan = {
            'review_words': [],
            'new_words': [],
            'weak_words': [],
            'total_count': 0
        }
        
        # TODO: 实现数据库查询
        # 1. 查询到期词汇
        # 2. 查询未学习词汇
        # 3. 查询弱项词汇
        # 4. 组合生成计划
        
        return plan
    
    def get_review_statistics(
        self,
        learning_records: List[Dict]
    ) -> Dict:
        """
        获取复习统计信息
        
        Args:
            learning_records: 学习记录列表
        
        Returns:
            {
                'total_words': int,
                'learned_words': int,
                'mastered_words': int,
                'average_accuracy': float,
                'average_mastery_level': float,
                'weak_words_count': int
            }
        """
        if not learning_records:
            return {
                'total_words': 0,
                'learned_words': 0,
                'mastered_words': 0,
                'average_accuracy': 0.0,
                'average_mastery_level': 0.0,
                'weak_words_count': 0
            }
        
        total_words = len(learning_records)
        learned_words = sum(1 for r in learning_records if r.get('review_count', 0) > 0)
        mastered_words = sum(1 for r in learning_records if r.get('mastery_level', 0) >= 5)
        
        total_reviews = sum(r.get('review_count', 0) for r in learning_records)
        total_correct = sum(r.get('correct_count', 0) for r in learning_records)
        average_accuracy = total_correct / total_reviews if total_reviews > 0 else 0
        
        total_mastery = sum(r.get('mastery_level', 0) for r in learning_records)
        average_mastery_level = total_mastery / total_words if total_words > 0 else 0
        
        weak_words = self.identify_weak_words(learning_records)
        weak_words_count = len(weak_words)
        
        return {
            'total_words': total_words,
            'learned_words': learned_words,
            'mastered_words': mastered_words,
            'average_accuracy': round(average_accuracy, 2),
            'average_mastery_level': round(average_mastery_level, 2),
            'weak_words_count': weak_words_count
        }


# 示例用法
if __name__ == "__main__":
    algorithm = ForgettingCurveAlgorithm()
    
    # 测试1: 计算下次复习时间
    print("=" * 60)
    print("测试1: 计算下次复习时间")
    print("=" * 60)
    
    next_review, new_index, new_ease = algorithm.calculate_next_review_time(
        current_interval_index=0,
        review_result='correct',
        algorithm='ebbinghaus'
    )
    print(f"下次复习时间: {next_review}")
    print(f"新间隔索引: {new_index}")
    print(f"难度因子: {new_ease}")
    
    # 测试2: 计算掌握等级
    print("\n" + "=" * 60)
    print("测试2: 计算掌握等级")
    print("=" * 60)
    
    mastery = algorithm.calculate_mastery_level(
        review_count=10,
        correct_count=9,
        current_interval_index=3
    )
    print(f"掌握等级: {mastery}")
    
    # 测试3: 识别弱项词汇
    print("\n" + "=" * 60)
    print("测试3: 识别弱项词汇")
    print("=" * 60)
    
    test_records = [
        {'word_id': 1, 'review_count': 5, 'correct_count': 2, 'wrong_count': 3, 
         'mastery_level': 1, 'current_interval_index': 0},
        {'word_id': 2, 'review_count': 10, 'correct_count': 9, 'wrong_count': 1, 
         'mastery_level': 4, 'current_interval_index': 5},
        {'word_id': 3, 'review_count': 8, 'correct_count': 3, 'wrong_count': 5, 
         'mastery_level': 2, 'current_interval_index': 1}
    ]
    
    weak_words = algorithm.identify_weak_words(test_records)
    print(f"弱项词汇ID: {weak_words}")
    
    # 测试4: 获取统计信息
    print("\n" + "=" * 60)
    print("测试4: 获取统计信息")
    print("=" * 60)
    
    stats = algorithm.get_review_statistics(test_records)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)
