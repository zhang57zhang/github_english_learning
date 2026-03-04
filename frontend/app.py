#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub英语学习系统 - Streamlit前端主程序
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import GitHubEnglishLearningAPI

# 页面配置
st.set_page_config(
    page_title="GitHub英语学习系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化API
@st.cache_resource
def init_api():
    return GitHubEnglishLearningAPI()

api = init_api()

# 会话状态管理
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1  # 默认用户

if 'current_page' not in st.session_state:
    st.session_state.current_page = "学习中心"

if 'learning_mode' not in st.session_state:
    st.session_state.learning_mode = 'new'

if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0

# 侧边栏
st.sidebar.title("📚 GitHub英语学习")
st.sidebar.markdown("---")

# 页面选择
page = st.sidebar.radio(
    "导航",
    ["🏠 学习中心", "📖 词汇学习", "📝 阅读练习", "📊 测试评估", "📈 学习进度", "⚙️ 设置"],
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
except:
    st.sidebar.warning("无法加载统计数据")

# 主内容区
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
        
    except Exception as e:
        st.error(f"加载学习计划失败: {e}")
    
    st.markdown("---")
    
    # 快速开始
    st.markdown("#### 🚀 快速开始")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 开始学习新词汇", use_container_width=True):
            st.session_state.learning_mode = 'new'
            st.session_state.current_page = "词汇学习"
            st.rerun()
    
    with col2:
        if st.button("🔄 复习旧词汇", use_container_width=True):
            st.session_state.learning_mode = 'review'
            st.session_state.current_page = "词汇学习"
            st.rerun()
    
    with col3:
        if st.button("📝 阅读练习", use_container_width=True):
            st.session_state.current_page = "阅读练习"
            st.rerun()
    
    st.markdown("---")
    
    # 学习统计
    st.markdown("#### 📊 学习统计")
    try:
        report = api.generate_learning_report(st.session_state.user_id, days=7)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**过去7天学习:** {report.get('total_words_learned', 0)} 词")
            st.info(f"**总复习次数:** {report.get('total_reviews', 0)} 次")
        
        with col2:
            st.info(f"**平均正确率:** {report.get('average_accuracy', 0):.1%}")
            st.info(f"**弱项领域:** {len(report.get('weak_areas', []))} 个")
            
    except Exception as e:
        st.warning(f"无法加载学习报告: {e}")

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
    
    # 获取词汇
    try:
        words = api.get_learning_words(
            st.session_state.user_id, 
            mode=learning_mode, 
            limit=10
        )
        
        if not words:
            st.info("🎉 太棒了！没有需要学习的词汇了！")
        else:
            # 当前词汇索引
            if st.session_state.current_word_index >= len(words):
                st.session_state.current_word_index = 0
            
            word = words[st.session_state.current_word_index]
            
            # 词汇卡片
            st.markdown(f"### {word['word']}")
            if word.get('phonetic'):
                st.markdown(f"**音标:** {word['phonetic']}")
            
            st.markdown(f"**释义:** {word['chinese']}")
            
            if word.get('example'):
                with st.expander("📝 查看例句"):
                    st.markdown(word['example'])
            
            if word.get('github_context'):
                with st.expander("💼 GitHub场景"):
                    st.markdown(word['github_context'])
            
            # 掌握等级
            difficulty = word.get('difficulty', 1)
            difficulty_emoji = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐"}
            st.markdown(f"**难度:** {difficulty_emoji.get(difficulty, '⭐')}")
            
            # 学习按钮
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("❌ 不认识", use_container_width=True):
                    result = api.submit_learning_result(
                        st.session_state.user_id,
                        word['id'],
                        False
                    )
                    st.success(f"继续努力！掌握度: {result.get('mastery_level', 0)}/5")
                    st.session_state.current_word_index += 1
                    st.rerun()
            
            with col2:
                if st.button("✅ 认识", use_container_width=True):
                    result = api.submit_learning_result(
                        st.session_state.user_id,
                        word['id'],
                        True
                    )
                    st.success(f"很好！掌握度: {result.get('mastery_level', 0)}/5")
                    st.session_state.current_word_index += 1
                    st.rerun()
            
            with col3:
                st.markdown(f"**进度:** {st.session_state.current_word_index + 1} / {len(words)}")
    
    except Exception as e:
        st.error(f"加载词汇失败: {e}")

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
    try:
        if "README" in exercise_type:
            exercises = api.get_readme_exercises(difficulty)
        elif "Issue" in exercise_type:
            exercises = api.get_issue_pr_exercises(difficulty)
        else:
            exercises = api.get_code_comment_exercises(difficulty)
        
        if not exercises:
            st.info("暂无练习内容")
        else:
            exercise = exercises[0]  # 显示第一个练习
            
            st.markdown(f"### {exercise['title']}")
            
            # 显示内容
            with st.expander("📖 阅读原文", expanded=True):
                st.markdown(exercise['content'])
            
            # 显示问题
            st.markdown("#### 问题:")
            for idx, question in enumerate(exercise['questions']):
                st.markdown(f"**{idx + 1}. {question['question']}**")
                
                # 选项
                for opt_idx, option in enumerate(question['options']):
                    st.markdown(f"  {chr(65+opt_idx)}. {option}")
                
                st.markdown("")  # 空行
            
            # 答案（可选显示）
            if st.checkbox("显示答案"):
                st.markdown("#### 答案:")
                for idx, question in enumerate(exercise['questions']):
                    answer_idx = question['correct_answer']
                    st.info(f"{idx + 1}. {chr(65+answer_idx)}. {question['options'][answer_idx]}")
    
    except Exception as e:
        st.error(f"加载练习失败: {e}")

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
                        st.session_state.user_id,
                        category if category != "全部" else None,
                        difficulty,
                        20
                    )
                elif "阅读" in test_type:
                    test = api.generate_reading_test(difficulty, 10)
                else:
                    test = api.generate_comprehensive_test(
                        st.session_state.user_id,
                        category if category != "全部" else None
                    )
                
                st.session_state.current_test = test
                st.session_state.test_answers = []
                st.rerun()
                
            except Exception as e:
                st.error(f"生成测试失败: {e}")
    
    # 显示测试
    if 'current_test' in st.session_state:
        test = st.session_state.current_test
        
        st.markdown(f"#### 测试信息")
        st.info(f"**题目数量:** {test['question_count']} | **及格线:** 90分")
        
        # 显示题目（简化版，实际应该有答题界面）
        st.markdown("#### 测试题目已生成")
        st.json({
            "test_type": test['test_type'],
            "question_count": test['question_count']
        })
        
        if st.button("提交测试（演示）"):
            # 模拟提交
            answers = [0] * test['question_count']  # 全选A
            result = api.submit_test(
                st.session_state.user_id,
                test['test_type'],
                answers
            )
            
            st.success(f"测试完成！得分: {result['score']}分")
            if result['passed']:
                st.balloons()
            else:
                st.warning("继续努力！")
            
            del st.session_state.current_test

elif "学习进度" in page:
    st.title("📈 学习进度")
    
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
            for test_type, data in test_stats['by_type'].items():
                st.markdown(f"- **{test_type}:** {data['count']}次，平均分 {data['avg_score']}")
        
    except Exception as e:
        st.error(f"加载统计数据失败: {e}")

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
    
    if st.button("保存设置", type="primary"):
        st.success("设置已保存！")

# 关闭API连接
# api.close()  # Streamlit会自动管理

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "📚 GitHub英语学习系统 v1.0 | "
    "💡 Powered by Streamlit & OpenClaw"
    "</div>",
    unsafe_allow_html=True
)
