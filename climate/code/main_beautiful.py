"""
运行美化版可视化
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import ClimateDataLoader
from beautiful_visualizer import BeautifulClimateVisualizer


def main():
    print("\n🎨 美化版气候可视化 - 参考 Seaborn 官方最佳实践\n")
    
    # 加载数据
    loader = ClimateDataLoader(data_dir='../data/raw')
    
    print("📥 加载数据...")
    df_global = loader.load_global_temperatures()
    df_country = loader.load_country_temperatures()
    df_city = loader.load_city_temperatures(major_cities_only=True)
    
    try:
        df_co2 = loader.load_co2_data()
    except:
        df_co2 = None
    
    try:
        df_sea_level = loader.load_sea_level_data()
    except:
        df_sea_level = None
    
    # 清洗数据
    print("\n🧹 清洗数据...")
    df_global_clean = df_global.dropna(subset=['LandAverageTemperature'])
    df_country_clean = df_country.dropna(subset=['AverageTemperature'])
    df_city_clean = df_city.dropna(subset=['AverageTemperature', 'Latitude_num'])
    
    if df_co2 is not None:
        df_co2_clean = df_co2.dropna(subset=['co2_emission'])
        if 'value' in df_co2_clean.columns and 'co2_emission' not in df_co2_clean.columns:
            df_co2_clean = df_co2_clean.rename(columns={'value': 'co2_emission'})
        if 'country_name' in df_co2_clean.columns:
            df_co2_clean = df_co2_clean.rename(columns={'country_name': 'country'})
        if 'co2_per_capita' not in df_co2_clean.columns:
            df_co2_clean['co2_per_capita'] = df_co2_clean['co2_emission'] / 1e6
    else:
        df_co2_clean = None
    
    if df_sea_level is not None:
        df_sea_level_clean = df_sea_level.dropna()
        if 'GMSL_noGIA' in df_sea_level_clean.columns and 'sea_level' not in df_sea_level_clean.columns:
            df_sea_level_clean = df_sea_level_clean.rename(columns={'GMSL_noGIA': 'sea_level'})
    else:
        df_sea_level_clean = None
    
    # 生成美化图表
    visualizer = BeautifulClimateVisualizer(output_dir='../output/beautiful_figures')
    visualizer.generate_all(
        df_global=df_global_clean,
        df_country=df_country_clean,
        df_city=df_city_clean,
        df_co2=df_co2_clean,
        df_sea_level=df_sea_level_clean
    )
    
    print("\n✅ 完成！")


if __name__ == '__main__':
    main()

