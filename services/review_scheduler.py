#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复习提醒系统
生成每日复习计划、学习报告和进度通知
"""

import sqlite3
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple
import json
from pathlib import Path

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "data" / "github_english_learning.db"

class ReviewScheduler:
    """复习计划生成器"""
    
    def __init__(self, db_path=None):
        """初始化"""
        self.db_path = db_path or DB_PATH
        self.conn = None
    
    def connect(self):
        """连接数据库"""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # 使用字典方式访问
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def generate_daily_plan(
        self,
        user_id: int,
        daily_goal: int = 350
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
        
        Returns:
            {
                'date': date,
                'review_words': [word_ids],
                'new_words': [word_ids],
                'weak_words': [word_ids],
                'total_count': int
            }
        """
        self.connect()
        cursor = self.conn.cursor()
        
        today = date.today()
        
        # 1. 查询到期词汇（需要复习的词汇）
        cursor.execute("""
            SELECT v.id as word_id
            FROM vocabulary v
            LEFT JOIN learning_records lr ON v.id = lr.word_id AND lr.user_id = ?
            WHERE (lr.next_review_time IS NULL 
                   OR DATE(lr.next_review_time) <= ?)
               AND (lr.status IS NULL OR lr.status != 'mastered')
            ORDER BY lr.review_count ASC, v.difficulty ASC
            LIMIT ?
        """, (user_id, today, daily_goal))
        
        review_words = [row['word_id'] for row in cursor.fetchall()]
        
        # 2. 查询未学习的新词汇
        remaining_quota = daily_goal - len(review_words)
        if remaining_quota > 0:
            cursor.execute("""
                SELECT v.id as word_id
                FROM vocabulary v
                LEFT JOIN learning_records lr ON v.id = lr.word_id AND lr.user_id = ?
                WHERE lr.id IS NULL
                ORDER BY v.difficulty ASC, v.frequency DESC
                LIMIT ?
            """, (user_id, remaining_quota))
            
            new_words = [row['word_id'] for row in cursor.fetchall()]
        else:
            new_words = []
        
        # 3. 查询弱项词汇（正确率<60%）
        cursor.execute("""
            SELECT lr.word_id
            FROM learning_records lr
            WHERE lr.user_id = ?
              AND lr.review_count >= 3
              AND CAST(lr.correct_count AS REAL) / lr.review_count < 0.6
              AND lr.mastery_level < 3
            ORDER BY lr.wrong_count DESC
            LIMIT 50
        """, (user_id,))
        
        weak_words = [row['word_id'] for row in cursor.fetchall()]
        
        # 4. 保存复习计划到数据库
        total_count = len(review_words) + len(new_words)
        
        cursor.execute("""
            INSERT OR REPLACE INTO review_plans
            (user_id, review_date, word_ids, total_words, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            today,
            json.dumps({
                'review': review_words,
                'new': new_words,
                'weak': weak_words
            }),
            total_count,
            datetime.now()
        ))
        
        self.conn.commit()
        
        return {
            'date': today.isoformat(),
            'review_words': review_words,
            'new_words': new_words,
            'weak_words': weak_words,
            'total_count': total_count
        }
    
    def get_today_plan(self, user_id: int) -> Dict:
        """获取今日复习计划"""
        self.connect()
        cursor = self.conn.cursor()
        
        today = date.today()
        
        cursor.execute("""
            SELECT * FROM review_plans
            WHERE user_id = ? AND review_date = ?
        """, (user_id, today))
        
        row = cursor.fetchone()
        
        if row:
            word_ids = json.loads(row['word_ids'])
            return {
                'date': row['review_date'],
                'review_words': word_ids.get('review', []),
                'new_words': word_ids.get('new', []),
                'weak_words': word_ids.get('weak', []),
                'total_words': row['total_words'],
                'completed_words': row['completed_words'],
                'is_completed': bool(row['is_completed'])
            }
        else:
            # 如果没有计划，生成一个
            return self.generate_daily_plan(user_id)
    
    def update_learning_record(
        self,
        user_id: int,
        word_id: int,
        is_correct: bool,
        algorithm: str = 'ebbinghaus'
    ) -> Dict:
        """
        更新学习记录
        
        Args:
            user_id: 用户ID
            word_id: 词汇ID
            is_correct: 是否正确
            algorithm: 算法类型
        
        Returns:
            更新后的记录信息
        """
        self.connect()
        cursor = self.conn.cursor()
        
        # 获取当前记录
        cursor.execute("""
            SELECT * FROM learning_records
            WHERE user_id = ? AND word_id = ?
        """, (user_id, word_id))
        
        record = cursor.fetchone()
        
        now = datetime.now()
        
        if record:
            # 更新现有记录
            review_count = record['review_count'] + 1
            correct_count = record['correct_count'] + (1 if is_correct else 0)
            wrong_count = record['wrong_count'] + (0 if is_correct else 1)
            current_interval_index = record['current_interval_index']
            ease_factor = record['ease_factor']
            
            # 计算下次复习时间
            from algorithms.forgetting_curve import ForgettingCurveAlgorithm
            algo = ForgettingCurveAlgorithm()
            
            review_result = 'correct' if is_correct else 'wrong'
            next_review_time, new_interval_index, new_ease_factor = \
                algo.calculate_next_review_time(
                    current_interval_index, ease_factor, review_result, algorithm
                )
            
            # 计算掌握等级
            mastery_level = algo.calculate_mastery_level(
                review_count, correct_count, new_interval_index
            )
            
            # 更新记录
            cursor.execute("""
                UPDATE learning_records
                SET last_review_time = ?,
                    next_review_time = ?,
                    review_count = ?,
                    correct_count = ?,
                    wrong_count = ?,
                    mastery_level = ?,
                    last_review_result = ?,
                    current_interval_index = ?,
                    ease_factor = ?,
                    status = CASE 
                        WHEN mastery_level >= 5 THEN 'mastered'
                        WHEN review_count > 0 THEN 'reviewing'
                        ELSE 'learning'
                    END
                WHERE user_id = ? AND word_id = ?
            """, (
                now, next_review_time, review_count, correct_count, wrong_count,
                mastery_level, review_result, new_interval_index, new_ease_factor,
                user_id, word_id
            ))
            
        else:
            # 创建新记录
            from .forgetting_curve import ForgettingCurveAlgorithm
            algo = ForgettingCurveAlgorithm()
            
            review_result = 'correct' if is_correct else 'wrong'
            next_review_time, new_interval_index, new_ease_factor = \
                algo.calculate_next_review_time(0, 2.5, review_result, algorithm)
            
            mastery_level = algo.calculate_mastery_level(
                1, 1 if is_correct else 0, new_interval_index
            )
            
            cursor.execute("""
                INSERT INTO learning_records
                (user_id, word_id, first_learn_time, last_review_time,
                 next_review_time, review_count, correct_count, wrong_count,
                 mastery_level, last_review_result, current_interval_index,
                 ease_factor, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'learning')
            """, (
                user_id, word_id, now, now, next_review_time,
                1, 1 if is_correct else 0, 0 if is_correct else 1,
                mastery_level, review_result, new_interval_index, new_ease_factor
            ))
        
        self.conn.commit()
        
        # 返回更新后的信息
        return {
            'word_id': word_id,
            'is_correct': is_correct,
            'next_review_time': next_review_time.isoformat() if 'next_review_time' in locals() else None,
            'mastery_level': mastery_level if 'mastery_level' in locals() else 0
        }
    
    def generate_learning_report(
        self,
        user_id: int,
        days: int = 7
    ) -> Dict:
        """
        生成学习报告
        
        Args:
            user_id: 用户ID
            days: 统计天数
        
        Returns:
            {
                'period': str,
                'total_words_learned': int,
                'total_reviews': int,
                'average_accuracy': float,
                'mastery_distribution': dict,
                'daily_progress': list,
                'weak_areas': list
            }
        """
        self.connect()
        cursor = self.conn.cursor()
        
        start_date = date.today() - timedelta(days=days)
        
        # 1. 统计学习词汇数
        cursor.execute("""
            SELECT COUNT(DISTINCT word_id) as count
            FROM learning_records
            WHERE user_id = ?
              AND DATE(first_learn_time) >= ?
        """, (user_id, start_date))
        
        total_words_learned = cursor.fetchone()['count']
        
        # 2. 统计复习次数
        cursor.execute("""
            SELECT SUM(review_count) as total_reviews
            FROM learning_records
            WHERE user_id = ?
        """, (user_id,))
        
        total_reviews = cursor.fetchone()['total_reviews'] or 0
        
        # 3. 计算平均正确率
        cursor.execute("""
            SELECT 
                SUM(correct_count) as total_correct,
                SUM(review_count) as total_reviews
            FROM learning_records
            WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        total_correct = row['total_correct'] or 0
        total_review_count = row['total_reviews'] or 0
        average_accuracy = (total_correct / total_review_count 
                           if total_review_count > 0 else 0)
        
        # 4. 掌握等级分布
        cursor.execute("""
            SELECT mastery_level, COUNT(*) as count
            FROM learning_records
            WHERE user_id = ?
            GROUP BY mastery_level
            ORDER BY mastery_level
        """, (user_id,))
        
        mastery_distribution = {
            f"level_{row['mastery_level']}": row['count']
            for row in cursor.fetchall()
        }
        
        # 5. 每日进度
        cursor.execute("""
            SELECT 
                DATE(start_time) as study_date,
                COUNT(*) as session_count,
                SUM(words_learned) as words_learned,
                SUM(words_reviewed) as words_reviewed
            FROM study_sessions
            WHERE user_id = ?
              AND DATE(start_time) >= ?
            GROUP BY DATE(start_time)
            ORDER BY study_date
        """, (user_id, start_date))
        
        daily_progress = [
            {
                'date': row['study_date'],
                'sessions': row['session_count'],
                'words_learned': row['words_learned'],
                'words_reviewed': row['words_reviewed']
            }
            for row in cursor.fetchall()
        ]
        
        # 6. 弱项领域
        cursor.execute("""
            SELECT 
                v.category,
                COUNT(*) as weak_count
            FROM learning_records lr
            JOIN vocabulary v ON lr.word_id = v.id
            WHERE lr.user_id = ?
              AND lr.review_count >= 3
              AND CAST(lr.correct_count AS REAL) / lr.review_count < 0.6
            GROUP BY v.category
            ORDER BY weak_count DESC
        """, (user_id,))
        
        weak_areas = [
            {
                'category': row['category'],
                'weak_count': row['weak_count']
            }
            for row in cursor.fetchall()
        ]
        
        return {
            'period': f"Last {days} days",
            'total_words_learned': total_words_learned,
            'total_reviews': total_reviews,
            'average_accuracy': round(average_accuracy, 2),
            'mastery_distribution': mastery_distribution,
            'daily_progress': daily_progress,
            'weak_areas': weak_areas
        }
    
    def create_notification(
        self,
        user_id: int,
        notification_type: str,
        title: str,
        message: str
    ):
        """创建通知"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO notifications
            (user_id, notification_type, title, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, notification_type, title, message, datetime.now()))
        
        self.conn.commit()
    
    def get_unread_notifications(self, user_id: int) -> List[Dict]:
        """获取未读通知"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM notifications
            WHERE user_id = ? AND is_read = 0
            ORDER BY created_at DESC
        """, (user_id,))
        
        notifications = [
            {
                'id': row['id'],
                'type': row['notification_type'],
                'title': row['title'],
                'message': row['message'],
                'created_at': row['created_at']
            }
            for row in cursor.fetchall()
        ]
        
        return notifications


# 示例用法
if __name__ == "__main__":
    scheduler = ReviewScheduler()
    
    try:
        # 测试1: 生成每日计划
        print("=" * 60)
        print("Test 1: Generate Daily Plan")
        print("=" * 60)
        
        plan = scheduler.generate_daily_plan(user_id=1, daily_goal=350)
        print(f"Date: {plan['date']}")
        print(f"Review words: {len(plan['review_words'])}")
        print(f"New words: {len(plan['new_words'])}")
        print(f"Weak words: {len(plan['weak_words'])}")
        print(f"Total: {plan['total_count']}")
        
        # 测试2: 获取今日计划
        print("\n" + "=" * 60)
        print("Test 2: Get Today's Plan")
        print("=" * 60)
        
        today_plan = scheduler.get_today_plan(user_id=1)
        print(f"Total words: {today_plan['total_words']}")
        print(f"Completed: {today_plan['completed_words']}")
        
        # 测试3: 生成学习报告
        print("\n" + "=" * 60)
        print("Test 3: Generate Learning Report")
        print("=" * 60)
        
        report = scheduler.generate_learning_report(user_id=1, days=7)
        for key, value in report.items():
            print(f"{key}: {value}")
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    finally:
        scheduler.close()
