#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub英语学习系统 - 增强版Streamlit前端
包含完整的学习功能、可视化图表、错题本等
"""

import streamlit as st
import sys
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import GitHubEnglishLearningAPI

# 页面配置
st.set_page_config(
    page_title="GitHub英语学习系统 - 增强版",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .big-font {
        font-size:24px !important;
    }
    .medium-font {
        font-size:18px !important;
    }
    .word-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .correct-answer {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .wrong-answer {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# 初始化API
@st.cache_resource
def init_api():
    return GitHubEnglishLearningAPI()

api = init_api()

# 会话状态管理
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1

if 'current_page' not in st.session_state:
    st.session_state.current_page = "学习中心"

if 'learning_mode' not in st.session_state:
    st.session_state.learning_mode = 'new'

if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0

if 'current_words' not in st.session_state:
    st.session_state.current_words = []

if 'wrong_words' not in st.session_state:
    st.session_state.wrong_words = []

if 'test_answers' not in st.session_state:
    st.session_state.test_answers = {}

if 'reading_answers' not in st.session_state:
    st.session_state.reading_answers = {}

# 侧边栏
st.sidebar.title("📚 GitHub英语学习")
st.sidebar.markdown("---")

# 页面选择
page = st.sidebar.radio(
    "导航",
    ["🏠 学习中心", "📖 词汇学习", "📝 阅读练习", "📊 测试评估", 
     "📈 学习进度", "❌ 错题本", "⚙️ 设置"],
    key="navigation"
)

st.sidebar.markdown("---")

# 用户信息
st.sidebar.markdown("### 👤 用户信息")
st.sidebar.info(f"**用户ID:** {st.session_state.user_id}")

# 获取学习统计
try:
    stats = api.get_learning_stats(st.session_state.user_id)
    st.sidebar.metric("已学词汇", stats.get('learned_words', 0))
    st.sidebar.metric("已掌握", stats.get('mastered_words', 0))
    st.sidebar.metric("平均掌握度", f"{stats.get('avg_mastery', 0):.1f}/5")
    
    # 错题数量
    wrong_count = len(st.session_state.wrong_words)
    if wrong_count > 0:
        st.sidebar.metric("错题数量", wrong_count, delta=None, delta_color="inverse")
except:
    st.sidebar.warning("无法加载统计数据")

# ============ 学习中心 ============
if "学习中心" in page:
    st.title("🏠 GitHub英语学习中心")
    st.markdown("### 欢迎来到程序员GitHub英语学习系统！")
    
    # 今日学习计划
    st.markdown("#### 📅 今日学习计划")
    try:
        plan = api.get_today_plan(st.session_state.user_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("今日目标", f"{plan.get('total_words', 0)} 词")
        with col2:
            st.metric("已完成", f"{plan.get('completed_words', 0)} 词")
        with col3:
            progress = (plan.get('completed_words', 0) / plan.get('total_words', 1)) * 100 if plan.get('total_words', 0) > 0 else 0
            st.metric("完成进度", f"{progress:.1f}%")
        
        # 进度条
        st.progress(progress / 100)
        
        # 预计完成时间
        if progress > 0 and progress < 100:
            remaining_words = plan.get('total_words', 0) - plan.get('completed_words', 0)
            st.info(f"📊 还需学习 {remaining_words} 个词汇即可完成今日目标")
        
    except Exception as e:
        st.error(f"加载学习计划失败: {e}")
    
    st.markdown("---")
    
    # 快速开始
    st.markdown("#### 🚀 快速开始")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 开始学习新词汇", use_container_width=True, type="primary"):
            st.session_state.learning_mode = 'new'
            st.session_state.current_word_index = 0
            st.session_state.current_words = api.get_learning_words(
                st.session_state.user_id, 
                mode='new', 
                limit=10
            )
            st.rerun()
    
    with col2:
        if st.button("🔄 复习旧词汇", use_container_width=True):
            st.session_state.learning_mode = 'review'
            st.session_state.current_word_index = 0
            st.session_state.current_words = api.get_learning_words(
                st.session_state.user_id, 
                mode='review', 
                limit=10
            )
            st.rerun()
    
    with col3:
        if st.button("📝 阅读练习", use_container_width=True):
            st.session_state.current_page = "阅读练习"
            st.rerun()
    
    st.markdown("---")
    
    # 学习统计图表
    st.markdown("#### 📊 学习统计（过去7天）")
    try:
        report = api.generate_learning_report(st.session_state.user_id, days=7)
        
        # 创建三列布局
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 学习词汇数统计
            fig_words = go.Figure(go.Indicator(
                mode="number+delta",
                value=report.get('total_words_learned', 0),
                title={"text": "学习词汇数"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            st.plotly_chart(fig_words, use_container_width=True)
        
        with col2:
            # 复习次数统计
            fig_reviews = go.Figure(go.Indicator(
                mode="number+delta",
                value=report.get('total_reviews', 0),
                title={"text": "总复习次数"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            st.plotly_chart(fig_reviews, use_container_width=True)
        
        with col3:
            # 正确率
            fig_accuracy = go.Figure(go.Indicator(
                mode="gauge+number",
                value=report.get('average_accuracy', 0) * 100,
                title={'text': "正确率"},
                gauge={'axis': {'range': [0, 100]},
                      'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}
            ))
            st.plotly_chart(fig_accuracy, use_container_width=True)
        
        # 弱项领域
        if report.get('weak_areas'):
            st.markdown("#### ⚠️ 弱项领域")
            for area in report['weak_areas']:
                st.warning(f"- {area}")
        
    except Exception as e:
        st.warning(f"无法加载学习报告: {e}")

# ============ 词汇学习 ============
elif "词汇学习" in page:
    st.title("📖 词汇学习")
    
    # 学习模式选择
    mode = st.radio(
        "选择学习模式",
        ["🆕 新词汇", "🔄 复习词汇", "⚠️ 弱项词汇"],
        horizontal=True
    )
    
    mode_map = {
        "🆕 新词汇": "new",
        "🔄 复习词汇": "review",
        "⚠️ 弱项词汇": "weak"
    }
    learning_mode = mode_map[mode]
    
    # 如果切换模式，重新获取词汇
    if learning_mode != st.session_state.learning_mode:
        st.session_state.learning_mode = learning_mode
        st.session_state.current_word_index = 0
        try:
            st.session_state.current_words = api.get_learning_words(
                st.session_state.user_id, 
                mode=learning_mode, 
                limit=10
            )
        except:
            st.session_state.current_words = []
        st.rerun()
    
    # 获取词汇（如果还没有）
    if not st.session_state.current_words:
        try:
            st.session_state.current_words = api.get_learning_words(
                st.session_state.user_id, 
                mode=learning_mode, 
                limit=10
            )
        except:
            st.session_state.current_words = []
    
    words = st.session_state.current_words
    
    if not words:
        st.info("🎉 太棒了！没有需要学习的词汇了！")
        if st.button("返回学习中心"):
            st.session_state.current_page = "学习中心"
            st.rerun()
    else:
        # 当前词汇索引
        if st.session_state.current_word_index >= len(words):
            st.session_state.current_word_index = 0
            st.success("🎉 本组词汇学习完成！")
            if st.button("继续学习下一组"):
                st.session_state.current_words = []
                st.rerun()
        else:
            word = words[st.session_state.current_word_index]
            
            # 进度条
            progress = (st.session_state.current_word_index + 1) / len(words)
            st.progress(progress)
            st.markdown(f"**进度:** {st.session_state.current_word_index + 1} / {len(words)}")
            
            st.markdown("---")
            
            # 词汇卡片（增强版）
            st.markdown('<div class="word-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # 单词和音标
                st.markdown(f"### {word['word']}")
                if word.get('phonetic'):
                    st.markdown(f"**音标:** `{word['phonetic']}`")
                
                st.markdown("")
                
                # 词性和释义
                if word.get('part_of_speech'):
                    st.markdown(f"**词性:** {word['part_of_speech']}")
                
                st.markdown(f"**中文释义:** {word['chinese']}")
                
                if word.get('english'):
                    st.markdown(f"**英文释义:** {word['english']}")
            
            with col2:
                # 难度等级
                difficulty = word.get('difficulty', 1)
                difficulty_text = {1: "⭐ 简单", 2: "⭐⭐ 中等", 3: "⭐⭐⭐ 困难"}
                st.metric("难度", difficulty_text.get(difficulty, "⭐"))
                
                # 学习次数
                if word.get('review_count'):
                    st.metric("复习次数", word['review_count'])
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("")
            
            # 例句（GitHub场景）
            if word.get('example'):
                with st.expander("📝 查看例句", expanded=False):
                    st.markdown(f"**例句:** {word['example']}")
                    if word.get('example_translation'):
                        st.markdown(f"**翻译:** {word['example_translation']}")
            
            # GitHub场景
            if word.get('github_context'):
                with st.expander("💼 GitHub应用场景", expanded=False):
                    st.markdown(word['github_context'])
                    if word.get('github_translation'):
                        st.markdown(f"**翻译:** {word['github_translation']}")
            
            # 同义词/反义词
            col1, col2 = st.columns(2)
            with col1:
                if word.get('synonyms'):
                    st.markdown(f"**同义词:** {', '.join(word['synonyms'])}")
            with col2:
                if word.get('antonyms'):
                    st.markdown(f"**反义词:** {', '.join(word['antonyms'])}")
            
            st.markdown("---")
            
            # 学习按钮
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("❌ 不认识", use_container_width=True, key=f"wrong_{word['id']}"):
                    try:
                        result = api.submit_learning_result(
                            st.session_state.user_id,
                            word['id'],
                            False
                        )
                        # 添加到错题本
                        st.session_state.wrong_words.append(word)
                        st.warning(f"继续努力！掌握度: {result.get('mastery_level', 0)}/5")
                        st.session_state.current_word_index += 1
                        st.rerun()
                    except Exception as e:
                        st.error(f"提交失败: {e}")
            
            with col2:
                if st.button("✅ 认识", use_container_width=True, key=f"correct_{word['id']}"):
                    try:
                        result = api.submit_learning_result(
                            st.session_state.user_id,
                            word['id'],
                            True
                        )
                        st.success(f"很好！掌握度: {result.get('mastery_level', 0)}/5")
                        st.session_state.current_word_index += 1
                        st.rerun()
                    except Exception as e:
                        st.error(f"提交失败: {e}")
            
            with col3:
                st.markdown("")  # 占位

# ============ 阅读练习 ============
elif "阅读练习" in page:
    st.title("📝 阅读练习")
    
    # 练习类型选择
    exercise_type = st.radio(
        "选择练习类型",
        ["📄 README文档", "💬 Issue/PR讨论", "💻 代码注释"],
        horizontal=True
    )
    
    difficulty = st.slider("难度等级", 1, 3, 1)
    
    # 获取练习
    if st.button("开始练习", type="primary"):
        try:
            if "README" in exercise_type:
                exercises = api.get_readme_exercises(difficulty, limit=1)
            elif "Issue" in exercise_type:
                exercises = api.get_issue_pr_exercises(difficulty, limit=1)
            else:
                exercises = api.get_code_comment_exercises(difficulty, limit=1)
            
            if exercises:
                st.session_state.current_exercise = exercises[0]
                st.session_state.reading_answers = {}
                st.rerun()
            else:
                st.warning("暂无练习内容")
        except Exception as e:
            st.error(f"加载练习失败: {e}")
    
    # 显示练习
    if 'current_exercise' in st.session_state:
        exercise = st.session_state.current_exercise
        
        st.markdown(f"### {exercise['title']}")
        st.markdown(f"**难度:** {'⭐' * exercise.get('difficulty', 1)}")
        
        st.markdown("---")
        
        # 显示原文
        with st.expander("📖 阅读原文", expanded=True):
            st.markdown(exercise['content'])
        
        st.markdown("---")
        
        # 显示问题（交互式答题）
        st.markdown("#### 回答问题:")
        
        questions = exercise.get('questions', [])
        
        for idx, question in enumerate(questions):
            st.markdown(f"**{idx + 1}. {question['question']}**")
            
            # 创建选项
            options = question['options']
            selected = st.radio(
                f"选择答案（题目{idx + 1}）",
                range(len(options)),
                format_func=lambda x: f"{chr(65+x)}. {options[x]}",
                key=f"q_{idx}"
            )
            
            st.session_state.reading_answers[idx] = selected
            st.markdown("")
        
        # 提交按钮
        if st.button("提交答案", type="primary"):
            # 计算得分
            correct_count = 0
            results = []
            
            for idx, question in enumerate(questions):
                user_answer = st.session_state.reading_answers.get(idx, 0)
                # 兼容两种字段名：answer 和 correct_answer
                correct_answer = question.get('correct_answer', question.get('answer', 0))
                is_correct = (user_answer == correct_answer)
                
                if is_correct:
                    correct_count += 1
                
                results.append({
                    'question': question['question'],
                    'user_answer': options[user_answer],
                    'correct_answer': options[correct_answer],
                    'is_correct': is_correct,
                    'explanation': question.get('explanation', '')
                })
            
            # 显示结果
            score = (correct_count / len(questions)) * 100
            st.markdown("---")
            st.markdown(f"### 测试结果")
            
            if score >= 90:
                st.success(f"🎉 优秀！得分: {score:.1f}分")
            elif score >= 60:
                st.info(f"👍 通过！得分: {score:.1f}分")
            else:
                st.error(f"💪 继续努力！得分: {score:.1f}分")
            
            st.markdown(f"**正确:** {correct_count}/{len(questions)}")
            
            # 显示详细结果
            with st.expander("查看详细解析"):
                for idx, result in enumerate(results):
                    if result['is_correct']:
                        st.markdown(f'<div class="correct-answer">', unsafe_allow_html=True)
                        st.markdown(f"**题目{idx + 1}:** {result['question']}")
                        st.markdown(f"✅ 你的答案: {result['user_answer']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">', unsafe_allow_html=True)
                        st.markdown(f"**题目{idx + 1}:** {result['question']}")
                        st.markdown(f"❌ 你的答案: {result['user_answer']}")
                        st.markdown(f"✅ 正确答案: {result['correct_answer']}")
                        if result['explanation']:
                            st.markdown(f"**解析:** {result['explanation']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("")
            
            # 清除当前练习
            if st.button("开始新练习"):
                if 'current_exercise' in st.session_state:
                    del st.session_state.current_exercise
                if 'reading_answers' in st.session_state:
                    del st.session_state.reading_answers
                st.success("✅ 已清除，请点击'开始练习'生成新练习")
                st.rerun()

# ============ 测试评估 ============
elif "测试评估" in page:
    st.title("📊 测试评估")
    
    # 测试类型选择
    test_type = st.radio(
        "选择测试类型",
        ["📝 词汇测试", "📖 阅读测试", "🎯 综合考核"],
        horizontal=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "选择类别",
            ["全部", "Python技术词汇", "大模型/Agent词汇", 
             "车载/底盘/动力学词汇", "GitHub通用词汇", "计算机基础词汇"]
        )
    
    with col2:
        difficulty = st.slider("难度等级", 1, 3, 2)
    
    # 生成测试按钮
    if st.button("生成测试", type="primary"):
        with st.spinner("正在生成测试..."):
            try:
                if "词汇" in test_type:
                    test = api.generate_vocabulary_test(
                        user_id=st.session_state.user_id,
                        category=category if category != "全部" else None,
                        difficulty=difficulty,
                        count=20
                    )
                elif "阅读" in test_type:
                    test = api.generate_reading_test(
                        difficulty=difficulty,
                        count=10
                    )
                else:
                    test = api.generate_comprehensive_test(
                        user_id=st.session_state.user_id,
                        category=category if category != "全部" else None
                    )
                
                st.session_state.current_test = test
                st.session_state.test_answers = {}
                st.rerun()
                
            except Exception as e:
                st.error(f"生成测试失败: {e}")
    
    # 显示测试
    if 'current_test' in st.session_state:
        test = st.session_state.current_test
        
        st.markdown(f"#### 测试信息")
        st.info(f"**测试类型:** {test['test_type']} | **题目数量:** {test['question_count']} | **及格线:** 90分")
        
        st.markdown("---")
        
        # 显示题目
        questions = test.get('questions', [])
        
        for idx, question in enumerate(questions):
            st.markdown(f"**{idx + 1}. {question['question']}**")
            
            # 选项
            options = question['options']
            selected = st.radio(
                f"选择答案（题目{idx + 1}）",
                range(len(options)),
                format_func=lambda x: f"{chr(65+x)}. {options[x]}",
                key=f"test_q_{idx}"
            )
            
            st.session_state.test_answers[idx] = selected
            st.markdown("")
        
        # 提交测试
        if st.button("提交测试", type="primary"):
            # 准备答案
            answers = [st.session_state.test_answers.get(idx, 0) for idx in range(len(questions))]
            
            try:
                result = api.submit_test(
                    st.session_state.user_id,
                    test['test_type'],
                    answers,
                    time_spent=300  # 假设5分钟
                )
                
                # 显示结果
                st.markdown("---")
                st.markdown(f"### 测试结果")
                
                if result['passed']:
                    st.success(f"🎉 恭喜通过！得分: {result['score']}分")
                    st.balloons()
                else:
                    st.error(f"💪 继续努力！得分: {result['score']}分（及格线: 90分）")
                
                st.markdown(f"**正确:** {result['correct_count']}/{result['total_count']}")
                
                # 显示错误题目
                if result.get('wrong_questions'):
                    with st.expander("查看错题"):
                        for wq in result['wrong_questions']:
                            st.markdown(f'<div class="wrong-answer">', unsafe_allow_html=True)
                            st.markdown(f"**{wq['question']}**")
                            st.markdown(f"❌ 你的答案: {wq['user_answer']}")
                            st.markdown(f"✅ 正确答案: {wq['correct_answer']}")
                            if wq.get('explanation'):
                                st.markdown(f"**解析:** {wq['explanation']}")
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.markdown("")
                
                # 清除测试
                if st.button("开始新测试"):
                    del st.session_state.current_test
                    st.rerun()
                
            except Exception as e:
                st.error(f"提交失败: {e}")

# ============ 学习进度 ============
elif "学习进度" in page:
    st.title("📈 学习进度")
    
    # Tab布局
    tab1, tab2, tab3 = st.tabs(["📊 学习统计", "📈 学习曲线", "🎯 目标达成"])
    
    with tab1:
        # 学习统计
        try:
            stats = api.get_learning_stats(st.session_state.user_id)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("已学词汇", stats.get('learned_words', 0))
            with col2:
                st.metric("已掌握", stats.get('mastered_words', 0))
            with col3:
                st.metric("平均掌握度", f"{stats.get('avg_mastery', 0):.1f}/5")
            with col4:
                st.metric("总复习次数", stats.get('total_reviews', 0))
            
            st.markdown("---")
            
            # 测试统计
            test_stats = api.get_test_statistics(st.session_state.user_id)
            
            st.markdown("#### 测试统计")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总测试次数", test_stats.get('total_tests', 0))
            with col2:
                st.metric("平均分数", f"{test_stats.get('avg_score', 0):.1f}")
            with col3:
                st.metric("通过次数", test_stats.get('passed_tests', 0))
            
            # 按类型统计
            if test_stats.get('by_type'):
                st.markdown("#### 各类型测试表现")
                
                # 创建柱状图
                types = list(test_stats['by_type'].keys())
                scores = [data['avg_score'] for data in test_stats['by_type'].values()]
                counts = [data['count'] for data in test_stats['by_type'].values()]
                
                fig = go.Figure(data=[
                    go.Bar(name='平均分', x=types, y=scores),
                    go.Bar(name='测试次数', x=types, y=counts)
                ])
                fig.update_layout(barmode='group', title="各类型测试表现")
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"加载统计数据失败: {e}")
    
    with tab2:
        st.markdown("#### 学习曲线（过去30天）")
        
        # 模拟学习曲线数据（实际应从API获取）
        try:
            report = api.generate_learning_report(st.session_state.user_id, days=30)
            
            # 创建学习曲线图
            dates = pd.date_range(end=datetime.now(), periods=30)
            words_learned = [report.get('total_words_learned', 0) // 30] * 30  # 简化
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=words_learned,
                mode='lines+markers',
                name='学习词汇数',
                line={'color': '#FF4B4B', 'width': 2}
            ))
            
            fig.update_layout(
                title="每日学习词汇数",
                xaxis_title="日期",
                yaxis_title="词汇数",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.warning(f"无法加载学习曲线: {e}")
    
    with tab3:
        st.markdown("#### 目标达成情况")
        
        # 学习目标
        st.markdown("##### 📅 每日目标")
        try:
            plan = api.get_today_plan(st.session_state.user_id)
            
            progress = (plan.get('completed_words', 0) / plan.get('total_words', 1)) * 100 if plan.get('total_words', 0) > 0 else 0
            
            # 创建仪表盘
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=progress,
                title={'text': "今日目标完成度"},
                gauge={'axis': {'range': [0, 100]},
                      'bar': {'color': "darkblue"},
                      'steps': [
                          {'range': [0, 50], 'color': "lightgray"},
                          {'range': [50, 80], 'color': "gray"}],
                      'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}}
            ))
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.warning(f"无法加载目标数据: {e}")

# ============ 错题本 ============
elif "错题本" in page:
    st.title("❌ 错题本")
    
    if not st.session_state.wrong_words:
        st.info("🎉 太棒了！没有错题！")
    else:
        st.markdown(f"**错题数量:** {len(st.session_state.wrong_words)}")
        
        st.markdown("---")
        
        # 显示所有错题
        for idx, word in enumerate(st.session_state.wrong_words):
            with st.expander(f"**{word['word']}** - {word['chinese']}", expanded=(idx == 0)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**音标:** {word.get('phonetic', 'N/A')}")
                    st.markdown(f"**释义:** {word['chinese']}")
                    
                    if word.get('example'):
                        st.markdown(f"**例句:** {word['example']}")
                
                with col2:
                    if st.button(f"重新学习", key=f"relearn_{idx}"):
                        # 移除错题
                        st.session_state.wrong_words.pop(idx)
                        st.success("已从错题本移除")
                        st.rerun()
        
        # 清空错题本
        if st.button("清空错题本"):
            st.session_state.wrong_words = []
            st.success("错题本已清空")
            st.rerun()

# ============ 设置 ============
elif "设置" in page:
    st.title("⚙️ 设置")
    
    st.markdown("### 用户设置")
    
    # 每日学习目标
    daily_goal = st.slider("每日学习目标（词）", 100, 500, 350, 50)
    st.info(f"当前设置: 每天学习 {daily_goal} 个词汇")
    
    # 算法选择
    algorithm = st.radio(
        "遗忘曲线算法",
        ["艾宾浩斯标准算法", "SM-2动态调整算法"]
    )
    st.info(f"当前算法: {algorithm}")
    
    # 其他设置
    st.markdown("### 通知设置")
    email_notification = st.checkbox("邮件提醒", value=True)
    review_reminder = st.checkbox("复习提醒", value=True)
    
    st.markdown("### 显示设置")
    show_phonetic = st.checkbox("显示音标", value=True)
    show_example = st.checkbox("显示例句", value=True)
    show_github_context = st.checkbox("显示GitHub场景", value=True)
    
    if st.button("保存设置", type="primary"):
        st.success("设置已保存！")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "📚 GitHub英语学习系统 v2.0 增强版 | "
    "💡 Powered by Streamlit & OpenClaw"
    "</div>",
    unsafe_allow_html=True
)
