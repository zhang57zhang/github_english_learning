# 程序员GitHub英语学习系统 - 项目计划

## 📊 项目概览

### 项目目标
- **主要目标:** 帮助新员工快速掌握GitHub项目阅读能力
- **核心能力:** 技术文档理解、Issue讨论理解、代码注释理解
- **学习周期:** 2-4周（每天1-2小时）
- **考核标准:** 90分及格

### 目标用户
- **主要人群:** 新员工（应届生/转行人员）
- **英语基础:** 中级水平（能阅读基础技术文档）
- **技术背景:** Python、大模型、Agent、车载、底盘、动力学

## 🎯 系统架构设计

### 核心功能模块

```
程序员GitHub英语学习系统
│
├─ 1. 词汇学习系统（核心）
│   ├─ 词汇库（5000词）
│   │   ├─ Python技术词汇（800词）
│   │   ├─ 大模型/Agent词汇（1000词）
│   │   ├─ 车载/底盘/动力学词汇（1200词）
│   │   ├─ GitHub通用词汇（1000词）
│   │   └─ 计算机基础词汇（1000词）
│   ├─ 遗忘曲线复习系统
│   │   ├─ 艾宾浩斯记忆曲线（1/2/4/7/15天）
│   │   ├─ 智能复习提醒
│   │   └─ 弱项词汇强化
│   └─ 学习进度跟踪
│       ├─ 每日学习量（350词）
│       ├─ 复习完成率
│       └─ 掌握程度评估
│
├─ 2. GitHub场景知识库
│   ├─ README文档英语
│   │   ├─ 项目介绍模板
│   │   ├─ 安装说明模板
│   │   ├─ 使用指南模板
│   │   └─ 贡献指南模板
│   ├─ Issue/PR讨论英语
│   │   ├─ Bug报告模板
│   │   ├─ 功能请求模板
│   │   ├─ 代码审查对话
│   │   └─ 技术讨论案例
│   ├─ 代码注释英语
│   │   ├─ 函数说明注释
│   │   ├─ 算法解释注释
│   │   ├─ 业务逻辑注释
│   │   └─ 配置文件注释
│   └─ Wiki/文档英语
│       ├─ 架构设计文档
│       ├─ API文档
│       └─ 最佳实践文档
│
├─ 3. 实战练习系统
│   ├─ 阅读理解
│   │   ├─ 真实GitHub项目片段
│   │   ├─ 技术文档理解测试
│   │   └─ Issue讨论分析
│   ├─ 翻译练习
│   │   ├─ 英译中（技术文档）
│   │   └─ 中译英（简单表达）
│   └─ 场景模拟
│       ├─ 模拟阅读项目README
│       ├─ 模拟理解Issue讨论
│       └─ 模拟阅读代码注释
│
└─ 4. 测试评估系统
    ├─ 词汇测试（选择题）
    ├─ 阅读理解（选择题+简答题）
    ├─ 翻译测试（英译中）
    └─ 综合考核（模拟真实场景）
```

### 技术架构（复用vehicle_learning_system）

```
前端: Streamlit（快速开发，友好界面）
后端: FastAPI（API服务）
向量存储: 多层降级架构
  - Layer 1: Qdrant + SentenceTransformers（最佳）
  - Layer 2: Qdrant + TF-IDF + SVD（备选）
  - Layer 3: 本地TF-IDF + SVD（零依赖）
知识库: 结构化Markdown + JSON
测试系统: 题库管理 + 自动评分
遗忘曲线: 数据库记录 + 智能提醒
```

## 📅 开发计划（2周）

### Phase 1: 需求细化与架构设计（1天）✅
**时间:** 2026-03-04

**任务:**
- ✅ 确认学习目标（阅读理解为主）
- ✅ 确认难度分级（中级）
- ✅ 确认学习周期（2-4周）
- ✅ 确认考核标准（90分及格）
- ✅ 确认技术领域（Python/大模型/Agent/车载/底盘/动力学）
- ✅ 确认词汇量（5000词，每次350词，遗忘曲线）

