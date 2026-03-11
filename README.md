# GitHub English Learning System

**A GitHub project reading ability improvement system for programmers**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

GitHub English Learning System is an English learning tool designed specifically for programmers, helping new employees quickly master GitHub project reading skills within 2-4 weeks.

**Core Features:**
- 5,000 technical vocabulary words (5 categories)
- Ebbinghaus forgetting curve review
- Real GitHub scenario practice
- Intelligent learning progress tracking
- 90-point passing assessment

---

## Features

### Vocabulary Learning
- 5 major vocabulary categories
- New vocabulary learning
- Review vocabulary
- Weakness reinforcement
- Phonetics, examples, GitHub scenarios
- Synonym/antonym associations

### Reading Practice
- README document practice
- Issue/PR discussion practice
- Code comment practice
- Difficulty levels (1-3)
- Interactive quiz
- Instant scoring feedback

### Test Assessment
- Vocabulary test (multiple choice)
- Reading comprehension test
- Comprehensive assessment
- Category and difficulty selection
- Auto-scoring system
- 90-point passing threshold

### Learning Progress
- Learning statistics
- Learning curve (30 days)
- Goal achievement dashboard
- Test performance analysis

### Error Notebook
- Automatic error recording
- Error details viewing
- Re-learning function
- Clear error notebook

### Forgetting Curve
- Ebbinghaus algorithm
- 1-day review
- 2-day review
- 4-day review
- 7-day review
- 15-day review

---

## Quick Start

### Requirements
- Python 3.11+
- Streamlit
- SQLite3

### Installation

```bash
pip install -r requirements.txt
```

### Run Application

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
bash start.sh
```

**Manual:**
```bash
streamlit run frontend/app_enhanced.py
```

### Access
Open browser: http://localhost:8501

---

## Project Structure

```
github_english_learning/
├── algorithms/              # Algorithm modules
│   └── forgetting_curve.py  # Forgetting curve algorithm
├── backend/                 # Backend modules
│   ├── vocabulary_learning.py
│   ├── reading_comprehension.py
│   └── test_assessment.py
├── database/                # Database
│   ├── schema.sql
│   └── init_db.py
├── data/                    # Data files
├── frontend/                # Frontend application
│   ├── app.py              # Basic version
│   └── app_enhanced.py     # Enhanced version
├── knowledge_base/          # Knowledge base
├── services/                # Service modules
├── tests/                   # Tests
├── vocabulary/              # Vocabulary library
├── api.py                   # API entry point
├── requirements.txt         # Dependencies
├── start.bat               # Windows startup
├── start.sh                # Linux/Mac startup
└── README.md
```

---

## Vocabulary Categories

| Category | Count | Description |
|----------|-------|-------------|
| Python Tech | 800 | Python programming vocabulary |
| LLM/Agent | 1,000 | Large model and AI agent vocabulary |
| Vehicle Dynamics | 1,200 | Automotive and chassis vocabulary |
| GitHub General | 1,000 | Common GitHub terminology |
| CS Basics | 1,000 | Computer science fundamentals |

---

## Learning Path (2-4 Weeks)

**Week 1: Vocabulary Building**
- 350 new words per day
- Use forgetting curve review
- Focus: Python technical vocabulary

**Week 2: Scenario Practice**
- README document practice
- Issue/PR discussion practice
- Code comment practice

**Week 3: Test Assessment**
- Vocabulary test
- Reading comprehension test
- Comprehensive assessment

**Week 4: Consolidation**
- Weakness reinforcement
- Error review
- Real project practice

---

## Tech Stack

**Frontend:**
- Streamlit - Web interface
- Plotly - Data visualization
- Pandas - Data processing

**Backend:**
- Python 3.11+
- SQLite - Database
- Custom algorithms

**Features:**
- Ebbinghaus forgetting curve
- Multi-layer fallback architecture
- Responsive design

---

## Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Vocabulary learning response | <500ms | <100ms |
| Reading practice response | <500ms | <100ms |
| Test generation | <1000ms | <500ms |
| Statistics query | <300ms | <50ms |
| Concurrent requests | <800ms | <600ms |

---

## License

MIT License

---

**Happy Learning!**
