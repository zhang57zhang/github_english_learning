-- 程序员GitHub英语学习系统 - 数据库Schema
-- SQLite数据库结构定义

-- ============================================
-- 1. 用户表（Users）
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    settings TEXT  -- JSON格式存储用户设置
);

-- ============================================
-- 2. 词汇表（Vocabulary）
-- ============================================
CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL,
    phonetic TEXT,
    part_of_speech TEXT,
    chinese TEXT NOT NULL,
    english TEXT,
    example TEXT,
    github_context TEXT,
    synonyms TEXT,  -- JSON数组
    antonyms TEXT,  -- JSON数组
    related_words TEXT,  -- JSON数组
    difficulty INTEGER DEFAULT 1,  -- 1=简单, 2=中等, 3=困难
    frequency TEXT DEFAULT 'medium',  -- high, medium, low
    category TEXT NOT NULL,  -- Python/LLM/Vehicle/GitHub/CS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 3. 词汇学习记录表（Learning Records）
-- ============================================
CREATE TABLE IF NOT EXISTS learning_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    first_learn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_review_time TIMESTAMP,
    next_review_time TIMESTAMP,  -- 下次复习时间（基于遗忘曲线）
    review_count INTEGER DEFAULT 0,  -- 复习次数
    correct_count INTEGER DEFAULT 0,  -- 正确次数
    wrong_count INTEGER DEFAULT 0,  -- 错误次数
    mastery_level INTEGER DEFAULT 0,  -- 掌握等级 (0-5)
    last_review_result TEXT,  -- 'correct', 'wrong', 'partial'
    review_intervals TEXT,  -- JSON数组：[1, 2, 4, 7, 15] 天
    current_interval_index INTEGER DEFAULT 0,  -- 当前间隔索引
    ease_factor REAL DEFAULT 2.5,  -- SM-2算法的难度因子
    status TEXT DEFAULT 'learning',  -- learning, reviewing, mastered
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (word_id) REFERENCES vocabulary(id),
    UNIQUE(user_id, word_id)  -- 每个用户对每个词汇只有一条记录
);

-- ============================================
-- 4. 复习计划表（Review Plans）
-- ============================================
CREATE TABLE IF NOT EXISTS review_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    review_date DATE NOT NULL,  -- 复习日期
    word_ids TEXT NOT NULL,  -- JSON数组：当日需要复习的词汇ID
    total_words INTEGER DEFAULT 0,  -- 总词汇数
    completed_words INTEGER DEFAULT 0,  -- 已完成词汇数
    correct_words INTEGER DEFAULT 0,  -- 正确词汇数
    wrong_words INTEGER DEFAULT 0,  -- 错误词汇数
    is_completed BOOLEAN DEFAULT 0,  -- 是否完成
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, review_date)  -- 每个用户每天只有一条计划
);

-- ============================================
-- 5. 学习进度表（Learning Progress）
-- ============================================
CREATE TABLE IF NOT EXISTS learning_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,  -- Python, LLM, Vehicle, GitHub, CS
    total_words INTEGER DEFAULT 0,  -- 总词汇数
    learned_words INTEGER DEFAULT 0,  -- 已学习词汇数
    mastered_words INTEGER DEFAULT 0,  -- 已掌握词汇数
    learning_days INTEGER DEFAULT 0,  -- 学习天数
    total_review_count INTEGER DEFAULT 0,  -- 总复习次数
    average_score REAL DEFAULT 0.0,  -- 平均分数
    streak_days INTEGER DEFAULT 0,  -- 连续学习天数
    last_study_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, category)  -- 每个用户每个类别只有一条记录
);

-- ============================================
-- 6. 测试记录表（Test Records）
-- ============================================
CREATE TABLE IF NOT EXISTS test_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    test_type TEXT NOT NULL,  -- vocabulary, reading, translation, comprehensive
    category TEXT,  -- Python, LLM, Vehicle, GitHub, CS
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    wrong_answers INTEGER DEFAULT 0,
    score REAL DEFAULT 0.0,  -- 分数 (0-100)
    time_spent INTEGER DEFAULT 0,  -- 用时（秒）
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,  -- JSON格式存储详细结果
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================
-- 7. 学习会话表（Study Sessions）
-- ============================================
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_type TEXT NOT NULL,  -- learn, review, test
    category TEXT,  -- Python, LLM, Vehicle, GitHub, CS
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    duration INTEGER DEFAULT 0,  -- 持续时间（秒）
    words_learned INTEGER DEFAULT 0,
    words_reviewed INTEGER DEFAULT 0,
    words_mastered INTEGER DEFAULT 0,
    score REAL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================
