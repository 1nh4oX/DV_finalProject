"""
气候数据分析主程序
"""
from data_loader import ClimateDataLoader
from data_processor import ClimateDataProcessor
from visualizer import ClimateVisualizer

def main():
    print("=" * 70)
    print("  全球气候变化数据分析系统")
    print("  Global Climate Change Data Analysis System")
    print("=" * 70)
    
    # 初始化
    loader = ClimateDataLoader(data_dir='../data/raw')
    processor = ClimateDataProcessor()
    visualizer = ClimateVisualizer(output_dir='../output/figures')
    
    # 检查数据集
    print("\n📊 第一步：检查数据集...")
    print("-" * 70)
    data_info = loader.get_data_info()
    
    # 检查是否有数据
    has_data = any(info['exists'] for info in data_info.values())
    
    if not has_data:
        print("\n" + "=" * 70)
        print("⚠️  未找到数据文件！")
        print("=" * 70)
        print("\n请按以下步骤操作：")
        print("1. 访问 Kaggle：")
        print("   https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data")
        print("\n2. 下载数据集（约 300MB）")
        print("\n3. 解压到 climate/data/raw/ 文件夹")
        print("\n4. 重新运行此程序")
        print("=" * 70)
        return
    
    # 加载数据
    print("\n📥 第二步：加载数据...")
    print("-" * 70)
    
    try:
        # 加载全球温度数据
        print("加载全球温度数据...")
        df_global = loader.load_global_temperatures()
        
        # 加载国家温度数据
        print("\n加载国家温度数据...")
        df_country = loader.load_country_temperatures()
        
        # 加载城市温度数据
        print("\n加载城市温度数据...")
        df_city = loader.load_city_temperatures(major_cities_only=True)
        
    except FileNotFoundError as e:
        print(f"\n❌ 数据文件未找到: {e}")
        print("请确保已下载并解压数据到 data/raw/ 文件夹")
        return
    except Exception as e:
        print(f"\n❌ 加载数据时出错: {e}")
        return
    
    # 数据处理
    print("\n🔧 第三步：数据处理...")
    print("-" * 70)
    
    # 处理全球数据
    print("处理全球数据...")
    df_global_clean = processor.filter_by_year_range(df_global, start_year=1900)
    df_global_clean = processor.remove_missing_values(
        df_global_clean, 
        temp_column='LandAverageTemperature'
    )
    
    # 处理国家数据
    print("\n处理国家数据...")
    df_country_clean = processor.filter_by_year_range(df_country, start_year=1900)
    df_country_clean = processor.remove_missing_values(df_country_clean)
    df_country_clean = processor.filter_by_uncertainty(df_country_clean, max_uncertainty=2.0)
    
    # 处理城市数据
    print("\n处理城市数据...")
    df_city_clean = processor.filter_by_year_range(df_city, start_year=1900)
    df_city_clean = processor.remove_missing_values(df_city_clean)
    df_city_clean = processor.filter_by_uncertainty(df_city_clean, max_uncertainty=2.0)
    
    # 生成可视化
    print("\n🎨 第四步：生成可视化图表...")
    print("-" * 70)
    
    visualizer.generate_all_visualizations(
        df_global=df_global_clean,
        df_country=df_country_clean,
        df_city=df_city_clean
    )
    
    # 完成
    print("\n" + "=" * 70)
    print("🎉 分析完成！")
    print("=" * 70)
    print("\n📁 生成的文件：")
    print("  - 可视化图表: output/figures/")
    print("\n📝 接下来的步骤：")
    print("  1. 查看 output/figures/ 中的图表")
    print("  2. 分析图表，得出结论")
    print("  3. 撰写分析报告")
    print("=" * 70)


if __name__ == '__main__':
    main()

