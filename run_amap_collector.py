"""
高德API数据采集 - 便捷运行脚本
自动更新Key并运行采集
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from amap_api_example import AmapDataCollector
import pandas as pd

def main():
    """主函数"""
    print("="*70)
    print("  高德地图API数据采集工具")
    print("="*70)
    print()
    
    # 获取API Key
    import sys
    
    # 方式1: 从命令行参数获取
    if len(sys.argv) > 1:
        api_key = sys.argv[1].strip()
        print(f"从命令行参数获取Key: {api_key[:10]}...{api_key[-4:]}")
    else:
        # 方式2: 交互式输入
        print("请输入您的高德Web服务API Key：")
        print("（在控制台找到：https://console.amap.com/dev/key/app）")
        print("（选择'Web服务'类型的Key）")
        print("（或使用: python3 run_amap_collector.py YOUR_KEY）")
        print()
        
        try:
            api_key = input("API Key: ").strip()
        except EOFError:
            print("\n❌ 无法交互式输入")
            print("💡 请使用命令行参数: python3 run_amap_collector.py YOUR_KEY")
            return
        
        if not api_key:
            print("\n❌ 未输入Key，退出")
            return
    
    # 移除可能的引号
    api_key = api_key.strip("'\"")
    
    print(f"\n✓ 使用Key: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    # 初始化采集器
    collector = AmapDataCollector(api_key)
    
    # 测试Key
    print("【步骤1】测试API Key...")
    print("-"*70)
    test_url = 'https://restapi.amap.com/v3/ip'
    import requests
    try:
        response = requests.get(test_url, params={'key': api_key, 'output': 'json'}, timeout=5)
        test_data = response.json()
        if test_data.get('status') == '1':
            print("✅ Key测试通过！")
        else:
            print(f"❌ Key测试失败: {test_data.get('info')}")
            print("   请检查Key是否正确")
            return
    except Exception as e:
        print(f"⚠️  测试请求异常: {e}")
        print("   继续尝试采集数据...")
    
    print()
    
    # 采集实时交通数据
    print("【步骤2】采集深圳市实时交通状态...")
    print("-"*70)
    print("⚠️  注意：交通态势API可能需要先在高德控制台开通服务")
    print("   如果失败，我们将继续采集OD路径数据...")
    print()
    
    raw_traffic = collector.get_traffic_status()
    
    if raw_traffic:
        df_traffic = collector.parse_traffic_data(raw_traffic)
        print(f"\n✅ 成功获取 {len(df_traffic)} 条道路数据")
        print("\n数据预览:")
        print(df_traffic.head(10))
        
        # 保存数据
        os.makedirs('data/raw', exist_ok=True)
        output_file = 'data/raw/traffic_realtime.csv'
        df_traffic.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 数据已保存: {output_file}")
        
        # 统计信息
        print("\n📊 数据统计:")
        print(f"  总道路数: {len(df_traffic)}")
        print(f"  平均速度: {df_traffic['speed'].mean():.2f} km/h")
        print(f"  拥堵道路数: {len(df_traffic[df_traffic['status'] >= 3])}")
        print(f"  畅通道路数: {len(df_traffic[df_traffic['status'] == 1])}")
    else:
        print("⚠️  交通态势API暂时不可用（可能需要开通服务）")
        print("   继续采集其他可用数据...")
    
    print()
    
    # 采集OD路径数据
    print("【步骤3】采集OD路径数据...")
    print("-"*70)
    print("（这将进行多次API调用，可能需要1-2分钟）")
    print()
    
    # 使用主要地点进行OD分析
    od_locations = {
        '市民中心': collector.key_locations['市民中心'],
        '深圳北站': collector.key_locations['深圳北站'],
        '科技园': collector.key_locations['科技园'],
        '华强北': collector.key_locations['华强北'],
        '前海': collector.key_locations['前海']
    }
    
    print(f"采集 {len(od_locations)} 个地点之间的路径数据...")
    df_od = collector.collect_od_matrix(od_locations)
    
    if not df_od.empty:
        print("\n✅ OD数据采集完成！")
        print("\n数据预览:")
        print(df_od)
        
        os.makedirs('data/raw', exist_ok=True)
        output_file = 'data/raw/od_matrix_amap.csv'
        df_od.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ OD数据已保存: {output_file}")
        
        # 统计信息
        print("\n📊 OD数据统计:")
        print(f"  总路径数: {len(df_od)}")
        print(f"  平均距离: {df_od['distance'].mean()/1000:.2f} km")
        print(f"  平均时间: {df_od['duration'].mean()/60:.1f} 分钟")
    else:
        print("\n⚠️  未能获取OD数据")
    
    print()
    print("="*70)
    print("✅ 数据采集完成！")
    print()
    print("📁 生成的文件：")
    files_generated = []
    if os.path.exists('data/raw/traffic_realtime.csv'):
        files_generated.append("  - data/raw/traffic_realtime.csv  (实时交通数据)")
    if os.path.exists('data/raw/od_matrix_amap.csv'):
        files_generated.append("  - data/raw/od_matrix_amap.csv  (OD路径数据)")
    
    if files_generated:
        for f in files_generated:
            print(f)
    else:
        print("  （暂无数据文件）")
    
    print()
    print("💡 下一步：")
    print("  1. 查看采集的数据: cat data/raw/od_matrix_amap.csv")
    print("  2. 可以多次运行此脚本采集不同时段的数据")
    print("  3. 使用采集的数据替换模拟数据进行分析")
    print()
    print("📝 关于交通态势API：")
    print("  如果交通态势API返回INVALID_PARAMS，可能需要：")
    print("  1. 在高德控制台开通'交通态势'服务")
    print("  2. 或使用其他可用的API（如路径规划）")
    print("="*70)


if __name__ == '__main__':
    main()
