#!/bin/bash
echo "===================================="
echo "GitHub English Learning System"
echo "Starting..."
echo "===================================="
echo

cd "$(dirname "$0")"

echo "[1/3] Checking Python environment..."
python3 --version
if [ $? -ne 0 ]; then
    echo "[ERROR] Python not found. Please install Python 3.11+"
    exit 1
fi

echo
echo "[2/3] Installing dependencies..."
pip3 install streamlit plotly pandas -q

echo
echo "[3/3] Starting Streamlit application..."
echo
echo "===================================="
echo "Web URL: http://localhost:8501"
echo "===================================="
echo

streamlit run frontend/app_enhanced.py --server.port 8501
