"""
气候数据处理模块
"""
import pandas as pd
import numpy as np

class ClimateDataProcessor:
    """气候数据处理器"""
    
    def __init__(self):
        pass
    
    def filter_by_year_range(self, df, start_year=1900, end_year=2015):
        """按年份范围过滤数据
        
        Args:
            df: 数据框
            start_year: 起始年份
            end_year: 结束年份
        """
        print(f"过滤年份范围: {start_year}-{end_year}")
        df_filtered = df[(df['year'] >= start_year) & (df['year'] <= end_year)].copy()
        print(f"  原始记录数: {len(df)}")
        print(f"  过滤后记录数: {len(df_filtered)}")
        return df_filtered
    
    def filter_by_uncertainty(self, df, max_uncertainty=2.0):
        """按不确定性过滤数据
        
        Args:
            df: 数据框
            max_uncertainty: 最大不确定性（摄氏度）
        """
        uncertainty_col = None
        for col in df.columns:
            if 'Uncertainty' in col:
                uncertainty_col = col
                break
        
        if uncertainty_col is None:
            print("⚠️  未找到不确定性列，跳过过滤")
            return df
        
        print(f"过滤不确定性 <= {max_uncertainty}°C")
        df_filtered = df[df[uncertainty_col] <= max_uncertainty].copy()
        print(f"  原始记录数: {len(df)}")
        print(f"  过滤后记录数: {len(df_filtered)}")
        return df_filtered
    
    def remove_missing_values(self, df, temp_column='AverageTemperature'):
        """移除缺失值
        
        Args:
            df: 数据框
            temp_column: 温度列名
        """
        print(f"移除 {temp_column} 列的缺失值")
        df_clean = df.dropna(subset=[temp_column]).copy()
        print(f"  原始记录数: {len(df)}")
        print(f"  清洗后记录数: {len(df_clean)}")
        print(f"  移除记录数: {len(df) - len(df_clean)}")
        return df_clean
    
    def aggregate_by_year(self, df, temp_column='AverageTemperature', group_cols=None):
        """按年份聚合数据
        
        Args:
            df: 数据框
            temp_column: 温度列名
            group_cols: 分组列（如 ['Country']）
        """
        if group_cols is None:
            group_cols = []
        
        group_cols_with_year = group_cols + ['year']
        
        print(f"按 {group_cols_with_year} 聚合数据")
        
        agg_dict = {
            temp_column: ['mean', 'std', 'min', 'max', 'count']
        }
        
        df_agg = df.groupby(group_cols_with_year).agg(agg_dict).reset_index()
        
        # 展平多级列名
        df_agg.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                         for col in df_agg.columns.values]
        
        print(f"  聚合后记录数: {len(df_agg)}")
        return df_agg
    
    def calculate_moving_average(self, df, temp_column='AverageTemperature', 
                                 window=12, group_col=None):
        """计算移动平均
        
        Args:
            df: 数据框
            temp_column: 温度列名
            window: 窗口大小（月数）
            group_col: 分组列（如 'Country'）
        """
        print(f"计算 {window}个月移动平均")
        
        df_ma = df.copy()
        
        if group_col:
            df_ma[f'{temp_column}_MA'] = df_ma.groupby(group_col)[temp_column].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
        else:
            df_ma[f'{temp_column}_MA'] = df_ma[temp_column].rolling(
                window=window, min_periods=1
            ).mean()
        
        print(f"  ✓ 已添加 {temp_column}_MA 列")
        return df_ma
    
    def calculate_temperature_change(self, df, temp_column='AverageTemperature', 
                                    group_col=None, baseline_years=(1951, 1980)):
        """计算温度变化（相对于基准期）
        
        Args:
            df: 数据框
            temp_column: 温度列名
            group_col: 分组列
            baseline_years: 基准期（开始年份，结束年份）
        """
        print(f"计算温度变化（基准期: {baseline_years[0]}-{baseline_years[1]}）")
        
        df_change = df.copy()
        
        # 计算基准期平均温度
        baseline_mask = (df_change['year'] >= baseline_years[0]) & \
                       (df_change['year'] <= baseline_years[1])
        
        if group_col:
            baseline_temps = df_change[baseline_mask].groupby(group_col)[temp_column].mean()
            df_change[f'{temp_column}_Change'] = df_change.apply(
                lambda row: row[temp_column] - baseline_temps.get(row[group_col], np.nan),
                axis=1
            )
        else:
            baseline_temp = df_change.loc[baseline_mask, temp_column].mean()
            df_change[f'{temp_column}_Change'] = df_change[temp_column] - baseline_temp
        
        print(f"  ✓ 已添加 {temp_column}_Change 列")
        return df_change
    
    def detect_outliers(self, df, temp_column='AverageTemperature', n_std=3):
        """检测异常值
        
        Args:
            df: 数据框
            temp_column: 温度列名
            n_std: 标准差倍数
        """
        print(f"检测异常值（{n_std} 倍标准差）")
        
        mean = df[temp_column].mean()
        std = df[temp_column].std()
        
        df_outliers = df[
            (df[temp_column] < mean - n_std * std) | 
            (df[temp_column] > mean + n_std * std)
        ].copy()
        
        print(f"  平均温度: {mean:.2f}°C")
        print(f"  标准差: {std:.2f}°C")
        print(f"  异常值数量: {len(df_outliers)} ({len(df_outliers)/len(df)*100:.2f}%)")
        
        return df_outliers
    
    def get_top_countries(self, df, temp_column='AverageTemperature', 
                         top_n=20, metric='change'):
        """获取TOP N国家
        
        Args:
            df: 数据框（需包含 Country 列）
            temp_column: 温度列名
            top_n: 数量
            metric: 指标 ('change', 'mean', 'std')
        """
        print(f"获取TOP {top_n}国家（按{metric}排序）")
        
        if metric == 'change':
            # 计算升温幅度（最近10年 vs 最早10年）
            recent_years = df['year'].max()
            early_years = df['year'].min()
            
            recent_df = df[df['year'] >= recent_years - 10].groupby('Country')[temp_column].mean()
            early_df = df[df['year'] <= early_years + 10].groupby('Country')[temp_column].mean()
            
            change_df = (recent_df - early_df).sort_values(ascending=False)
            top_countries = change_df.head(top_n).index.tolist()
            
        elif metric == 'mean':
            top_countries = df.groupby('Country')[temp_column].mean().sort_values(
                ascending=False
            ).head(top_n).index.tolist()
            
        elif metric == 'std':
            top_countries = df.groupby('Country')[temp_column].std().sort_values(
                ascending=False
            ).head(top_n).index.tolist()
        
        print(f"  ✓ 已选择 {len(top_countries)} 个国家")
        return top_countries
    
    def prepare_for_geospatial(self, df_city, recent_years_only=True, n_years=10):
        """准备地理空间可视化数据
        
        Args:
            df_city: 城市数据框
            recent_years_only: 是否只使用最近数据
            n_years: 最近N年
        """
        print("准备地理空间可视化数据")
        
        df_geo = df_city.copy()
        
        # 只使用最近数据
        if recent_years_only:
            max_year = df_geo['year'].max()
            df_geo = df_geo[df_geo['year'] >= max_year - n_years]
            print(f"  使用最近{n_years}年数据（{max_year-n_years}-{max_year}）")
        
        # 按城市聚合
        df_geo = df_geo.groupby(['City', 'Country', 'Latitude_num', 'Longitude_num']).agg({
            'AverageTemperature': 'mean',
            'AverageTemperatureUncertainty': 'mean'
        }).reset_index()
        
        # 移除缺失坐标
        df_geo = df_geo.dropna(subset=['Latitude_num', 'Longitude_num'])
        
        print(f"  ✓ 准备完成：{len(df_geo)} 个城市")
        return df_geo


if __name__ == '__main__':
    print("数据处理模块测试")
    
    # 创建测试数据
    np.random.seed(42)
    test_df = pd.DataFrame({
        'year': np.repeat(range(2000, 2020), 12),
        'month': list(range(1, 13)) * 20,
        'AverageTemperature': np.random.randn(240) * 5 + 15,
        'AverageTemperatureUncertainty': np.random.rand(240) * 2
    })
    
    processor = ClimateDataProcessor()
    
    # 测试过滤
    df_filtered = processor.filter_by_year_range(test_df, 2010, 2015)
    
    # 测试聚合
    df_agg = processor.aggregate_by_year(df_filtered)
    
    print("\n测试完成")

