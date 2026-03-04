# GitHub英语学习系统

**面向程序员的GitHub项目阅读能力提升系统**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 项目简介

GitHub英语学习系统是一个专为程序员设计的英语学习工具，帮助新员工在2-4周内快速掌握GitHub项目的阅读能力。

**核心能力:**
- 📚 5000个技术词汇（5大类）
- 🧠 艾宾浩斯遗忘曲线复习
- 💼 真实GitHub场景练习
- 📊 智能学习进度跟踪
- 🎯 90分及格考核

---

## 🎯 学习目标

完成本系统学习后，你将能够：

1. **轻松阅读GitHub项目README**
   - 理解项目介绍和特性
   - 掌握安装和配置说明
   - 看懂使用指南和API文档

2. **理解Issue和PR讨论**
   - 看懂Bug报告和功能请求
   - 理解代码审查对话
   - 参与技术讨论

3. **阅读代码注释**
   - 理解函数说明
   - 掌握算法解释
   - 看懂业务逻辑

---

## ✨ 功能特性

### 📖 词汇学习

**5大词汇类别:**
- Python技术词汇（800词）
- 大模型/Agent词汇（1000词）
- 车载/底盘/动力学词汇（1200词）
- GitHub通用词汇（1000词）
- 计算机基础词汇（1000词）

**学习功能:**
- ✅ 新词汇学习
- ✅ 复习词汇
- ✅ 弱项强化
- ✅ 音标、例句、GitHub场景
- ✅ 同义词/反义词关联

### 📝 阅读练习

**3大练习场景:**
- 📄 README文档练习
- 💬 Issue/PR讨论练习
- 💻 代码注释练习

**练习功能:**
- ✅ 难度分级（1-3级）
- ✅ 交互式答题
- ✅ 即时评分反馈
- ✅ 详细解析

### 📊 测试评估

**3种测试类型:**
- 📝 词汇测试（选择题）
- 📖 阅读理解测试
- 🎯 综合考核

**评估功能:**
- ✅ 类别和难度选择
- ✅ 自动评分系统
- ✅ 90分及格判定
- ✅ 错题汇总

### 📈 学习进度

**进度跟踪:**
- ✅ 学习统计（已学/已掌握）
- ✅ 学习曲线（30天）
- ✅ 目标达成仪表盘
- ✅ 测试表现分析

### ❌ 错题本

**错题管理:**
- ✅ 自动记录错题
- ✅ 错题详情查看
- ✅ 重新学习功能
- ✅ 清空错题本

### 🧠 遗忘曲线

**艾宾浩斯算法:**
- ✅ 1天后复习
- ✅ 2天后复习
- ✅ 4天后复习
- ✅ 7天后复习
- ✅ 15天后复习

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Streamlit
- SQLite3

### 安装依赖

```bash
pip install streamlit plotly pandas
```

### 启动应用

**Windows:**
```bash
cd github_english_learning
start.bat
```

**Linux/Mac:**
```bash
cd github_english_learning
bash start.sh
```

**手动启动:**
```bash
streamlit run frontend/app_enhanced.py
```

### 访问应用

打开浏览器访问: http://localhost:8501

---

## 📚 使用指南

### 1️⃣ 学习词汇

1. 选择学习模式（新词汇/复习/弱项）
2. 查看词汇详情（音标、释义、例句、GitHub场景）
3. 点击"认识"或"不认识"
4. 系统自动记录学习进度

### 2️⃣ 阅读练习

1. 选择练习类型（README/Issue/代码注释）
2. 选择难度等级（1-3级）
3. 阅读原文
4. 回答问题
5. 查看评分和解析

### 3️⃣ 测试评估

1. 选择测试类型（词汇/阅读/综合）
2. 选择类别和难度
3. 生成测试
4. 答题
5. 查看成绩（90分及格）

### 4️⃣ 查看进度

1. 查看学习统计
2. 查看学习曲线
3. 查看目标达成
4. 查看测试表现

---

## 📊 项目结构

```
github_english_learning/
├── algorithms/              # 算法模块
│   └── forgetting_curve.py  # 遗忘曲线算法
├── backend/                 # 后端模块
│   ├── vocabulary_learning.py
│   ├── reading_comprehension.py
│   └── test_assessment.py
├── database/                # 数据库
│   ├── schema.sql
│   └── init_db.py
├── data/                    # 数据文件
│   └── github_english_learning.db
├── frontend/                # 前端应用
│   ├── app.py              # 基础版
│   └── app_enhanced.py     # 增强版 ⭐
├── knowledge_base/          # 知识库
│   ├── readme_templates.md
│   ├── issue_pr_cases.md
│   └── code_comments_examples.md
├── services/                # 服务模块
│   └── review_scheduler.py
├── tests/                   # 测试
│   ├── test_frontend.py
│   └── performance_test.py
├── vocabulary/              # 词汇库
│   ├── python_tech.json
│   ├── llm_agent.json
│   ├── vehicle_dynamics.json
│   ├── github_general.json
│   ├── cs_basics.json
│   └── detailed/           # 详细词汇
├── api.py                   # API入口
├── PROJECT_PLAN.md         # 项目计划
├── start.bat               # Windows启动脚本
├── start.sh                # Linux/Mac启动脚本
└── README.md               # 本文档
```

---

## 🎓 学习建议

### 学习周期（2-4周）

**第1周: 词汇积累**
- 每天350个新词汇
- 使用遗忘曲线复习
- 重点：Python技术词汇

**第2周: 场景练习**
- README文档练习
- Issue/PR讨论练习
- 代码注释练习

**第3周: 测试评估**
- 词汇测试
- 阅读理解测试
- 综合考核

**第4周: 巩固提升**
- 弱项强化
- 错题复习
- 真实项目实战

### 学习技巧

1. **每日坚持** - 每天1-2小时
2. **及时复习** - 按遗忘曲线复习
3. **场景应用** - 结合真实GitHub项目
4. **错题本** - 重点复习错题
5. **目标明确** - 90分及格为目标

---

## 📈 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| 词汇学习响应 | <500ms | <100ms ✅ |
| 阅读练习响应 | <500ms | <100ms ✅ |
| 测试生成 | <1000ms | <500ms ✅ |
| 统计查询 | <300ms | <50ms ✅ |
| 并发请求 | <800ms | <600ms ✅ |

---

## 🛠️ 技术栈

**前端:**
- Streamlit - Web界面
- Plotly - 数据可视化
- Pandas - 数据处理

**后端:**
- Python 3.11+
- SQLite - 数据库
- 自定义算法

**特色:**
- 艾宾浩斯遗忘曲线
- 多层降级架构
- 响应式设计

---

## 📝 更新日志

### v2.0 (2026-03-04)
- ✅ 增强版前端（7个页面）
- ✅ 交互式答题系统
- ✅ 数据可视化（Plotly）
- ✅ 错题本功能
- ✅ 性能优化

### v1.0 (2026-03-04)
- ✅ 基础词汇学习
- ✅ 阅读练习
- ✅ 测试评估
- ✅ 遗忘曲线算法

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 📧 联系方式

**项目作者:** CodeCraft  
**创建时间:** 2026-03-04  
**最后更新:** 2026-03-04

---

## 🎉 致谢

感谢以下开源项目:
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)

---

**Happy Learning! 📚✨**