**输出:**
- ✅ PROJECT_PLAN.md（本文档）
- ✅ 系统架构设计
- ✅ 开发时间表

---

### Phase 2: 词汇库构建（3天）
**时间:** 2026-03-05 - 2026-03-07

#### 2.1 词汇分类与收集（1天）
**任务:**
- [ ] Python技术词汇（800词）
  - 基础语法词汇
  - 标准库词汇
  - 第三方库词汇
  - Web框架词汇（FastAPI/Flask/Django）
  
- [ ] 大模型/Agent词汇（1000词）
  - LLM基础词汇（token/embedding/attention等）
  - RAG系统词汇（retrieval/generation/vector等）
  - Agent词汇（planning/tool/action等）
  - 模型训练词汇（fine-tuning/hyperparameter等）
  
- [ ] 车载/底盘/动力学词汇（1200词）
  - 车辆动力学词汇（suspension/damping/roll等）
  - 底盘控制词汇（braking/steering/stability等）
  - 车载系统词汇（CAN/bus/ECU/sensor等）
  - 测试验证词汇（validation/verification/benchmark等）
  
- [ ] GitHub通用词汇（1000词）
  - 版本控制词汇（commit/merge/branch等）
  - 协作词汇（pull request/review/collaborator等）
  - 项目管理词汇（issue/milestone/label等）
  - 文档词汇（README/wiki/contributing等）
  
- [ ] 计算机基础词汇（1000词）
  - 数据结构词汇
  - 算法词汇
  - 系统设计词汇
  - 网络通信词汇

**输出:**
- `vocabulary/python_tech.json`（800词）
- `vocabulary/llm_agent.json`（1000词）
- `vocabulary/vehicle_dynamics.json`（1200词）
- `vocabulary/github_general.json`（1000词）
- `vocabulary/cs_basics.json`（1000词）

#### 2.2 词汇详细化（2天）
**任务:**
- [ ] 每个词汇添加详细信息
  - 单词
  - 音标
  - 词性
  - 中文释义
  - 英文释义
  - 例句（GitHub场景）
  - 同义词
  - 反义词
  - 关联词汇
  - 难度等级
  
- [ ] 词汇分组（350词/组，共15组）
  - Group 1-3: Python基础词汇
  - Group 4-6: 大模型/Agent词汇
  - Group 7-9: 车载/底盘/动力学词汇
  - Group 10-12: GitHub通用词汇
  - Group 13-15: 计算机基础词汇

**输出:**
- `vocabulary/detailed/python_tech_detailed.json`
- `vocabulary/detailed/llm_agent_detailed.json`
- `vocabulary/detailed/vehicle_dynamics_detailed.json`
- `vocabulary/detailed/github_general_detailed.json`
- `vocabulary/detailed/cs_basics_detailed.json`

---

### Phase 3: GitHub场景知识库构建（3天）
**时间:** 2026-03-08 - 2026-03-10

#### 3.1 README文档模板（1天）
**任务:**
- [ ] 项目介绍模板
  - 项目名称和简介
  - 特性列表
  - 快速开始
  - 徽章（badges）
  
- [ ] 安装说明模板
  - 环境要求
  - 安装步骤
  - 依赖说明
  - 配置指南
  
- [ ] 使用指南模板
  - 基础用法
  - 高级功能
  - API参考
  - 示例代码
  
- [ ] 贡献指南模板
  - 开发环境设置
  - 代码规范
  - 提交规范
  - PR流程

**输出:**
- `knowledge_base/readme_templates.md`

#### 3.2 Issue/PR讨论案例（1天）
**任务:**
- [ ] Bug报告案例
  - 问题描述
  - 复现步骤
  - 期望行为
  - 环境信息
  
- [ ] 功能请求案例
  - 功能描述
  - 使用场景
  - 实现建议
  
- [ ] 代码审查对话
  - 审查意见
  - 改进建议
  - 讨论回复
  
- [ ] 技术讨论案例
  - 架构设计讨论
  - 性能优化讨论
  - 最佳实践讨论

**输出:**
- `knowledge_base/issue_pr_cases.md`

