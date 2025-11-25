"""
主程序 - 生成符合论文框架的高级气候可视化
"""
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import ClimateDataLoader
from advanced_visualizer import AdvancedClimateVisualizer


def main():
    """主函数"""
    print("\n" + "="*80)
    print("🌍 全球气候变化数据分析 - 高级可视化模块")
    print("📄 完全符合论文框架要求")
    print("🎨 使用 crest 配色主题")
    print("="*80 + "\n")
    
    # 初始化数据加载器
    print("📂 初始化数据加载器...")
    loader = ClimateDataLoader(data_dir='../data/raw')
    
    # 初始化可视化器
    print("🎨 初始化可视化器...")
    visualizer = AdvancedClimateVisualizer(output_dir='../output/advanced_figures')
    
    # ============================================================
    # 加载数据
    # ============================================================
    
    print("\n" + "="*80)
    print("📊 开始加载数据...")
    print("="*80 + "\n")
    
    try:
        # 1. 加载全球温度数据
        print("📥 [1/5] 加载全球温度数据...")
        df_global = loader.load_global_temperatures()
        print(f"   ✓ 全球温度数据：{len(df_global)} 条记录\n")
        
        # 2. 加载国家温度数据
        print("📥 [2/5] 加载国家温度数据...")
        df_country = loader.load_country_temperatures()
        print(f"   ✓ 国家温度数据：{len(df_country)} 条记录")
        print(f"   ✓ 涉及国家：{df_country['Country'].nunique()} 个\n")
        
        # 3. 加载城市温度数据（主要城市）
        print("📥 [3/5] 加载城市温度数据...")
        df_city = loader.load_city_temperatures(major_cities_only=True)
        print(f"   ✓ 城市温度数据：{len(df_city)} 条记录")
        print(f"   ✓ 涉及城市：{df_city['City'].nunique()} 个\n")
        
        # 4. 加载 CO2 数据（如果有）
        print("📥 [4/5] 加载 CO₂ 排放数据...")
        try:
            df_co2 = loader.load_co2_data()
            if df_co2 is not None and not df_co2.empty:
                print(f"   ✓ CO₂ 数据：{len(df_co2)} 条记录")
                print(f"   ✓ 涉及国家：{df_co2['country'].nunique()} 个")
                print(f"   ✓ 时间范围：{df_co2['year'].min()} - {df_co2['year'].max()}\n")
            else:
                print("   ⚠ CO₂ 数据不可用\n")
                df_co2 = None
        except Exception as e:
            print(f"   ⚠ CO₂ 数据加载失败：{e}\n")
            df_co2 = None
        
        # 5. 加载海平面数据（如果有）
        print("📥 [5/5] 加载海平面数据...")
        try:
            df_sea_level = loader.load_sea_level_data()
            if df_sea_level is not None and not df_sea_level.empty:
                print(f"   ✓ 海平面数据：{len(df_sea_level)} 条记录")
                print(f"   ✓ 时间范围：{df_sea_level['year'].min()} - {df_sea_level['year'].max()}\n")
            else:
                print("   ⚠ 海平面数据不可用\n")
                df_sea_level = None
        except Exception as e:
            print(f"   ⚠ 海平面数据加载失败：{e}\n")
            df_sea_level = None
        
    except Exception as e:
        print(f"\n❌ 数据加载失败：{e}")
        import traceback
        traceback.print_exc()
        return
    
    # ============================================================
    # 数据清洗
    # ============================================================
    
    print("="*80)
    print("🧹 数据清洗与预处理...")
    print("="*80 + "\n")
    
    try:
        # 清洗全球温度数据
        print("🧹 清洗全球温度数据...")
        df_global_clean = df_global.dropna(subset=['LandAverageTemperature'])
        print(f"   ✓ 清洗后：{len(df_global_clean)} 条记录（移除 {len(df_global) - len(df_global_clean)} 条空值）\n")
        
        # 清洗国家温度数据
        print("🧹 清洗国家温度数据...")
        df_country_clean = df_country.dropna(subset=['AverageTemperature'])
        print(f"   ✓ 清洗后：{len(df_country_clean)} 条记录（移除 {len(df_country) - len(df_country_clean)} 条空值）\n")
        
        # 清洗城市温度数据
        print("🧹 清洗城市温度数据...")
        df_city_clean = df_city.dropna(subset=['AverageTemperature', 'Latitude_num', 'Longitude_num'])
        print(f"   ✓ 清洗后：{len(df_city_clean)} 条记录（移除 {len(df_city) - len(df_city_clean)} 条空值）\n")
        
        # 清洗 CO2 数据
        if df_co2 is not None and not df_co2.empty:
            print("🧹 清洗 CO₂ 数据...")
            # 检查列名
            co2_col = 'co2_emission' if 'co2_emission' in df_co2.columns else 'value'
            df_co2_clean = df_co2.dropna(subset=[co2_col])
            # 统一列名
            if co2_col == 'value':
                df_co2_clean = df_co2_clean.rename(columns={'value': 'co2_emission'})
            print(f"   ✓ 清洗后：{len(df_co2_clean)} 条记录（移除 {len(df_co2) - len(df_co2_clean)} 条空值）\n")
        else:
            df_co2_clean = None
        
        # 清洗海平面数据
        if df_sea_level is not None and not df_sea_level.empty:
            print("🧹 清洗海平面数据...")
            # 检查列名
            sea_col = 'sea_level' if 'sea_level' in df_sea_level.columns else 'GMSL_noGIA'
            df_sea_level_clean = df_sea_level.dropna(subset=[sea_col])
            # 统一列名
            if sea_col == 'GMSL_noGIA':
                df_sea_level_clean = df_sea_level_clean.rename(columns={'GMSL_noGIA': 'sea_level'})
            print(f"   ✓ 清洗后：{len(df_sea_level_clean)} 条记录（移除 {len(df_sea_level) - len(df_sea_level_clean)} 条空值）\n")
        else:
            df_sea_level_clean = None
        
    except Exception as e:
        print(f"\n❌ 数据清洗失败：{e}")
        import traceback
        traceback.print_exc()
        return
    
    # ============================================================
    # 生成可视化
    # ============================================================
    
    print("="*80)
    print("🎨 开始生成高级可视化...")
    print("="*80 + "\n")
    
    try:
        visualizer.generate_all_visualizations(
            df_global=df_global_clean,
            df_country=df_country_clean,
            df_city=df_city_clean,
            df_co2=df_co2_clean,
            df_sea_level=df_sea_level_clean
        )
        
        print("\n" + "="*80)
        print("✅ 全部完成！")
        print("="*80 + "\n")
        
        # 输出总结
        print("📊 生成的可视化总结：\n")
        print("第一章：全球变暖是否持续？")
        print("  ├─ 01_long_term_trend.png - 全球温度长期趋势验证\n")
        
        print("第二章：变暖是否均匀？")
        print("  ├─ 02_country_heatmap_6_periods.png - 国家温度演变热力图（6个时期）")
        print("  └─ 03_regional_temperature_lines.png - 全球区域温度演变对比\n")
        
        print("第三章：城市层面发生了什么？")
        print("  ├─ 04_latitude_violin.png - 纬度带温度分布小提琴图")
        print("  └─ 05_city_temperature_boxplot.png - 主要城市温度箱线图\n")
        
        if df_co2_clean is not None:
            print("第四章：驱动因素在哪里？")
            print("  ├─ 06_co2_time_series.png - CO₂排放时间序列")
            print("  ├─ 07_co2_vs_temperature_regression.png - CO₂ vs 温度回归分析")
            print("  └─ 08_co2_jointplot.png - JointPlot（人均 vs 总排放）\n")
        
        if df_sea_level_clean is not None:
            print("第五章：后果是否已经显现？")
            print("  ├─ 09_sea_level_trend.png - 海平面变化趋势")
            print("  └─ 10_sea_level_vs_temperature.png - 海平面 vs 温度双轴图\n")
        
        print("第六章：综合验证")
        print("  └─ 11_pairplot.png - 多变量相关矩阵（PairPlot）\n")
        
        print(f"📁 所有图表已保存至：{visualizer.output_dir.absolute()}\n")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ 可视化生成失败：{e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == '__main__':
    main()

