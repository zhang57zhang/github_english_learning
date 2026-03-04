#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建SQLite数据库和所有表
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "data" / "github_english_learning.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

def init_database():
    """初始化数据库"""
    print("=" * 60)
    print("GitHub英语学习系统 - 数据库初始化")
    print("=" * 60)
    
    # 确保data目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除旧数据库（如果存在）
    if DB_PATH.exists():
        print(f"[WARNING] 数据库已存在，将删除旧数据库: {DB_PATH}")
        DB_PATH.unlink()
    
    # 读取schema
    print(f"[INFO] 读取Schema文件: {SCHEMA_PATH}")
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # 创建数据库连接
    print(f"[INFO] 创建数据库: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 执行schema
    print("[INFO] 创建表和索引...")
    cursor.executescript(schema_sql)
    
    # 提交事务
    conn.commit()
    
    # 验证表是否创建成功
    print("\n[INFO] 验证数据库结构:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    print(f"  表数量: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' ORDER BY name")
    indexes = cursor.fetchall()
    print(f"\n  索引数量: {len(indexes)}")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
    views = cursor.fetchall()
    print(f"  视图数量: {len(views)}")
    for view in views:
        print(f"  - {view[0]}")
    
    # 关闭连接
    conn.close()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 数据库初始化完成!")
    print("=" * 60)
    print(f"数据库位置: {DB_PATH}")
    print(f"数据库大小: {DB_PATH.stat().st_size / 1024:.2f} KB")
    print("=" * 60)

def load_vocabulary():
    """加载词汇数据到数据库"""
    print("\n" + "=" * 60)
    print("加载词汇数据")
    print("=" * 60)
    
    import json
    
    # 词汇库目录
    vocab_dir = Path(__file__).parent.parent / "vocabulary" / "detailed"
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 词汇库文件列表
    vocab_files = [
        ("Python技术词汇", "python_tech_detailed.json"),
        ("大模型/Agent词汇", "llm_agent_detailed.json"),
        ("车载/底盘/动力学词汇", "vehicle_dynamics_detailed.json"),
        ("GitHub通用词汇", "github_general_detailed.json"),
        ("计算机基础词汇", "cs_basics_detailed.json")
    ]
    
    total_words = 0
    
    for category_name, filename in vocab_files:
        filepath = vocab_dir / filename
        if not filepath.exists():
            print(f"[WARNING] 文件不存在: {filepath}")
            continue
        
        print(f"\n[INFO] 加载: {category_name}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取所有词汇
        words = []
        for group in data.get("groups", []):
            for word_data in group.get("words", []):
                words.append((
                    word_data.get("word", ""),
                    word_data.get("phonetic", ""),
                    word_data.get("part_of_speech", ""),
                    word_data.get("chinese", ""),
                    word_data.get("english", ""),
                    word_data.get("example", ""),
                    word_data.get("github_context", ""),
                    json.dumps(word_data.get("synonyms", []), ensure_ascii=False),
                    json.dumps(word_data.get("antonyms", []), ensure_ascii=False),
                    json.dumps(word_data.get("related", []), ensure_ascii=False),
                    word_data.get("difficulty", 1),
                    word_data.get("frequency", "medium"),
                    category_name
                ))
        
        # 批量插入（使用INSERT OR IGNORE忽略重复词汇）
        cursor.executemany("""
            INSERT OR IGNORE INTO vocabulary 
            (word, phonetic, part_of_speech, chinese, english, example, 
             github_context, synonyms, antonyms, related_words, 
             difficulty, frequency, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, words)
        
        print(f"  加载词汇数: {len(words)}")
        total_words += len(words)
    
    # 提交事务
    conn.commit()
    
    # 验证
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"[SUCCESS] 词汇加载完成!")
    print(f"总词汇数: {count}")
    print("=" * 60)

def create_test_user():
    """创建测试用户"""
    print("\n" + "=" * 60)
    print("创建测试用户")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建测试用户
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, settings)
        VALUES (?, ?, ?, ?)
    """, (
        "test_user",
        "test@example.com",
        "hashed_password_123",
        json.dumps({"daily_goal": 350, "review_reminder": True}, ensure_ascii=False)
    ))
    
    user_id = cursor.lastrowid
    
    # 创建学习进度记录
    categories = ["Python技术词汇", "大模型/Agent词汇", "车载/底盘/动力学词汇", 
                  "GitHub通用词汇", "计算机基础词汇"]
    
    for category in categories:
        cursor.execute("""
            INSERT INTO learning_progress (user_id, category, total_words)
            VALUES (?, ?, ?)
        """, (user_id, category, 1000))  # 假设每个类别1000词
    
    conn.commit()
    conn.close()
    
    print(f"[SUCCESS] 测试用户创建成功! user_id = {user_id}")
    print("=" * 60)

def test_database():
    """测试数据库功能"""
    print("\n" + "=" * 60)
    print("测试数据库功能")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 测试1: 查询词汇数量
    print("\n[TEST 1] 查询词汇数量:")
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    print(f"  总词汇数: {cursor.fetchone()[0]}")
    
    # 测试2: 按类别统计
    print("\n[TEST 2] 按类别统计:")
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM vocabulary
        GROUP BY category
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}词")
    
    # 测试3: 按难度统计
    print("\n[TEST 3] 按难度统计:")
    cursor.execute("""
        SELECT difficulty, COUNT(*) as count
        FROM vocabulary
        GROUP BY difficulty
        ORDER BY difficulty
    """)
    for row in cursor.fetchall():
        difficulty_name = {1: "简单", 2: "中等", 3: "困难"}
        print(f"  {difficulty_name.get(row[0], '未知')} (Level {row[0]}): {row[1]}词")
    
    # 测试4: 查询示例词汇
    print("\n[TEST 4] Sample vocabulary:")
    cursor.execute("""
        SELECT word, phonetic, chinese, difficulty
        FROM vocabulary
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[2]} (Level {row[3]})")
    
    # 测试5: 测试用户数据
    print("\n[TEST 5] 测试用户:")
    cursor.execute("SELECT id, username, email FROM users")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Username: {row[1]}, Email: {row[2]}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 所有测试通过!")
    print("=" * 60)

def main():
    """主函数"""
    try:
        # 1. 初始化数据库
        init_database()
        
        # 2. 加载词汇数据
        load_vocabulary()
        
        # 3. 创建测试用户
        create_test_user()
        
        # 4. 测试数据库
        test_database()
        
        print("\n" + "=" * 60)
        print("[COMPLETE] 数据库初始化全部完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