#### 3.3 代码注释范例（1天）
**任务:**
- [ ] 函数说明注释
  - docstring格式
  - 参数说明
  - 返回值说明
  - 异常说明
  
- [ ] 算法解释注释
  - 算法思路
  - 复杂度分析
  - 边界条件
  
- [ ] 业务逻辑注释
  - 业务规则
  - 特殊处理
  - 注意事项
  
- [ ] 配置文件注释
  - 配置项说明
  - 默认值
  - 可选值

**输出:**
- `knowledge_base/code_comments_examples.md`

---

### Phase 4: 遗忘曲线系统开发（2天）
**时间:** 2026-03-11 - 2026-03-12

#### 4.1 数据库设计（0.5天）
**任务:**
- [ ] 设计词汇学习记录表
  - user_id
  - word_id
  - first_learn_time
  - next_review_time
  - review_count
  - mastery_level
  - last_review_result
  
- [ ] 设计复习计划表
  - user_id
  - review_date
  - word_ids（JSON数组）
  - completed
  
- [ ] 设计学习进度表
  - user_id
  - total_words
  - learned_words
  - mastered_words
  - daily_goal
  - current_streak

**输出:**
- `database/schema.sql`
- `database/init_db.py`

#### 4.2 遗忘曲线算法（0.5天）
**任务:**
- [ ] 实现艾宾浩斯记忆曲线
  - 第1次复习: 1天后
  - 第2次复习: 2天后
  - 第3次复习: 4天后
  - 第4次复习: 7天后
  - 第5次复习: 15天后
  
- [ ] 智能调整算法
  - 根据复习结果调整间隔
  - 错误词汇缩短间隔
  - 正确词汇延长间隔
  
- [ ] 弱项词汇识别
  - 识别高频错误词汇
  - 自动加入强化复习

**输出:**
- `algorithms/forgetting_curve.py`

#### 4.3 复习提醒系统（1天）
**任务:**
- [ ] 每日复习计划生成
  - 根据遗忘曲线生成当日复习词汇
  - 结合新词汇学习
  - 总量控制在350词
  
- [ ] 复习提醒推送
  - 邮件提醒（可选）
  - 系统内提醒
  - 进度条显示
  
- [ ] 学习报告生成
  - 每日学习报告
  - 每周学习报告
  - 掌握程度统计

**输出:**
- `services/review_scheduler.py`
- `services/notification.py`
- `services/learning_report.py`

---

### Phase 5: 核心功能开发（3天）
**时间:** 2026-03-13 - 2026-03-15

#### 5.1 词汇学习模块（1天）
**任务:**
- [ ] 词汇展示页面
  - 单词卡片
  - 音标发音
  - 释义展示
  - 例句展示
  - 进度显示
  
- [ ] 学习模式
  - 浏览模式（顺序浏览）
  - 测试模式（选择题）
  - 拼写模式（填空题）
  
- [ ] 复习模式
  - 今日复习词汇
  - 强化复习词汇
  - 自定义复习

**输出:**
- `backend/vocabulary_learning.py`
- `frontend/pages/vocabulary.py`

#### 5.2 阅读理解模块（1天）
**任务:**
- [ ] GitHub场景阅读
  - README文档阅读
  - Issue讨论阅读
  - 代码注释阅读
  
- [ ] 理解测试
  - 关键信息提取
  - 主题理解
  - 细节理解
  
- [ ] 翻译练习
  - 英译中练习
  - 对照参考译文
  - 评分反馈

**输出:**
- `backend/reading_comprehension.py`
- `frontend/pages/reading.py`

#### 5.3 测试评估模块（1天）
**任务:**
- [ ] 词汇测试
  - 选择题（词义选择）
  - 填空题（拼写测试）
  - 配对题（中英配对）
  
- [ ] 阅读理解测试
  - 选择题
  - 简答题
  - 判断题
  
- [ ] 综合测试
  - 模拟GitHub场景
  - 真实项目片段
  - 90分及格判定

**输出:**
- `backend/test_assessment.py`
- `frontend/pages/test.py`

---

