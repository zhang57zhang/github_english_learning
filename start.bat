@echo off
echo ====================================
echo GitHub English Learning System
echo Starting...
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

echo.
echo [2/3] Installing dependencies...
pip install streamlit plotly pandas -q
if errorlevel 1 (
    echo [WARN] Dependency installation failed, but continuing...
)

echo.
echo [3/3] Starting Streamlit application...
echo.
echo ====================================
echo Web URL: http://localhost:8501
echo ====================================
echo.

streamlit run frontend/app_enhanced.py --server.port 8501

pause
