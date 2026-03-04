#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阅读理解模块API
提供GitHub场景阅读、翻译练习等功能
"""

import sqlite3
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

DB_PATH = Path(__file__).parent.parent / "data" / "github_english_learning.db"

class ReadingComprehensionAPI:
    """阅读理解API"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self.conn = None
        self.knowledge_base_path = Path(__file__).parent.parent / "knowledge_base"
    
    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def get_readme_exercises(self, difficulty: int = 1) -> List[Dict]:
        """获取README练习"""
        exercises = []
        
        # 简单练习（难度1）
        if difficulty == 1:
            exercises = [
                {
                    "type": "readme",
                    "title": "Project Introduction",
                    "content": """# My Project

This is a simple Python project for data processing.

## Features
- Easy to use
- Fast processing
- Cross-platform support

## Installation
```bash
pip install myproject
```

## Quick Start
```python
from myproject import Processor
processor = Processor()
result = processor.run()
```""",
                    "questions": [
                        {
                            "question": "What is the main purpose of this project?",
                            "options": ["Data processing", "Web development", "Mobile apps", "Game development"],
                            "answer": 0
                        },
                        {
                            "question": "How do you install this project?",
                            "options": ["npm install", "pip install myproject", "apt-get install", "download zip"],
                            "answer": 1
                        }
                    ]
                }
            ]
        
        # 中等练习（难度2）
        elif difficulty == 2:
            exercises = [
                {
                    "type": "readme",
                    "title": "Installation Guide",
                    "content": """## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/user/repo.git
cd repo
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
export DATABASE_URL=postgresql://localhost/mydb
export SECRET_KEY=your-secret-key
```

5. Run the application:
```bash
python app.py
```""",
                    "questions": [
                        {
                            "question": "What Python version is required?",
                            "options": ["3.6", "3.8 or higher", "2.7", "Any version"],
                            "answer": 1
                        },
                        {
                            "question": "Which command activates the virtual environment on Windows?",
                            "options": ["source venv/bin/activate", "venv\\\\Scripts\\\\activate", "activate venv", "python venv"],
                            "answer": 1
                        }
                    ]
                }
            ]
        
        return exercises
    
    def get_issue_pr_exercises(self, difficulty: int = 1) -> List[Dict]:
        """获取Issue/PR练习"""
        exercises = [
            {
                "type": "issue",
                "title": "Bug Report",
                "content": """## Bug Description

**Title:** ValueError when processing empty DataFrame

**Steps to Reproduce:**
1. Create an empty DataFrame: `df = pd.DataFrame()`
2. Run processor: `processor.process(df)`
3. See error: `ValueError: Cannot process empty DataFrame`

**Expected Behavior:**
Should handle empty DataFrames gracefully.

**Environment:**
- Python: 3.11
- pandas: 2.0.0
- OS: Ubuntu 20.04""",
                "questions": [
                    {
                        "question": "What type of issue is this?",
                        "options": ["Feature request", "Bug report", "Documentation", "Question"],
                        "answer": 1
                    },
                    {
                        "question": "What is the expected behavior?",
                        "options": ["Raise an error", "Handle empty DataFrames gracefully", "Ignore the input", "Return None"],
                        "answer": 1
                    }
                ]
            },
            {
                "type": "pr",
                "title": "Pull Request Review",
                "content": """## Pull Request Description

**Changes:**
- Added batch processing support
- Improved error handling
- Updated documentation

**Code Review Comments:**

Reviewer @senior-dev:
"Great work! Please add type hints to the `process_batch()` function."

Author @developer1:
"Good catch! I've added type hints and updated the PR."

**Final Status:** Approved ✓""",
                "questions": [
                    {
                        "question": "What did the reviewer ask for?",
                        "options": ["More tests", "Type hints", "Documentation", "Bug fixes"],
                        "answer": 1
                    },
                    {
                        "question": "What was the final status?",
                        "options": ["Rejected", "Pending", "Approved", "Closed"],
                        "answer": 2
                    }
                ]
            }
        ]
        
        return exercises
    
    def get_code_comment_exercises(self, difficulty: int = 1) -> List[Dict]:
        """获取代码注释练习"""
        exercises = [
            {
                "type": "code_comment",
                "title": "Function Documentation",
                "content": """def calculate_average(numbers: list[float]) -> float:
    \"\"\"
    Calculate the arithmetic mean of a list of numbers.
    
    Args:
        numbers: A list of numeric values
        
    Returns:
        The arithmetic mean as a float
        
    Raises:
        ValueError: If the input list is empty
        
    Example:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
    \"\"\"
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)""",
                "questions": [
                    {
                        "question": "What does this function calculate?",
                        "options": ["Sum", "Average", "Median", "Mode"],
                        "answer": 1
                    },
                    {
                        "question": "What exception does it raise for empty lists?",
                        "options": ["TypeError", "IndexError", "ValueError", "ZeroDivisionError"],
                        "answer": 2
                    }
                ]
            }
        ]
        
        return exercises
    
    def submit_reading_result(
        self,
        user_id: int,
        exercise_type: str,
        exercise_id: str,
        answers: List[int]
    ) -> Dict:
        """提交阅读理解结果"""
        self.connect()
        cursor = self.conn.cursor()
        
        # 计算正确率（这里简化处理，实际需要根据具体练习判断）
        correct_count = sum(1 for ans in answers if ans >= 0)  # 简化
        total = len(answers)
        score = (correct_count / total * 100) if total > 0 else 0
        
        # 记录到数据库
        cursor.execute("""
            INSERT INTO test_records
            (user_id, test_type, total_questions, correct_answers, score, test_date, details)
            VALUES (?, 'reading', ?, ?, ?, ?, ?)
        """, (
            user_id, total, correct_count, score, datetime.now(),
            json.dumps({"exercise_type": exercise_type, "exercise_id": exercise_id})
        ))
        
        self.conn.commit()
        
        return {
            "success": True,
            "score": score,
            "correct": correct_count,
            "total": total
        }
    
    def get_translation_exercises(self, category: str = 'readme') -> List[Dict]:
        """获取翻译练习"""
        exercises = [
            {
                "type": "translation",
                "category": category,
                "english": "This function processes a batch of items efficiently.",
                "chinese": "此函数高效地处理一批项目。",
                "hint": "batch = 批次，efficiently = 高效地"
            },
            {
                "type": "translation",
                "category": category,
                "english": "Please ensure all dependencies are installed before running the application.",
                "chinese": "请确保在运行应用程序之前安装所有依赖项。",
                "hint": "dependencies = 依赖项，ensure = 确保"
            }
        ]
        
        return exercises
    
    def get_random_exercise(self, difficulty: int = 1) -> Dict:
        """获取随机练习"""
        exercise_types = ['readme', 'issue_pr', 'code_comment']
        exercise_type = random.choice(exercise_types)
        
        if exercise_type == 'readme':
            exercises = self.get_readme_exercises(difficulty)
        elif exercise_type == 'issue_pr':
            exercises = self.get_issue_pr_exercises(difficulty)
        else:
            exercises = self.get_code_comment_exercises(difficulty)
        
        return random.choice(exercises) if exercises else {}


# 测试
if __name__ == "__main__":
    api = ReadingComprehensionAPI()
    
    print("=" * 60)
    print("Reading Comprehension API Test")
    print("=" * 60)
    
    # 测试1: README练习
    print("\n[Test 1] README Exercises")
    exercises = api.get_readme_exercises(difficulty=1)
    print(f"Found {len(exercises)} exercises")
    
    # 测试2: Issue/PR练习
    print("\n[Test 2] Issue/PR Exercises")
    exercises = api.get_issue_pr_exercises(difficulty=1)
    print(f"Found {len(exercises)} exercises")
    
    # 测试3: 随机练习
    print("\n[Test 3] Random Exercise")
    exercise = api.get_random_exercise(difficulty=1)
    print(f"Type: {exercise.get('type')}, Title: {exercise.get('title')}")
    
    api.close()
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