### Phase 6: 前端开发（3天）
**时间:** 2026-03-16 - 2026-03-18

#### 6.1 用户界面设计（1天）
**任务:**
- [ ] 首页设计
  - 学习进度概览
  - 今日任务
  - 复习提醒
  - 学习统计
  
- [ ] 学习中心
  - 词汇学习
  - 阅读练习
  - 测试评估
  
- [ ] 个人中心
  - 学习记录
  - 成绩统计
  - 设置

**输出:**
- `frontend/app.py`
- `frontend/pages/home.py`

#### 6.2 交互功能实现（1天）
**任务:**
- [ ] 学习进度跟踪
  - 实时进度更新
  - 进度条显示
  - 完成提醒
  
- [ ] 测试反馈系统
  - 即时评分
  - 错误解析
  - 改进建议
  
- [ ] 学习报告可视化
  - 学习曲线图
  - 词汇掌握度图
  - 复习效果统计

**输出:**
- `frontend/components/progress_tracker.py`
- `frontend/components/test_feedback.py`
- `frontend/components/learning_charts.py`

#### 6.3 用户体验优化（1天）
**任务:**
- [ ] 响应式设计
  - 适配不同屏幕
  - 移动端优化
  
- [ ] 快捷键支持
  - 键盘导航
  - 快速答题
  
- [ ] 离线支持
  - 本地缓存
  - 离线学习

**输出:**
- `frontend/static/style.css`
- `frontend/utils/keyboard_shortcuts.py`

---

### Phase 7: 测试与优化（2天）
**时间:** 2026-03-19 - 2026-03-20

#### 7.1 功能测试（1天）
**任务:**
- [ ] 词汇学习功能测试
- [ ] 遗忘曲线功能测试
- [ ] 阅读理解功能测试
- [ ] 测试评估功能测试
- [ ] 前端界面测试

**输出:**
- `tests/test_vocabulary.py`
- `tests/test_forgetting_curve.py`
- `tests/test_reading.py`
- `tests/test_assessment.py`
- `tests/test_frontend.py`

#### 7.2 性能优化（1天）
**任务:**
- [ ] 数据库查询优化
- [ ] 向量检索优化
- [ ] 前端加载优化
- [ ] 缓存策略优化

**输出:**
- `tests/performance_test.py`
- `optimization_report.md`

---

## 📊 成功标准

### 功能完整性
- ✅ 5000词汇完整收集
- ✅ 15个词汇组（350词/组）
- ✅ 遗忘曲线复习系统
- ✅ GitHub场景知识库
- ✅ 阅读理解练习
- ✅ 测试评估系统
- ✅ 学习进度跟踪

### 质量标准
- ✅ 词汇准确率 >99%
- ✅ 例句质量高（真实GitHub场景）
- ✅ 测试覆盖率 >90%
- ✅ 用户界面友好
- ✅ 响应时间 <500ms

### 学习效果
- ✅ 2-4周完成学习
- ✅ 90分及格率 >80%
- ✅ 词汇掌握率 >85%
- ✅ GitHub阅读能力显著提升

## 🚀 部署计划

### 开发环境
```
Python 3.11+
Streamlit
FastAPI
SQLite（词汇学习记录）
Qdrant（可选，向量检索）
```

### 生产环境
```
Docker容器化
Nginx反向代理
PostgreSQL（生产数据库）
Redis（缓存）
```

### 启动方式
```bash
# 开发环境
cd E:\workspace\github_english_learning
streamlit run frontend/app.py

# 生产环境
docker-compose up -d
```

## 📝 文档计划

- [ ] README.md（项目介绍）
- [ ] USER_GUIDE.md（用户指南）
- [ ] DEVELOPER_GUIDE.md（开发者指南）
- [ ] VOCABULARY_GUIDE.md（词汇学习指南）
- [ ] API_DOCUMENTATION.md（API文档）

## 🎯 下一步行动

**立即开始:**
1. 创建项目目录结构
2. 开始词汇收集（Python技术词汇）
3. 设计数据库schema
4. 搭建基础前端框架

**准备就绪，随时开始开发！** 🚀
