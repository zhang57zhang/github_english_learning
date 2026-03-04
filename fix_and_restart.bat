@echo off
chcp 65001 >nul
echo ====================================
echo GitHub英语学习系统 - 一键修复
echo ====================================
echo.

echo [1/4] 停止旧进程...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] 更新代码...
cd /d "%~dp0"
git fetch origin
git reset --hard origin/main
git pull

echo [3/4] 清理缓存...
del /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul

echo [4/4] 重新启动...
echo.
echo ====================================
echo 🌐 访问地址: http://localhost:8501
echo ====================================
echo.

start "" streamlit run frontend/app_enhanced.py --server.port 8501

echo ✅ 修复完成！
echo.
echo 如果浏览器没有自动打开，请手动访问：
echo http://localhost:8501
echo.
pause
