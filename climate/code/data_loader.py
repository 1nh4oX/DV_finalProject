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
    
    def load_co2_data(self):
        """加载CO2排放数据
        
        支持数据集：
        - CO2 Emissions by Country: https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country
        
        预期文件格式：
        - 列：year, country, co2_emissions, 或类似格式
        - 或：date, country, co2
        """
        # 尝试多个可能的文件位置
        possible_paths = [
            self.data_dir / 'co2' / 'co2_emissions_by_country.csv',
            self.data_dir / 'co2' / 'co2-emissions-by-country.csv',
            self.data_dir / 'co2' / 'co2_data.csv',
            self.data_dir / 'co2_data.csv',
            self.data_dir / 'co2.csv'
        ]
        
        # 尝试直接查找co2相关文件
        if (self.data_dir / 'co2').exists():
            possible_paths.extend(list((self.data_dir / 'co2').glob('*.csv')))
        possible_paths.extend(list(self.data_dir.glob('*co2*.csv')))
        
        file_path = None
        for path in possible_paths:
            if path.exists() and path.is_file():
                file_path = path
                break
        
        if file_path is None:
            print("⚠️  CO2数据文件未找到")
            print("   请下载CO2数据到以下位置之一：")
            print("   - climate/data/raw/co2/co2_emissions_by_country.csv")
            print("   - climate/data/raw/co2_data.csv")
            print("   数据集链接: https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country")
            return None
        
        print(f"正在加载CO2数据: {file_path}")
        df = pd.read_csv(file_path)
        
        print(f"  数据列: {list(df.columns)}")
        
        # 尝试解析日期列
        date_cols = ['date', 'Date', 'dt', 'Dt', 'year_month', 'Year', 'year']
        year_col = None
        for col in date_cols:
            if col.lower() in [c.lower() for c in df.columns]:
                actual_col = [c for c in df.columns if c.lower() == col.lower()][0]
                if col.lower() == 'year':
                    df['year'] = pd.to_numeric(df[actual_col], errors='coerce')
                    year_col = 'year'
                else:
                    try:
                        df[actual_col] = pd.to_datetime(df[actual_col], errors='coerce')
                        df['year'] = df[actual_col].dt.year
                        df['month'] = df[actual_col].dt.month
                        year_col = 'year'
                    except:
                        pass
                if year_col:
                    break
        
        if year_col is None:
            # 尝试从文件名或其他列推断年份
            print("⚠️  未找到年份列，尝试从数据推断...")
            # 检查是否有数值列可能是年份
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    sample = df[col].dropna().head(100)
                    if len(sample) > 0 and sample.min() >= 1800 and sample.max() <= 2100:
                        df['year'] = df[col]
                        year_col = 'year'
                        print(f"  推断年份列: {col}")
                        break
        
        # 查找CO2列（支持多种命名）
        co2_cols = ['co2', 'CO2', 'co2_emissions', 'CO2_emissions', 'co2_ppm', 'CO2_ppm', 
                   'carbon_dioxide', 'Carbon Dioxide', 'emission', 'Emissions',
                   'total_co2', 'Total CO2', 'co2_kt', 'CO2_kt']
        co2_col = None
        for col in df.columns:
            col_lower = col.lower()
            for co2_pattern in co2_cols:
                if co2_pattern.lower() in col_lower:
                    co2_col = col
                    break
            if co2_col:
                break
        
        if co2_col is None:
            print("⚠️  未找到CO2排放列")
            print(f"   可用列: {list(df.columns)}")
            return None
        
        # 确保年份列存在
        if 'year' not in df.columns:
            print("⚠️  无法确定年份列")
            return None
        
        # 清理数据
        df = df.dropna(subset=[co2_col, 'year'])
        df['year'] = df['year'].astype(int)
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        if 'year' in df.columns:
            print(f"  时间范围：{df['year'].min()} - {df['year'].max()}")
        print(f"  CO2列：{co2_col}")
        if 'Country' in df.columns or 'country' in df.columns:
            country_col = 'Country' if 'Country' in df.columns else 'country'
            print(f"  国家数量：{df[country_col].nunique()}")
        
        return df
    
    def load_sea_level_data(self):
        """加载海平面高度数据
        
        支持数据集：
        - Global Sea Level 1993-2021: https://www.kaggle.com/datasets/kkhandekar/global-sea-level-1993-2021
        
        预期文件格式：
        - 列：year, sea_level_mm, 或类似格式
        - 或：date, sea_level
        """
        possible_paths = [
            self.data_dir / 'sea_level' / 'global-sea-level-1993-2021.csv',
            self.data_dir / 'sea_level' / 'sea_level_data.csv',
            self.data_dir / 'sea_level' / 'noaa_sea_level.csv',
            self.data_dir / 'sea_level_data.csv',
            self.data_dir / 'sea_level.csv'
        ]
        
        # 尝试直接查找sea level相关文件
        if (self.data_dir / 'sea_level').exists():
            possible_paths.extend(list((self.data_dir / 'sea_level').glob('*.csv')))
        possible_paths.extend(list(self.data_dir.glob('*sea*level*.csv')))
        
        file_path = None
        for path in possible_paths:
            if path.exists() and path.is_file():
                file_path = path
                break
        
        if file_path is None:
            print("⚠️  海平面数据文件未找到")
            print("   请下载海平面数据到以下位置之一：")
            print("   - climate/data/raw/sea_level/global-sea-level-1993-2021.csv")
            print("   - climate/data/raw/sea_level_data.csv")
            print("   数据集链接: https://www.kaggle.com/datasets/kkhandekar/global-sea-level-1993-2021")
            return None
        
        print(f"正在加载海平面数据: {file_path}")
        df = pd.read_csv(file_path)
        
        print(f"  数据列: {list(df.columns)}")
        
        # 尝试解析日期列
        date_cols = ['date', 'Date', 'dt', 'Dt', 'Year', 'year', 'time', 'Time']
        year_col = None
        for col in date_cols:
            if col.lower() in [c.lower() for c in df.columns]:
                actual_col = [c for c in df.columns if c.lower() == col.lower()][0]
                if col.lower() == 'year':
                    df['year'] = pd.to_numeric(df[actual_col], errors='coerce')
                    year_col = 'year'
                else:
                    try:
                        df[actual_col] = pd.to_datetime(df[actual_col], errors='coerce')
                        df['year'] = df[actual_col].dt.year
                        if 'month' in df[actual_col].dt:
                            df['month'] = df[actual_col].dt.month
                        year_col = 'year'
                    except:
                        pass
                if year_col:
                    break
        
        if year_col is None:
            # 尝试从数值列推断年份
            print("⚠️  未找到年份列，尝试从数据推断...")
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    sample = df[col].dropna().head(100)
                    if len(sample) > 0 and sample.min() >= 1990 and sample.max() <= 2030:
                        df['year'] = df[col]
                        year_col = 'year'
                        print(f"  推断年份列: {col}")
                        break
        
        # 查找海平面列（支持多种命名）
        sea_level_cols = ['sea_level', 'Sea_Level', 'sea_level_mm', 'Sea_Level_mm', 
                         'GMSL', 'gmsl', 'height', 'Height', 'level', 'Level',
                         'sea level', 'Sea Level', 'global_mean_sea_level', 'GMSL_mm']
        sea_level_col = None
        for col in df.columns:
            col_lower = col.lower()
            for sl_pattern in sea_level_cols:
                if sl_pattern.lower() in col_lower:
                    sea_level_col = col
                    break
            if sea_level_col:
                break
        
        if sea_level_col is None:
            print("⚠️  未找到海平面高度列")
            print(f"   可用列: {list(df.columns)}")
            return None
        
        # 确保年份列存在
        if 'year' not in df.columns:
            print("⚠️  无法确定年份列")
            return None
        
        # 清理数据
        df = df.dropna(subset=[sea_level_col, 'year'])
        df['year'] = df['year'].astype(int)
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        if 'year' in df.columns:
            print(f"  时间范围：{df['year'].min()} - {df['year'].max()}")
        print(f"  海平面列：{sea_level_col}")
        
        return df
    
    def load_precipitation_data(self):
        """加载降水量数据
        
        预期文件格式：
        - 列：year, month, precipitation_mm, country/city
        """
        possible_paths = [
            self.data_dir / 'precipitation' / 'precipitation_data.csv',
            self.data_dir / 'precipitation' / 'gpcc_precipitation.csv',
            self.data_dir / 'precipitation_data.csv',
            self.data_dir / 'precipitation.csv'
        ]
        
        file_path = None
        for path in possible_paths:
            if path.exists():
                file_path = path
                break
        
        if file_path is None:
            print("⚠️  降水量数据文件未找到")
            print("   请下载降水量数据到以下位置之一：")
            for path in possible_paths:
                print(f"   - {path}")
            return None
        
        print(f"正在加载降水量数据: {file_path}")
        df = pd.read_csv(file_path)
        
        # 尝试解析日期列
        date_cols = ['date', 'Date', 'dt', 'Dt', 'year_month']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
                df['year'] = df[col].dt.year
                df['month'] = df[col].dt.month
                break
        
        # 查找降水量列
        precip_cols = ['precipitation', 'Precipitation', 'precipitation_mm', 
                       'Precipitation_mm', 'rainfall', 'Rainfall']
        precip_col = None
        for col in precip_cols:
            if col in df.columns:
                precip_col = col
                break
        
        if precip_col is None:
            print("⚠️  未找到降水量列")
            return None
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        print(f"  时间范围：{df['year'].min()} - {df['year'].max()}")
        print(f"  降水量列：{precip_col}")
        return df
    
    def load_glacier_ice_data(self):
        """加载冰川/海冰数据
        
        支持数据集：
        - NOAA G02135 海冰数据: https://noaadata.apps.nsidc.org/NOAA/G02135/
        
        预期文件格式：
        - CSV: 列：year, month, ice_area_km2, region
        - NetCDF: 需要先用 xarray 读取后转换
        """
        possible_paths = [
            self.data_dir / 'sea_ice' / 'sea_ice_data.csv',
            self.data_dir / 'sea_ice' / 'north' / 'sea_ice_north.csv',
            self.data_dir / 'sea_ice' / 'south' / 'sea_ice_south.csv',
            self.data_dir / 'glacier' / 'ice_data.csv',
            self.data_dir / 'glacier' / 'sea_ice_data.csv',
            self.data_dir / 'ice_data.csv',
            self.data_dir / 'glacier.csv'
        ]
        
        # 尝试直接查找CSV文件
        if (self.data_dir / 'sea_ice').exists():
            possible_paths.extend(list((self.data_dir / 'sea_ice').glob('*.csv')))
        
        file_path = None
        for path in possible_paths:
            if path.exists() and path.is_file():
                file_path = path
                break
        
        if file_path is None:
            print("⚠️  海冰数据文件未找到")
            print("   请下载海冰数据到以下位置之一：")
            print("   - climate/data/raw/sea_ice/sea_ice_data.csv")
            print("   - climate/data/raw/sea_ice/north/sea_ice_north.csv")
            print("   - climate/data/raw/sea_ice/south/sea_ice_south.csv")
            print("   数据源: https://noaadata.apps.nsidc.org/NOAA/G02135/")
            print("   下载指南: 查看 climate/DOWNLOAD_SEA_ICE.md")
            return None
        
        print(f"正在加载海冰数据: {file_path}")
        
        # 尝试读取CSV
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"⚠️  读取CSV失败: {e}")
            print("   如果是NetCDF格式，请先转换为CSV")
            return None
        
        print(f"  数据列: {list(df.columns)}")
        
        # 尝试解析日期列
        date_cols = ['date', 'Date', 'dt', 'Dt', 'year_month', 'Year', 'year']
        year_col = None
        for col in date_cols:
            if col.lower() in [c.lower() for c in df.columns]:
                actual_col = [c for c in df.columns if c.lower() == col.lower()][0]
                if col.lower() == 'year':
                    df['year'] = pd.to_numeric(df[actual_col], errors='coerce')
                    year_col = 'year'
                else:
                    try:
                        df[actual_col] = pd.to_datetime(df[actual_col], errors='coerce')
                        df['year'] = df[actual_col].dt.year
                        if 'month' in df[actual_col].dt:
                            df['month'] = df[actual_col].dt.month
                        year_col = 'year'
                    except:
                        pass
                if year_col:
                    break
        
        # 查找海冰面积列
        ice_cols = ['ice_area', 'Ice_Area', 'ice_area_km2', 'Ice_Area_km2',
                   'sea_ice_area', 'Sea_Ice_Area', 'extent', 'Extent',
                   'area', 'Area', 'coverage', 'Coverage']
        ice_col = None
        for col in df.columns:
            col_lower = col.lower()
            for ice_pattern in ice_cols:
                if ice_pattern.lower() in col_lower:
                    ice_col = col
                    break
            if ice_col:
                break
        
        if ice_col is None:
            print("⚠️  未找到海冰面积列")
            print(f"   可用列: {list(df.columns)}")
            # 不返回None，让用户知道有哪些列可用
        
        print(f"✓ 加载完成：{len(df)} 条记录")
        if 'year' in df.columns:
            print(f"  时间范围：{df['year'].min()} - {df['year'].max()}")
        if ice_col:
            print(f"  海冰面积列：{ice_col}")
        
        return df


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

