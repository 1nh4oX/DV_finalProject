"""
深圳交通数据分析主程序
一键生成所有数据和可视化图表
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import ShenzhenTrafficDataGenerator
from visualizer import TrafficVisualizer


def main():
    """主函数"""
    print("="*70)
    print("  深圳城市交通与出行模式分析系统")
    print("  Shenzhen Traffic and Travel Pattern Analysis System")
    print("="*70)
    print()
    
    # 步骤1：生成数据
    print("📊 第一步：生成模拟数据...")
    print("-"*70)
    
    generator = ShenzhenTrafficDataGenerator()
    datasets = generator.generate_all_data()
    
    # 保存数据
    data_dir = 'data/sample'
    os.makedirs(data_dir, exist_ok=True)
    
    for name, df in datasets.items():
        filepath = os.path.join(data_dir, f'{name}.csv')
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"  ✓ {name}: {len(df)} 条记录")
    
    print()
    print(f"✅ 数据生成完成！共 {len(datasets)} 个数据集")
    print()
    
    # 步骤2：生成可视化
    print("🎨 第二步：生成可视化图表...")
    print("-"*70)
    
    visualizer = TrafficVisualizer(data_dir=data_dir, output_dir='outputs/figures')
    visualizer.generate_all_visualizations()
    
    print()
    print("="*70)
    print("🎉 分析完成！")
    print()
    print("📁 生成的文件：")
    print("  - 数据文件: data/sample/")
    print("  - 可视化图表: outputs/figures/")
    print()
    print("📝 接下来的步骤：")
    print("  1. 查看 outputs/figures/ 中的图表")
    print("  2. 阅读自动生成的分析报告")
    print("  3. 根据可视化结果撰写论文")
    print("="*70)


if __name__ == '__main__':
    main()

