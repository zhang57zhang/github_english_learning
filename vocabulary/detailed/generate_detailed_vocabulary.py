#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词汇详细化脚本
自动为词汇添加音标、例句、同义词等信息
"""

import json
import os
from pathlib import Path

# 词汇基础数据
BASE_VOCABULARY_DIR = Path("E:/workspace/github_english_learning/vocabulary")
DETAILED_DIR = Path("E:/workspace/github_english_learning/vocabulary/detailed")

# 音标映射（常见词汇）
PHONETIC_MAP = {
    # Python基础
    "variable": "/ˈver.i.ə.bəl/",
    "function": "/ˈfʌŋk.ʃən/",
    "class": "/klæs/",
    "object": "/ˈɒb.dʒekt/",
    "method": "/ˈmeθ.əd/",
    "attribute": "/əˈtrɪb.juːt/",
    "parameter": "/pəˈræm.ɪ.tər/",
    "argument": "/ˈɑːr.ɡjʊ.mənt/",
    "return": "/rɪˈtɜːrn/",
    "import": "/ɪmˈpɔːrt/",
    "module": "/ˈmɒd.juːl/",
    "package": "/ˈpæk.ɪdʒ/",
    "exception": "/ɪkˈsep.ʃən/",
    "error": "/ˈer.ər/",
    "try": "/traɪ/",
    "catch": "/kætʃ/",
    "raise": "/reɪz/",
    "finally": "/ˈfaɪ.nəl.i/",
    "with": "/wɪð/",
    "as": "/æz/",
    "lambda": "/ˈlæm.də/",
    
    # 数据结构
    "array": "/əˈreɪ/",
    "list": "/lɪst/",
    "dictionary": "/ˈdɪk.ʃən.er.i/",
    "tuple": "/ˈtuː.pəl/",
    "set": "/set/",
    "string": "/strɪŋ/",
    "integer": "/ˈɪn.tɪ.dʒər/",
    "float": "/fləʊt/",
    "boolean": "/ˈbuː.li.ən/",
    
    # 算法
    "algorithm": "/ˈæl.ɡə.rɪ.ðəm/",
    "sort": "/sɔːrt/",
    "search": "/sɜːrtʃ/",
    "recursion": "/rɪˈkɜː.ʃən/",
    "iteration": "/ˌɪt.əˈreɪ.ʃən/",
    
    # 网络通信
    "network": "/ˈnet.wɜːrk/",
    "protocol": "/ˈproʊ.tə.kɒl/",
    "server": "/ˈsɜːr.vər/",
    "client": "/ˈklaɪ.ənt/",
    "request": "/rɪˈkwest/",
    "response": "/rɪˈspɒns/",
    
    # 默认
    "default": "/dɪˈfɔːlt/"
}

# GitHub场景例句模板
GITHUB_EXAMPLE_TEMPLATES = {
    "function": "Functions are the building blocks of Python programs. Most projects organize code into functions for reusability.",
    "class": "Classes are essential in OOP. Python projects often define classes to model real-world entities.",
    "module": "Projects are organized into modules. Each .py file is a module. Understanding module structure helps navigate codebases.",
    "package": "Packages organize related modules. Large projects use packages to structure code hierarchically.",
    "import": "Import statements are at the top of most Python files. They show what dependencies a project uses.",
    "exception": "Exception handling is crucial for robust code. GitHub projects use try-except blocks to handle errors gracefully.",
    "default": "Common in Python projects for various purposes."
}

# 同义词映射
SYNONYM_MAP = {
    "function": ["method", "procedure", "routine"],
    "class": ["type", "object blueprint"],
    "variable": ["identifier", "name", "storage"],
    "error": ["bug", "fault", "mistake"],
    "module": ["file", "unit"],
    "package": ["library", "collection"],
    "default": []
}

# 关联词汇映射
RELATED_MAP = {
    "function": ["def", "return", "parameter", "argument", "lambda"],
    "class": ["object", "instance", "inheritance", "method", "attribute"],
    "variable": ["assignment", "value", "type", "scope"],
    "module": ["package", "import", "__init__.py", "namespace"],
    "default": []
}

def get_phonetic(word):
    """获取音标"""
    return PHONETIC_MAP.get(word, f"/{word}/")

def get_github_context(word, category):
    """获取GitHub场景说明"""
    if word in GITHUB_EXAMPLE_TEMPLATES:
        return GITHUB_EXAMPLE_TEMPLATES[word]
    
    # 根据类别生成
    category_contexts = {
        "Python技术词汇": f"Common in Python projects, especially in {word}-related functionality.",
        "大模型/Agent词汇": f"Frequently used in LLM and Agent development contexts.",
        "车载/底盘/动力学词汇": f"Common in automotive software and vehicle control systems.",
        "GitHub通用词汇": f"Essential terminology for GitHub collaboration and version control.",
        "计算机基础词汇": f"Fundamental concept in computer science and software development."
    }
    
    return category_contexts.get(category, "Common in software development projects.")

def get_synonyms(word):
    """获取同义词"""
    return SYNONYM_MAP.get(word, [])

def get_related_words(word):
    """获取关联词汇"""
    return RELATED_MAP.get(word, [])

def determine_part_of_speech(word):
    """判断词性"""
    keywords = {
        "function": "noun",
        "class": "noun",
        "def": "keyword",
        "return": "keyword",
        "import": "keyword/verb",
        "try": "keyword",
        "except": "keyword",
        "lambda": "keyword",
        "with": "keyword",
        "as": "keyword"
    }
    
    return keywords.get(word, "noun/adjective")

def generate_detailed_word(word_data, category):
    """生成详细词汇信息"""
    word = word_data["word"]
    chinese = word_data["chinese"]
    difficulty = word_data["difficulty"]
    
    detailed = {
        "word": word,
        "phonetic": get_phonetic(word),
        "part_of_speech": determine_part_of_speech(word),
        "chinese": chinese,
        "english": f"A concept or term in {category}",
        "example": f"Usage example for {word} (to be enhanced)",
        "github_context": get_github_context(word, category),
        "synonyms": get_synonyms(word),
        "antonyms": [],
        "related": get_related_words(word),
        "difficulty": difficulty,
        "frequency": "high" if difficulty == 1 else "medium" if difficulty == 2 else "low"
    }
    
    return detailed

def process_vocabulary_file(input_file, output_dir, words_per_group=350):
    """处理词汇文件并生成详细版本"""
    print(f"Processing {input_file.name}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    category = data["category"]
    total_words = data["total_words"]
    
    # 收集所有词汇
    all_words = []
    for subcategory_name, subcategory_data in data["subcategories"].items():
        for word_data in subcategory_data["words"]:
            all_words.append(word_data)
    
    # 分组
    groups = []
    for i in range(0, len(all_words), words_per_group):
        group_words = all_words[i:i + words_per_group]
        group_number = i // words_per_group + 1
        
        detailed_words = []
        for word_data in group_words:
            detailed_word = generate_detailed_word(word_data, category)
            detailed_words.append(detailed_word)
        
        group = {
            "group_id": group_number,
            "group_name": f"{category} - 第{group_number}组",
            "word_count": len(detailed_words),
            "words": detailed_words
        }
        groups.append(group)
    
    # 保存详细版本
    output_data = {
        "category": f"{category} - 详细版",
        "total_words": total_words,
        "description": f"{data['description']}，包含音标、例句、同义词等详细信息",
        "groups": groups
    }
    
    output_file = output_dir / f"{input_file.stem}_detailed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Generated {output_file.name} with {len(groups)} groups")
    return len(groups)

def main():
    """主函数"""
    print("=" * 60)
    print("Vocabulary Detail Generation Script")
    print("=" * 60)
    
    # 确保输出目录存在
    DETAILED_DIR.mkdir(parents=True, exist_ok=True)
    
    # 处理所有词汇文件
    vocabulary_files = [
        "python_tech.json",
        "llm_agent.json",
        "vehicle_dynamics.json",
        "github_general.json",
        "cs_basics.json"
    ]
    
    total_groups = 0
    for vocab_file in vocabulary_files:
        input_file = BASE_VOCABULARY_DIR / vocab_file
        if input_file.exists():
            groups = process_vocabulary_file(input_file, DETAILED_DIR)
            total_groups += groups
        else:
            print(f"[WARNING] File not found: {vocab_file}")
    
    print("=" * 60)
    print(f"[DONE] Total {total_groups} vocabulary groups generated")
    print("=" * 60)

if __name__ == "__main__":
    main()
