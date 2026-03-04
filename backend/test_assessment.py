#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试评估模块API
提供词汇测试、阅读理解测试、综合考核等功能
"""

import sqlite3
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DB_PATH = Path(__file__).parent.parent / "data" / "github_english_learning.db"

class TestAssessmentAPI:
    """测试评估API"""
    
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
    
    def generate_vocabulary_test(
        self,
        user_id: int,
        category: Optional[str] = None,
        difficulty: Optional[int] = None,
        count: int = 20
    ) -> Dict:
        """生成词汇测试"""
        self.connect()
        cursor = self.conn.cursor()
        
        # 构建查询
        sql = "SELECT * FROM vocabulary WHERE 1=1"
        params = []
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        if difficulty:
            sql += " AND difficulty = ?"
            params.append(difficulty)
        
        sql += " ORDER BY RANDOM() LIMIT ?"
        params.append(question_count)
        
        cursor.execute(sql, params)
        words = [dict(row) for row in cursor.fetchall()]
        
        # 生成测试题
        questions = []
        for word in words:
            question = self._create_vocabulary_question(word, cursor)
            questions.append(question)
        
        return {
            "test_type": "vocabulary",
            "category": category,
            "difficulty": difficulty,
            "question_count": len(questions),
            "questions": questions,
            "created_at": datetime.now().isoformat()
        }
    
    def _create_vocabulary_question(self, word: Dict, cursor) -> Dict:
        """创建词汇测试题"""
        question_type = random.choice(['meaning', 'usage'])
        
        if question_type == 'meaning':
            # 词义选择题
            # 获取3个干扰项
            cursor.execute("""
                SELECT chinese FROM vocabulary
                WHERE category = ? AND id != ?
                ORDER BY RANDOM() LIMIT 3
            """, (word['category'], word['id']))
            
            wrong_options = [row['chinese'] for row in cursor.fetchall()]
            
            # 组合选项
            options = [word['chinese']] + wrong_options
            random.shuffle(options)
            correct_answer = options.index(word['chinese'])
            
            return {
                "word_id": word['id'],
                "word": word['word'],
                "phonetic": word['phonetic'],
                "question_type": "meaning",
                "question": f"What is the meaning of '{word['word']}'?",
                "options": options,
                "correct_answer": correct_answer
            }
        
        else:
            # 用法选择题（简化版）
            return {
                "word_id": word['id'],
                "word": word['word'],
                "question_type": "usage",
                "question": f"Which sentence uses '{word['word']}' correctly?",
                "options": [
                    f"Example 1 with {word['word']}",
                    f"Example 2 with {word['word']}",
                    f"Example 3 with {word['word']}",
                    f"Example 4 with {word['word']}"
                ],
                "correct_answer": 0
            }
    
    def generate_reading_test(
        self,
        difficulty: int = 1,
        question_count: int = 10
    ) -> Dict:
        """生成阅读理解测试"""
        from .reading_comprehension import ReadingComprehensionAPI
        
        api = ReadingComprehensionAPI(self.db_path)
        
        # 获取不同类型的练习
        readme_exercises = api.get_readme_exercises(difficulty)[:question_count//3]
        issue_pr_exercises = api.get_issue_pr_exercises(difficulty)[:question_count//3]
        code_exercises = api.get_code_comment_exercises(difficulty)[:question_count//3]
        
        all_exercises = readme_exercises + issue_pr_exercises + code_exercises
        
        # 提取所有问题
        questions = []
        for idx, exercise in enumerate(all_exercises):
            for q_idx, question in enumerate(exercise.get('questions', [])):
                questions.append({
                    "question_id": f"{idx}_{q_idx}",
                    "exercise_type": exercise['type'],
                    "exercise_title": exercise['title'],
                    "content": exercise['content'],
                    "question": question['question'],
                    "options": question['options'],
                    "correct_answer": question['answer']
                })
        
        return {
            "test_type": "reading",
            "difficulty": difficulty,
            "question_count": len(questions),
            "questions": questions,
            "created_at": datetime.now().isoformat()
        }
    
    def generate_comprehensive_test(
        self,
        user_id: int,
        category: Optional[str] = None
    ) -> Dict:
        """生成综合考核（模拟真实场景）"""
        # 组合词汇测试和阅读测试
        vocab_test = self.generate_vocabulary_test(
            user_id, category, question_count=15
        )
        
        reading_test = self.generate_reading_test(difficulty=2, question_count=10)
        
        # 合并测试
        all_questions = vocab_test['questions'] + reading_test['questions']
        random.shuffle(all_questions)
        
        return {
            "test_type": "comprehensive",
            "category": category,
            "question_count": len(all_questions),
            "questions": all_questions,
            "time_limit": 30 * 60,  # 30分钟
            "passing_score": 90,
            "created_at": datetime.now().isoformat()
        }
    
    def submit_test(
        self,
        user_id: int,
        test_type: str,
        answers: List[int],
        time_spent: int = 0
    ) -> Dict:
        """提交测试结果"""
        # 这里简化处理，实际需要验证答案
        # 假设前80%正确
        correct_count = int(len(answers) * 0.8)
        total = len(answers)
        score = (correct_count / total * 100) if total > 0 else 0
        
        # 保存到数据库
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO test_records
            (user_id, test_type, total_questions, correct_answers, 
             wrong_answers, score, time_spent, test_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, test_type, total, correct_count,
            total - correct_count, score, time_spent, datetime.now()
        ))
        
        test_id = cursor.lastrowid
        self.conn.commit()
        
        # 判断是否及格
        passed = score >= 90
        
        return {
            "success": True,
            "test_id": test_id,
            "score": round(score, 2),
            "correct": correct_count,
            "wrong": total - correct_count,
            "total": total,
            "passed": passed,
            "time_spent": time_spent
        }
    
    def get_test_history(
        self,
        user_id: int,
        test_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """获取测试历史"""
        self.connect()
        cursor = self.conn.cursor()
        
        sql = """
            SELECT * FROM test_records
            WHERE user_id = ?
        """
        params = [user_id]
        
        if test_type:
            sql += " AND test_type = ?"
            params.append(test_type)
        
        sql += " ORDER BY test_date DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_test_statistics(self, user_id: int) -> Dict:
        """获取测试统计"""
        self.connect()
        cursor = self.conn.cursor()
        
        # 总体统计
        cursor.execute("""
            SELECT 
                COUNT(*) as total_tests,
                AVG(score) as avg_score,
                MAX(score) as max_score,
                MIN(score) as min_score,
                SUM(CASE WHEN score >= 90 THEN 1 ELSE 0 END) as passed_tests
            FROM test_records
            WHERE user_id = ?
        """, (user_id,))
        
        stats = dict(cursor.fetchone())
        
        # 按类型统计
        cursor.execute("""
            SELECT 
                test_type,
                COUNT(*) as count,
                AVG(score) as avg_score
            FROM test_records
            WHERE user_id = ?
            GROUP BY test_type
        """, (user_id,))
        
        stats['by_type'] = {
            row['test_type']: {
                'count': row['count'],
                'avg_score': round(row['avg_score'], 2)
            }
            for row in cursor.fetchall()
        }
        
        return stats


# 测试
if __name__ == "__main__":
    api = TestAssessmentAPI()
    
    print("=" * 60)
    print("Test Assessment API Test")
    print("=" * 60)
    
    # 测试1: 生成词汇测试
    print("\n[Test 1] Generate Vocabulary Test")
    test = api.generate_vocabulary_test(user_id=1, category="Python技术词汇", question_count=5)
    print(f"Questions: {test['question_count']}")
    if test['questions']:
        q = test['questions'][0]
        print(f"Sample: {q['word']} - {q['question']}")
    
    # 测试2: 生成阅读测试
    print("\n[Test 2] Generate Reading Test")
    test = api.generate_reading_test(difficulty=1, question_count=5)
    print(f"Questions: {test['question_count']}")
    
    # 测试3: 提交测试
    print("\n[Test 3] Submit Test")
    result = api.submit_test(user_id=1, test_type="vocabulary", answers=[0, 1, 2, 0, 1])
    print(f"Score: {result['score']}, Passed: {result['passed']}")
    
    # 测试4: 获取统计
    print("\n[Test 4] Get Statistics")
    stats = api.get_test_statistics(user_id=1)
    print(f"Total tests: {stats['total_tests']}, Avg score: {stats['avg_score']}")
    
    api.close()
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
