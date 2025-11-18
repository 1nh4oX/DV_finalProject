"""
气候数据加载模块
"""
import pandas as pd
import numpy as np
from pathlib import Path

class ClimateDataLoader:
    """气候数据加载器"""
    
    def __init__(self, data_dir='../data/raw'):
        self.data_dir = Path(data_dir)
        
    def load_global_temperatures(self):
        """加载全球温度数据"""
        file_path = self.data_dir / 'GlobalTemperatures.csv'
        print(f"正在加载全球温度数据: {file_path}")
        
        df = pd.read_csv(file_path)
        df['dt'] = pd.to_datetime(df['dt'])
        df['year'] = df['dt'].dt.year
        df['month'] = df['dt'].dt.month
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        return df
    
    def load_city_temperatures(self, major_cities_only=True):
        """加载城市温度数据
        
        Args:
            major_cities_only: 是否只加载主要城市
        """
        if major_cities_only:
            file_path = self.data_dir / 'GlobalLandTemperaturesByMajorCity.csv'
            print(f"正在加载主要城市温度数据: {file_path}")
        else:
            file_path = self.data_dir / 'GlobalLandTemperaturesByCity.csv'
            print(f"正在加载所有城市温度数据: {file_path}")
        
        df = pd.read_csv(file_path)
        df['dt'] = pd.to_datetime(df['dt'])
        df['year'] = df['dt'].dt.year
        df['month'] = df['dt'].dt.month
        
        # 解析经纬度
        df['Latitude_num'] = df['Latitude'].apply(self._parse_coordinate)
        df['Longitude_num'] = df['Longitude'].apply(self._parse_coordinate)
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        print(f"  城市数量: {df['City'].nunique()}")
        print(f"  国家数量: {df['Country'].nunique()}")
        
        return df
    
    def load_country_temperatures(self):
        """加载国家温度数据"""
        file_path = self.data_dir / 'GlobalLandTemperaturesByCountry.csv'
        print(f"正在加载国家温度数据: {file_path}")
        
        df = pd.read_csv(file_path)
        df['dt'] = pd.to_datetime(df['dt'])
        df['year'] = df['dt'].dt.year
        df['month'] = df['dt'].dt.month
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        print(f"  国家数量: {df['Country'].nunique()}")
        
        return df
    
    def load_state_temperatures(self):
        """加载州/省温度数据"""
        file_path = self.data_dir / 'GlobalLandTemperaturesByState.csv'
        print(f"正在加载州/省温度数据: {file_path}")
        
        df = pd.read_csv(file_path)
        df['dt'] = pd.to_datetime(df['dt'])
        df['year'] = df['dt'].dt.year
        df['month'] = df['dt'].dt.month
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        
        return df
    
    @staticmethod
    def _parse_coordinate(coord_str):
        """解析经纬度字符串
        
        Examples:
            '41.78N' -> 41.78
            '87.68W' -> -87.68
            '23.13S' -> -23.13
            '116.38E' -> 116.38
        """
        if pd.isna(coord_str):
            return np.nan
        
        try:
            # 提取数字和方向
            value = float(coord_str[:-1])
            direction = coord_str[-1]
            
            # 南纬和西经为负
            if direction in ['S', 'W']:
                value = -value
            
            return value
        except:
            return np.nan
    
    def get_data_info(self):
        """获取数据集信息"""
        info = {}
        
        files = {
            'GlobalTemperatures.csv': '全球温度',
            'GlobalLandTemperaturesByCity.csv': '城市温度（全部）',
            'GlobalLandTemperaturesByMajorCity.csv': '主要城市温度',
            'GlobalLandTemperaturesByCountry.csv': '国家温度',
            'GlobalLandTemperaturesByState.csv': '州/省温度'
        }
        
        print("=" * 60)
        print("数据集信息")
        print("=" * 60)
        
        for filename, desc in files.items():
            file_path = self.data_dir / filename
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                info[filename] = {
                    'description': desc,
                    'size_mb': round(size_mb, 2),
                    'exists': True
                }
                print(f"✓ {desc:20s} - {filename:50s} ({size_mb:.2f} MB)")
            else:
                info[filename] = {
                    'description': desc,
                    'exists': False
                }
                print(f"✗ {desc:20s} - {filename:50s} (未找到)")
        
        print("=" * 60)
        return info


if __name__ == '__main__':
    # 测试数据加载
    loader = ClimateDataLoader()
    
    # 显示数据集信息
    loader.get_data_info()
    
    # 测试加载数据（如果文件存在）
    try:
        df_global = loader.load_global_temperatures()
        print(f"\n全球温度数据预览：")
        print(df_global.head())
        print(f"\n时间范围：{df_global['year'].min()} - {df_global['year'].max()}")
    except FileNotFoundError:
        print("\n⚠️  请先下载数据集到 data/raw/ 文件夹")
        print("   下载地址: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data")

