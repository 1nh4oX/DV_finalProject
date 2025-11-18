#!/bin/bash
# 激活虚拟环境的便捷脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 激活虚拟环境
source "$SCRIPT_DIR/venv/bin/activate"

echo "✅ 虚拟环境已激活！"
echo "📍 当前目录: $SCRIPT_DIR"
echo ""
echo "💡 常用命令："
echo "   python main.py              # 生成数据和图表"
echo "   python run_amap_collector.py YOUR_KEY  # 采集真实数据"
echo "   jupyter notebook            # 启动Jupyter"
echo ""
echo "⚠️  退出虚拟环境: deactivate"