-- 8. 通知表（Notifications）
-- ============================================
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_type TEXT NOT NULL,  -- review_reminder, achievement, report
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================
-- 索引（Indexes）
-- ============================================
CREATE INDEX idx_learning_records_user ON learning_records(user_id);
CREATE INDEX idx_learning_records_word ON learning_records(word_id);
CREATE INDEX idx_learning_records_next_review ON learning_records(next_review_time);
CREATE INDEX idx_learning_records_status ON learning_records(status);

CREATE INDEX idx_review_plans_user_date ON review_plans(user_id, review_date);
CREATE INDEX idx_review_plans_date ON review_plans(review_date);

CREATE INDEX idx_learning_progress_user ON learning_progress(user_id);
CREATE INDEX idx_learning_progress_category ON learning_progress(category);

CREATE INDEX idx_vocabulary_category ON vocabulary(category);
CREATE INDEX idx_vocabulary_difficulty ON vocabulary(difficulty);

CREATE INDEX idx_test_records_user ON test_records(user_id);
CREATE INDEX idx_test_records_date ON test_records(test_date);

CREATE INDEX idx_study_sessions_user ON study_sessions(user_id);
CREATE INDEX idx_study_sessions_start ON study_sessions(start_time);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);

-- ============================================
-- 触发器（Triggers）
-- ============================================

-- 自动更新updated_at字段
CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS update_progress_timestamp 
AFTER UPDATE ON learning_progress
FOR EACH ROW
BEGIN
    UPDATE learning_progress SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- 当学习记录更新时，更新学习进度
CREATE TRIGGER IF NOT EXISTS update_progress_on_learn
AFTER INSERT ON learning_records
FOR EACH ROW
BEGIN
    INSERT OR IGNORE INTO learning_progress (user_id, category)
    SELECT NEW.user_id, v.category
    FROM vocabulary v
    WHERE v.id = NEW.word_id;
    
    UPDATE learning_progress
    SET learned_words = learned_words + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = NEW.user_id
      AND category = (SELECT category FROM vocabulary WHERE id = NEW.word_id);
END;

CREATE TRIGGER IF NOT EXISTS update_progress_on_master
AFTER UPDATE OF mastery_level ON learning_records
FOR EACH ROW
WHEN NEW.mastery_level >= 5 AND OLD.mastery_level < 5
BEGIN
    UPDATE learning_progress
    SET mastered_words = mastered_words + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = NEW.user_id
      AND category = (SELECT category FROM vocabulary WHERE id = NEW.word_id);
END;

-- ============================================
-- 视图（Views）
-- ============================================

-- 今日待复习词汇视图
CREATE VIEW IF NOT EXISTS today_review_words AS
SELECT 
    lr.user_id,
    v.id as word_id,
    v.word,
    v.phonetic,
    v.chinese,
    v.english,
    v.example,
    v.github_context,
    v.difficulty,
    v.category,
    lr.review_count,
    lr.mastery_level,
    lr.last_review_result
FROM learning_records lr
JOIN vocabulary v ON lr.word_id = v.id
WHERE DATE(lr.next_review_time) = DATE('now')
   OR lr.next_review_time IS NULL;

-- 用户学习统计视图
CREATE VIEW IF NOT EXISTS user_statistics AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(DISTINCT lr.word_id) as total_learned_words,
    COUNT(DISTINCT CASE WHEN lr.mastery_level >= 5 THEN lr.word_id END) as mastered_words,
    COUNT(DISTINCT CASE WHEN lr.status = 'learning' THEN lr.word_id END) as learning_words,
    SUM(lr.review_count) as total_reviews,
    AVG(lr.mastery_level) as avg_mastery_level,
    MAX(ss.start_time) as last_study_time
FROM users u
LEFT JOIN learning_records lr ON u.id = lr.user_id
LEFT JOIN study_sessions ss ON u.id = ss.user_id
GROUP BY u.id, u.username;

-- 词汇掌握情况视图
CREATE VIEW IF NOT EXISTS vocabulary_mastery AS
SELECT 
    v.category,
    v.difficulty,
    COUNT(DISTINCT lr.user_id) as user_count,
    AVG(lr.mastery_level) as avg_mastery,
    AVG(lr.review_count) as avg_reviews,
    COUNT(CASE WHEN lr.mastery_level >= 5 THEN 1 END) as mastered_count,
    COUNT(CASE WHEN lr.mastery_level < 5 THEN 1 END) as learning_count
FROM vocabulary v
LEFT JOIN learning_records lr ON v.id = lr.word_id
GROUP BY v.category, v.difficulty;
