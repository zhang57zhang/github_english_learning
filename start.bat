@echo off
chcp 65001 >nul
echo ====================================
echo GitHub英语学习系统 - 启动中...
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo.
echo [2/3] 安装依赖...
pip install streamlit plotly pandas -q
if errorlevel 1 (
    echo ⚠️ 依赖安装失败，但继续尝试启动
)

echo.
echo [3/3] 启动Streamlit应用...
echo.
echo ====================================
echo 🌐 访问地址: http://localhost:8501
echo ====================================
echo.

streamlit run frontend/app_enhanced.py --server.port 8501

pause
