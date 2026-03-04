#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词汇学习模块API
提供词汇学习、复习、查询等功能
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional

DB_PATH = Path(__file__).parent.parent / "data" / "github_english_learning.db"

class VocabularyLearningAPI:
    """词汇学习API"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self.conn = None
    
    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def get_word(self, word_id: int) -> Optional[Dict]:
        """获取单个词汇详情"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM vocabulary WHERE id = ?
        """, (word_id,))
        
        row = cursor.fetchone()
        if row:
            word_dict = dict(row)
            # 解析JSON字段
            if word_dict.get('synonyms') and isinstance(word_dict['synonyms'], str):
                try:
                    word_dict['synonyms'] = json.loads(word_dict['synonyms'])
                except:
                    word_dict['synonyms'] = []
            if word_dict.get('antonyms') and isinstance(word_dict['antonyms'], str):
                try:
                    word_dict['antonyms'] = json.loads(word_dict['antonyms'])
                except:
                    word_dict['antonyms'] = []
            return word_dict
        return None
    
    def get_words_by_category(
        self, 
        category: str, 
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """按类别获取词汇列表"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM vocabulary
            WHERE category = ?
            ORDER BY difficulty, frequency DESC
            LIMIT ? OFFSET ?
        """, (category, limit, offset))
        
        words = [dict(row) for row in cursor.fetchall()]
        return [self._parse_word_json(word) for word in words]
    
    def get_learning_words(
        self,
        user_id: int,
        mode: str = 'new',
        limit: int = 20
    ) -> List[Dict]:
        """
        获取学习词汇
        
        mode: 'new' - 新词汇, 'review' - 复习词汇, 'weak' - 弱项词汇
        """
        self.connect()
        cursor = self.conn.cursor()
        
        if mode == 'new':
            # 获取未学习的词汇
            cursor.execute("""
                SELECT v.* FROM vocabulary v
                LEFT JOIN learning_records lr ON v.id = lr.word_id AND lr.user_id = ?
                WHERE lr.id IS NULL
                ORDER BY v.difficulty, v.frequency DESC
                LIMIT ?
            """, (user_id, limit))
        
        elif mode == 'review':
            # 获取需要复习的词汇
            cursor.execute("""
                SELECT v.*, lr.mastery_level, lr.review_count
                FROM vocabulary v
                JOIN learning_records lr ON v.id = lr.word_id
                WHERE lr.user_id = ?
                  AND DATE(lr.next_review_time) <= DATE('now')
                  AND lr.status != 'mastered'
                ORDER BY lr.next_review_time ASC
                LIMIT ?
            """, (user_id, limit))
        
        elif mode == 'weak':
            # 获取弱项词汇
            cursor.execute("""
                SELECT v.*, lr.mastery_level, lr.review_count, lr.correct_count
                FROM vocabulary v
                JOIN learning_records lr ON v.id = lr.word_id
                WHERE lr.user_id = ?
                  AND lr.review_count >= 3
                  AND CAST(lr.correct_count AS REAL) / lr.review_count < 0.6
                ORDER BY lr.wrong_count DESC
                LIMIT ?
            """, (user_id, limit))
        
        words = [dict(row) for row in cursor.fetchall()]
        # 解析JSON字段
        return [self._parse_word_json(word) for word in words]
    
    def _parse_word_json(self, word_dict: Dict) -> Dict:
        """解析词汇的JSON字段"""
        if word_dict.get('synonyms') and isinstance(word_dict['synonyms'], str):
            try:
                word_dict['synonyms'] = json.loads(word_dict['synonyms'])
            except:
                word_dict['synonyms'] = []
        if word_dict.get('antonyms') and isinstance(word_dict['antonyms'], str):
            try:
                word_dict['antonyms'] = json.loads(word_dict['antonyms'])
            except:
                word_dict['antonyms'] = []
        return word_dict
    
    def submit_learning_result(
        self,
        user_id: int,
        word_id: int,
        is_correct: bool,
        mode: str = 'learning'
    ) -> Dict:
        """提交学习结果"""
        from services.review_scheduler import ReviewScheduler
        
        scheduler = ReviewScheduler(self.db_path)
        try:
            result = scheduler.update_learning_record(
                user_id, word_id, is_correct
            )
            
            # 更新今日计划进度
            self._update_plan_progress(user_id)
            
            return {
                'success': True,
                'word_id': word_id,
                'is_correct': is_correct,
                'next_review': result.get('next_review_time'),
                'mastery_level': result.get('mastery_level', 0)
            }
        finally:
            scheduler.close()
    
    def _update_plan_progress(self, user_id: int):
        """更新计划进度"""
        self.connect()
        cursor = self.conn.cursor()
        
        today = date.today()
        cursor.execute("""
            UPDATE review_plans
            SET completed_words = completed_words + 1
            WHERE user_id = ? AND review_date = ?
        """, (user_id, today))
        
        self.conn.commit()
    
    def get_learning_stats(self, user_id: int) -> Dict:
        """获取学习统计"""
        self.connect()
        cursor = self.conn.cursor()
        
        # 总体统计
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT word_id) as learned_words,
                COUNT(CASE WHEN mastery_level >= 5 THEN 1 END) as mastered_words,
                AVG(mastery_level) as avg_mastery,
                SUM(review_count) as total_reviews
            FROM learning_records
            WHERE user_id = ?
        """, (user_id,))
        
        stats = dict(cursor.fetchone())
        
        # 今日进度
        cursor.execute("""
            SELECT total_words, completed_words
            FROM review_plans
            WHERE user_id = ? AND review_date = DATE('now')
        """, (user_id,))
        
        today = cursor.fetchone()
        if today:
            stats['today_total'] = today['total_words']
            stats['today_completed'] = today['completed_words']
        else:
            stats['today_total'] = 0
            stats['today_completed'] = 0
        
        return stats
    
    def search_words(
        self,
        query: str,
        category: Optional[str] = None,
        difficulty: Optional[int] = None
    ) -> List[Dict]:
        """搜索词汇"""
        self.connect()
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM vocabulary WHERE word LIKE ?"
        params = [f"%{query}%"]
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        if difficulty:
            sql += " AND difficulty = ?"
            params.append(difficulty)
        
        sql += " ORDER BY frequency DESC LIMIT 50"
        
        cursor.execute(sql, params)
        words = [dict(row) for row in cursor.fetchall()]
        return [self._parse_word_json(word) for word in words]


# 测试
if __name__ == "__main__":
    api = VocabularyLearningAPI()
    
    print("=" * 60)
    print("Vocabulary Learning API Test")
    print("=" * 60)
    
    # 测试1: 获取词汇
    print("\n[Test 1] Get Word")
    word = api.get_word(1)
    print(f"Word: {word['word']}, Chinese: {word['chinese']}")
    
    # 测试2: 按类别获取
    print("\n[Test 2] Get Words by Category")
    words = api.get_words_by_category("Python技术词汇", limit=5)
    print(f"Found {len(words)} words")
    
    # 测试3: 获取新词汇
    print("\n[Test 3] Get New Words")
    new_words = api.get_learning_words(user_id=1, mode='new', limit=10)
    print(f"New words: {len(new_words)}")
    
    # 测试4: 搜索
    print("\n[Test 4] Search Words")
    results = api.search_words("function")
    print(f"Search results: {len(results)}")
    
    api.close()
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
