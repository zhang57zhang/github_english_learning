#!/bin/bash

echo "===================================="
echo "GitHub英语学习系统 - 启动中..."
echo "===================================="
echo ""

# 进入脚本所在目录
cd "$(dirname "$0")"

echo "[1/3] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi
python3 --version

echo ""
echo "[2/3] 安装依赖..."
pip3 install streamlit plotly pandas -q

echo ""
echo "[3/3] 启动Streamlit应用..."
echo ""
echo "===================================="
echo "🌐 访问地址: http://localhost:8501"
echo "===================================="
echo ""

streamlit run frontend/app_enhanced.py --server.port 8501
