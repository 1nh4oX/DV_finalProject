"""
气候数据可视化模块
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# MacBook上的中文字体
MAC_CHINESE_FONTS = ['STHeiti', 'PingFang SC', 'Hiragino Sans GB', 'Arial Unicode MS', 'Songti SC']

# 设置字体
plt.rcParams['font.sans-serif'] = MAC_CHINESE_FONTS + ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['figure.facecolor'] = 'white'

# 设置绘图风格 - 进一步美化
sns.set_style("whitegrid", {
    'grid.color': '.85',
    'grid.linestyle': '--',
    'grid.linewidth': 0.6,
    'grid.alpha': 0.4,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 1.2,
    'axes.edgecolor': '.3',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
})

# 设置颜色方案
VIRIDIS_CMAP = sns.color_palette("viridis", as_cmap=True)
ROCKET_R_CMAP = sns.color_palette("rocket_r", as_cmap=True)
COOLWARM_CMAP = sns.color_palette("coolwarm", as_cmap=True)

print(f"✓ 字体设置: {MAC_CHINESE_FONTS[0]} (MacBook系统字体)")


class ClimateVisualizer:
    """气候数据可视化类"""
    
    def __init__(self, output_dir='../output/figures'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _ensure_font(self):
        """确保中文字体设置"""
        plt.rcParams['font.sans-serif'] = MAC_CHINESE_FONTS + ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_global_temperature_trend(self, df_global):
        """图1: 全球温度趋势线图"""
        print("正在绘制：全球温度趋势线图...")
        self._ensure_font()
        
        # 按年份聚合
        df_yearly = df_global.groupby('year').agg({
            'LandAverageTemperature': 'mean',
            'LandAverageTemperatureUncertainty': 'mean'
        }).reset_index()
        
        # 过滤掉缺失值
        df_yearly = df_yearly.dropna()
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # 绘制主线
        viridis_colors = sns.color_palette("viridis", 2)
        ax.plot(df_yearly['year'], df_yearly['LandAverageTemperature'],
               linewidth=2.5, color=viridis_colors[0], label='陆地平均温度')
        
        # 绘制置信区间
        ax.fill_between(
            df_yearly['year'],
            df_yearly['LandAverageTemperature'] - df_yearly['LandAverageTemperatureUncertainty'],
            df_yearly['LandAverageTemperature'] + df_yearly['LandAverageTemperatureUncertainty'],
            alpha=0.3, color=viridis_colors[0], label='置信区间'
        )
        
        # 添加趋势线（最近100年）
        recent_df = df_yearly[df_yearly['year'] >= df_yearly['year'].max() - 100]
        z = np.polyfit(recent_df['year'], recent_df['LandAverageTemperature'], 1)
        p = np.poly1d(z)
        ax.plot(recent_df['year'], p(recent_df['year']), 
               'r--', linewidth=2, label=f'趋势线 (斜率: {z[0]:.4f}°C/年)')
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('陆地平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title('全球陆地平均温度变化趋势 (1750-2015)', 
                    fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.legend(fontsize=12, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '01_global_temperature_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：01_global_temperature_trend.png")
    
    def plot_country_temperature_comparison(self, df_country, top_n=20):
        """图2: 国家温度对比（TOP20升温最快）"""
        print("正在绘制：国家温度对比图...")
        self._ensure_font()
        
        # 计算升温幅度
        max_year = df_country['year'].max()
        min_year = df_country['year'].min()
        
        recent_temp = df_country[df_country['year'] >= max_year - 10].groupby('Country')['AverageTemperature'].mean()
        early_temp = df_country[df_country['year'] <= min_year + 10].groupby('Country')['AverageTemperature'].mean()
        
        temp_change = (recent_temp - early_temp).dropna().sort_values(ascending=False)
        top_countries = temp_change.head(top_n)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # 子图1：升温幅度条形图
        rocket_colors = sns.color_palette("rocket_r", len(top_countries))
        bars = ax1.barh(range(len(top_countries)), top_countries.values,
                       color=rocket_colors, edgecolor='white', linewidth=0.8)
        ax1.set_yticks(range(len(top_countries)))
        ax1.set_yticklabels(top_countries.index)
        ax1.set_xlabel('温度升高 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title(f'TOP{top_n} 升温最快的国家', fontsize=16, fontweight='bold', color='#1a1a1a')
        ax1.grid(axis='x', alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars, top_countries.values)):
            ax1.text(value + 0.1, bar.get_y() + bar.get_height()/2,
                    f'+{value:.2f}°C', va='center', fontweight='bold')
        
        # 子图2：TOP10国家温度趋势
        top_10_countries = top_countries.head(10).index
        viridis_palette = sns.color_palette("viridis", 10)
        
        for i, country in enumerate(top_10_countries):
            country_data = df_country[df_country['Country'] == country].groupby('year')['AverageTemperature'].mean()
            ax2.plot(country_data.index, country_data.values, 
                    linewidth=2, label=country, color=viridis_palette[i], alpha=0.8)
        
        ax2.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('TOP10国家温度变化趋势', fontsize=16, fontweight='bold', color='#1a1a1a')
        ax2.legend(fontsize=9, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '02_country_temperature_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：02_country_temperature_comparison.png")
    
    def plot_city_temperature_map(self, df_city):
        """图3: 城市温度地理散点图（交互式）"""
        print("正在绘制：城市温度地理散点图...")
        
        # 准备数据（最近10年平均）
        max_year = df_city['year'].max()
        df_recent = df_city[df_city['year'] >= max_year - 10]
        
        df_map = df_recent.groupby(['City', 'Country', 'Latitude_num', 'Longitude_num']).agg({
            'AverageTemperature': 'mean',
            'AverageTemperatureUncertainty': 'mean'
        }).reset_index()
        
        df_map = df_map.dropna(subset=['Latitude_num', 'Longitude_num', 'AverageTemperature'])
        
        # 创建交互式地图
        fig = px.scatter_geo(
            df_map,
            lat='Latitude_num',
            lon='Longitude_num',
            color='AverageTemperature',
            size='AverageTemperatureUncertainty',
            hover_name='City',
            hover_data={
                'Country': True,
                'AverageTemperature': ':.2f',
                'AverageTemperatureUncertainty': ':.2f',
                'Latitude_num': False,
                'Longitude_num': False
            },
            color_continuous_scale='Viridis',
            title=f'全球城市平均温度分布 ({max_year-10}-{max_year})',
            labels={'AverageTemperature': '平均温度 (°C)',
                   'AverageTemperatureUncertainty': '不确定性'}
        )
        
        fig.update_layout(
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                projection_type='natural earth'
            ),
            width=1400,
            height=800,
            font=dict(size=12)
        )
        
        fig.write_html(self.output_dir / '03_city_temperature_map.html')
        print("✓ 已保存：03_city_temperature_map.html")
    
    def plot_seasonal_heatmap(self, df_global):
        """图4: 季节性温度热力图"""
        print("正在绘制：季节性温度热力图...")
        self._ensure_font()
        
        # 准备数据（最近50年）
        max_year = df_global['year'].max()
        df_recent = df_global[df_global['year'] >= max_year - 50]
        
        # 创建月份-年份矩阵
        pivot_data = df_recent.pivot_table(
            values='LandAverageTemperature',
            index='month',
            columns='year',
            aggfunc='mean'
        )
        
        fig, ax = plt.subplots(figsize=(16, 10))
        
        sns.heatmap(pivot_data, cmap=ROCKET_R_CMAP, ax=ax,
                   cbar_kws={'label': '温度 (°C)', 'shrink': 0.8}, 
                   linewidths=0.8, linecolor='white', square=False)
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('月份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title(f'月度温度热力图 ({max_year-50}-{max_year})', 
                    fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.set_yticklabels(['1月', '2月', '3月', '4月', '5月', '6月', 
                           '7月', '8月', '9月', '10月', '11月', '12月'])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '04_seasonal_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：04_seasonal_heatmap.png")
    
    def plot_temperature_distribution(self, df_country):
        """图5: 温度分布箱线图"""
        print("正在绘制：温度分布箱线图...")
        self._ensure_font()
        
        # 选择部分国家
        countries = ['China', 'United States', 'Russia', 'India', 'Brazil', 
                    'Canada', 'Australia', 'Germany', 'France', 'Japan']
        df_selected = df_country[df_country['Country'].isin(countries)]
        
        # 只使用最近50年数据
        max_year = df_selected['year'].max()
        df_selected = df_selected[df_selected['year'] >= max_year - 50]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        viridis_palette = sns.color_palette("viridis", len(countries))
        sns.boxplot(data=df_selected, x='Country', y='AverageTemperature',
                   palette=viridis_palette, ax=ax)
        
        ax.set_xlabel('国家', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title('主要国家温度分布 (最近50年)', 
                    fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '05_temperature_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：05_temperature_distribution.png")
    
    def plot_temperature_change_rate(self, df_global):
        """图6: 温度变化速率分析"""
        print("正在绘制：温度变化速率分析...")
        self._ensure_font()
        
        # 按10年窗口计算温度变化速率
        df_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        df_yearly = df_yearly.dropna()
        
        # 计算每10年的变化速率
        window = 10
        change_rates = []
        years = []
        
        for i in range(window, len(df_yearly)):
            start_temp = df_yearly.iloc[i-window]['LandAverageTemperature']
            end_temp = df_yearly.iloc[i]['LandAverageTemperature']
            start_year = df_yearly.iloc[i-window]['year']
            end_year = df_yearly.iloc[i]['year']
            
            rate = (end_temp - start_temp) / window  # °C/年
            change_rates.append(rate)
            years.append(end_year)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
        
        # 子图1：变化速率时间序列
        viridis_colors = sns.color_palette("viridis", 1)
        ax1.plot(years, change_rates, linewidth=2.5, color=viridis_colors[0], marker='o', markersize=4)
        ax1.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax1.fill_between(years, 0, change_rates, where=np.array(change_rates) > 0, 
                        alpha=0.3, color='red', label='升温期')
        ax1.fill_between(years, 0, change_rates, where=np.array(change_rates) < 0, 
                        alpha=0.3, color='blue', label='降温期')
        
        ax1.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('温度变化速率 (°C/年)', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('全球温度变化速率（10年滑动窗口）', 
                     fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax1.legend(fontsize=12, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 子图2：变化速率分布直方图
        rocket_colors = sns.color_palette("rocket_r", 1)
        ax2.hist(change_rates, bins=30, color=rocket_colors[0], edgecolor='white', 
                linewidth=0.8, alpha=0.8)
        ax2.axvline(np.mean(change_rates), color='red', linestyle='--', linewidth=2,
                   label=f'均值: {np.mean(change_rates):.4f}°C/年')
        ax2.axvline(np.median(change_rates), color='orange', linestyle='--', linewidth=2,
                   label=f'中位数: {np.median(change_rates):.4f}°C/年')
        
        ax2.set_xlabel('温度变化速率 (°C/年)', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('频次', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('温度变化速率分布', fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax2.legend(fontsize=12, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '06_temperature_change_rate.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：06_temperature_change_rate.png")
    
    def plot_latitude_temperature_relationship(self, df_city):
        """图7: 纬度与温度关系分析"""
        print("正在绘制：纬度与温度关系分析...")
        self._ensure_font()
        
        # 准备数据（最近10年）
        max_year = df_city['year'].max()
        df_recent = df_city[df_city['year'] >= max_year - 10]
        
        df_lat = df_recent.groupby(['City', 'Latitude_num']).agg({
            'AverageTemperature': 'mean'
        }).reset_index()
        df_lat = df_lat.dropna()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # 子图1：散点图 + 回归线
        scatter = ax1.scatter(df_lat['Latitude_num'], df_lat['AverageTemperature'],
                            c=df_lat['AverageTemperature'], cmap=ROCKET_R_CMAP,
                            s=50, alpha=0.6, edgecolors='white', linewidth=0.3)
        
        # 添加回归线
        z = np.polyfit(df_lat['Latitude_num'], df_lat['AverageTemperature'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df_lat['Latitude_num'].min(), df_lat['Latitude_num'].max(), 100)
        ax1.plot(x_line, p(x_line), 'r--', linewidth=2.5, 
                label=f'回归线: y = {z[0]:.3f}x + {z[1]:.2f}')
        
        # 计算相关系数
        r = np.corrcoef(df_lat['Latitude_num'], df_lat['AverageTemperature'])[0, 1]
        ax1.text(0.05, 0.95, f'相关系数 R = {r:.3f}', transform=ax1.transAxes,
                fontsize=12, fontweight='bold', verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax1.set_xlabel('纬度', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('纬度与温度关系（全球城市）', 
                     fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax1.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        cbar1 = plt.colorbar(scatter, ax=ax1, shrink=0.8)
        cbar1.set_label('温度 (°C)', fontsize=12, fontweight='bold', color='#333333')
        
        # 子图2：按纬度带分组箱线图
        df_lat['lat_band'] = pd.cut(df_lat['Latitude_num'], 
                                   bins=[-90, -60, -30, 0, 30, 60, 90],
                                   labels=['极地(-90~-60)', '高纬(-60~-30)', '中纬(-30~0)',
                                          '中纬(0~30)', '高纬(30~60)', '极地(60~90)'])
        
        viridis_palette = sns.color_palette("viridis", 6)
        sns.boxplot(data=df_lat, x='lat_band', y='AverageTemperature',
                   palette=viridis_palette, ax=ax2)
        
        ax2.set_xlabel('纬度带', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('不同纬度带温度分布', fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '07_latitude_temperature_relationship.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：07_latitude_temperature_relationship.png")
    
    def plot_extreme_events(self, df_global):
        """图8: 极端温度事件分析"""
        print("正在绘制：极端温度事件分析...")
        self._ensure_font()
        
        # 按年份聚合
        df_yearly = df_global.groupby('year').agg({
            'LandAverageTemperature': 'mean',
            'LandMaxTemperature': 'mean',
            'LandMinTemperature': 'mean'
        }).reset_index()
        df_yearly = df_yearly.dropna()
        
        # 计算异常值（超过2个标准差）
        mean_temp = df_yearly['LandAverageTemperature'].mean()
        std_temp = df_yearly['LandAverageTemperature'].std()
        
        df_yearly['is_extreme_high'] = df_yearly['LandAverageTemperature'] > mean_temp + 2*std_temp
        df_yearly['is_extreme_low'] = df_yearly['LandAverageTemperature'] < mean_temp - 2*std_temp
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # 子图1：时间序列 + 极端事件标注
        viridis_colors = sns.color_palette("viridis", 2)
        ax1.plot(df_yearly['year'], df_yearly['LandAverageTemperature'],
                linewidth=2, color=viridis_colors[0], label='平均温度', alpha=0.8)
        
        # 标注极端高温事件
        extreme_high = df_yearly[df_yearly['is_extreme_high']]
        ax1.scatter(extreme_high['year'], extreme_high['LandAverageTemperature'],
                   s=100, color='red', marker='^', edgecolors='darkred', linewidth=1.5,
                   label='极端高温事件', zorder=5)
        
        # 标注极端低温事件
        extreme_low = df_yearly[df_yearly['is_extreme_low']]
        ax1.scatter(extreme_low['year'], extreme_low['LandAverageTemperature'],
                   s=100, color='blue', marker='v', edgecolors='darkblue', linewidth=1.5,
                   label='极端低温事件', zorder=5)
        
        # 添加阈值线
        ax1.axhline(mean_temp + 2*std_temp, color='red', linestyle='--', 
                   linewidth=1.5, alpha=0.7, label=f'高温阈值 (+2σ)')
        ax1.axhline(mean_temp - 2*std_temp, color='blue', linestyle='--', 
                   linewidth=1.5, alpha=0.7, label=f'低温阈值 (-2σ)')
        ax1.axhline(mean_temp, color='gray', linestyle='-', 
                   linewidth=1, alpha=0.5, label=f'均值 ({mean_temp:.2f}°C)')
        
        ax1.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('极端温度事件识别（±2σ）', 
                     fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax1.legend(fontsize=10, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray', ncol=2)
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 子图2：极端事件频率统计
        # 按50年窗口统计极端事件频率
        window = 50
        periods = []
        high_freqs = []
        low_freqs = []
        
        for start_year in range(int(df_yearly['year'].min()), 
                               int(df_yearly['year'].max()) - window, window):
            period_df = df_yearly[(df_yearly['year'] >= start_year) & 
                                 (df_yearly['year'] < start_year + window)]
            if len(period_df) > 0:
                periods.append(f'{start_year}-{start_year+window}')
                high_freqs.append(period_df['is_extreme_high'].sum())
                low_freqs.append(period_df['is_extreme_low'].sum())
        
        x = np.arange(len(periods))
        width = 0.35
        
        rocket_colors = sns.color_palette("rocket_r", 2)
        bars1 = ax2.bar(x - width/2, high_freqs, width, label='极端高温', 
                       color=rocket_colors[0], edgecolor='white', linewidth=0.8)
        bars2 = ax2.bar(x + width/2, low_freqs, width, label='极端低温', 
                       color=rocket_colors[1], edgecolor='white', linewidth=0.8)
        
        ax2.set_xlabel('时间段', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('极端事件次数', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('极端温度事件频率变化（50年窗口）', 
                     fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax2.set_xticks(x)
        ax2.set_xticklabels(periods, rotation=45, ha='right')
        ax2.legend(fontsize=12, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # 添加数值标签
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '08_extreme_events.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：08_extreme_events.png")
    
    def plot_hemisphere_comparison(self, df_city):
        """图9: 南北半球温度对比"""
        print("正在绘制：南北半球温度对比...")
        self._ensure_font()
        
        # 准备数据
        max_year = df_city['year'].max()
        df_recent = df_city[df_city['year'] >= max_year - 50]
        
        df_hemi = df_recent.copy()
        df_hemi['hemisphere'] = df_hemi['Latitude_num'].apply(
            lambda x: '北半球' if x >= 0 else '南半球'
        )
        
        df_hemi_agg = df_hemi.groupby(['year', 'hemisphere'])['AverageTemperature'].mean().reset_index()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # 子图1：时间序列对比
        viridis_colors = sns.color_palette("viridis", 2)
        for hemi, color in [('北半球', viridis_colors[1]), ('南半球', viridis_colors[0])]:
            hemi_data = df_hemi_agg[df_hemi_agg['hemisphere'] == hemi]
            ax1.plot(hemi_data['year'], hemi_data['AverageTemperature'],
                    linewidth=2.5, label=hemi, color=color, marker='o', markersize=3, alpha=0.8)
        
        ax1.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('南北半球温度变化对比（最近50年）', 
                     fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax1.legend(fontsize=12, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 子图2：温度分布对比
        rocket_colors = sns.color_palette("rocket_r", 2)
        sns.violinplot(data=df_hemi, x='hemisphere', y='AverageTemperature',
                      palette={'北半球': rocket_colors[0], '南半球': rocket_colors[1]},
                      ax=ax2, inner='box')
        
        ax2.set_xlabel('半球', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('南北半球温度分布对比', fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '09_hemisphere_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：09_hemisphere_comparison.png")
    
    def plot_temperature_anomaly(self, df_global):
        """图10: 温度异常分析（相对于基准期）"""
        print("正在绘制：温度异常分析...")
        self._ensure_font()
        
        # 按年份聚合
        df_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        df_yearly = df_yearly.dropna()
        
        # 使用1951-1980作为基准期
        baseline = df_yearly[(df_yearly['year'] >= 1951) & (df_yearly['year'] <= 1980)]
        baseline_mean = baseline['LandAverageTemperature'].mean()
        
        df_yearly['anomaly'] = df_yearly['LandAverageTemperature'] - baseline_mean
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # 绘制异常值
        colors = ['red' if x > 0 else 'blue' for x in df_yearly['anomaly']]
        bars = ax.bar(df_yearly['year'], df_yearly['anomaly'], 
                     color=colors, alpha=0.7, edgecolor='white', linewidth=0.5)
        
        # 添加零线
        ax.axhline(0, color='black', linestyle='-', linewidth=1.5, label='基准线 (1951-1980均值)')
        
        # 添加移动平均线
        window = 10
        df_yearly['anomaly_ma'] = df_yearly['anomaly'].rolling(window=window, center=True).mean()
        ax.plot(df_yearly['year'], df_yearly['anomaly_ma'], 
               'k-', linewidth=3, label=f'{window}年移动平均', zorder=5)
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('温度异常 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title(f'全球温度异常分析（基准期：1951-1980，基准温度：{baseline_mean:.2f}°C）', 
                    fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.legend(fontsize=12, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # 添加统计信息
        recent_anomaly = df_yearly[df_yearly['year'] >= 2000]['anomaly'].mean()
        ax.text(0.02, 0.98, f'2000年后平均异常: +{recent_anomaly:.2f}°C', 
               transform=ax.transAxes, fontsize=12, fontweight='bold',
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '10_temperature_anomaly.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：10_temperature_anomaly.png")
    
    def plot_city_temperature_scatter(self, df_city):
        """图11: 城市温度地理散点图（静态版，使用rocket_r）"""
        print("正在绘制：城市温度地理散点图（静态版）...")
        self._ensure_font()
        
        # 准备数据（最近10年平均）
        max_year = df_city['year'].max()
        df_recent = df_city[df_city['year'] >= max_year - 10]
        
        df_map = df_recent.groupby(['City', 'Country', 'Latitude_num', 'Longitude_num']).agg({
            'AverageTemperature': 'mean',
            'AverageTemperatureUncertainty': 'mean'
        }).reset_index()
        
        df_map = df_map.dropna(subset=['Latitude_num', 'Longitude_num', 'AverageTemperature'])
        
        fig, ax = plt.subplots(figsize=(20, 12))
        
        # 使用散点图，颜色表示温度，大小表示不确定性
        scatter = ax.scatter(df_map['Longitude_num'], df_map['Latitude_num'],
                           c=df_map['AverageTemperature'], s=df_map['AverageTemperatureUncertainty']*50,
                           cmap=ROCKET_R_CMAP, alpha=0.7, edgecolors='white', linewidth=0.3)
        
        ax.set_xlabel('经度', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('纬度', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title(f'全球城市温度分布（{max_year-10}-{max_year}年平均）', 
                    fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label('平均温度 (°C)', fontsize=13, fontweight='bold', color='#333333')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '11_city_temperature_scatter.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：11_city_temperature_scatter.png")
    
    def plot_decade_comparison(self, df_global):
        """图12: 年代对比分析"""
        print("正在绘制：年代对比分析...")
        self._ensure_font()
        
        # 按年份聚合
        df_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        df_yearly = df_yearly.dropna()
        
        # 按年代分组
        df_yearly['decade'] = (df_yearly['year'] // 10) * 10
        df_decade = df_yearly.groupby('decade')['LandAverageTemperature'].agg(['mean', 'std', 'min', 'max']).reset_index()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
        
        # 子图1：年代平均温度
        viridis_colors = sns.color_palette("viridis", len(df_decade))
        bars1 = ax1.bar(df_decade['decade'], df_decade['mean'],
                       color=viridis_colors, edgecolor='white', linewidth=0.8)
        ax1.errorbar(df_decade['decade'], df_decade['mean'], yerr=df_decade['std'],
                     fmt='none', color='black', capsize=5, linewidth=1.5)
        
        ax1.set_xlabel('年代', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_ylabel('平均温度 (°C)', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_title('各年代平均温度对比', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax1.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 添加数值标签
        for bar, mean_val in zip(bars1, df_decade['mean']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{mean_val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # 子图2：温度范围（min-max）
        rocket_colors = sns.color_palette("rocket_r", len(df_decade))
        ax2.fill_between(df_decade['decade'], df_decade['min'], df_decade['max'],
                        alpha=0.3, color=rocket_colors[0], label='温度范围')
        ax2.plot(df_decade['decade'], df_decade['mean'], 'o-', linewidth=2.5,
                color=rocket_colors[0], markersize=8, label='平均温度')
        
        ax2.set_xlabel('年代', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_ylabel('温度 (°C)', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_title('各年代温度范围', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax2.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # 子图3：温度标准差（波动性）
        ax3.plot(df_decade['decade'], df_decade['std'], 'o-', linewidth=2.5,
                color=viridis_colors[0], markersize=8)
        ax3.fill_between(df_decade['decade'], 0, df_decade['std'],
                        alpha=0.3, color=viridis_colors[0])
        
        ax3.set_xlabel('年代', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_ylabel('温度标准差 (°C)', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_title('各年代温度波动性', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax3.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # 子图4：温度变化趋势（相对于第一个年代）
        first_decade_temp = df_decade.iloc[0]['mean']
        df_decade['change_from_first'] = df_decade['mean'] - first_decade_temp
        
        bars4 = ax4.bar(df_decade['decade'], df_decade['change_from_first'],
                       color=rocket_colors, edgecolor='white', linewidth=0.8)
        ax4.axhline(0, color='black', linestyle='--', linewidth=1)
        
        ax4.set_xlabel('年代', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_ylabel('温度变化 (°C)', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_title(f'相对于{int(df_decade.iloc[0]["decade"])}年代的温度变化', 
                     fontsize=15, fontweight='bold', color='#1a1a1a')
        ax4.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        
        # 添加数值标签
        for bar, change in zip(bars4, df_decade['change_from_first']):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{change:+.2f}', ha='center', 
                    va='bottom' if height > 0 else 'top', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '12_decade_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：12_decade_comparison.png")
    
    def generate_all_visualizations(self, df_global=None, df_country=None, df_city=None):
        """生成所有可视化图表"""
        print("=" * 60)
        print("开始生成气候数据可视化...")
        print("=" * 60)
        
        try:
            if df_global is not None:
                self.plot_global_temperature_trend(df_global)
                self.plot_seasonal_heatmap(df_global)
                self.plot_temperature_change_rate(df_global)
                self.plot_extreme_events(df_global)
                self.plot_temperature_anomaly(df_global)
                self.plot_decade_comparison(df_global)
            
            if df_country is not None:
                self.plot_country_temperature_comparison(df_country)
                self.plot_temperature_distribution(df_country)
            
            if df_city is not None:
                self.plot_city_temperature_map(df_city)
                self.plot_city_temperature_scatter(df_city)
                self.plot_latitude_temperature_relationship(df_city)
                self.plot_hemisphere_comparison(df_city)
            
            print("\n" + "=" * 60)
            print("✅ 所有图表生成完成！")
            print(f"📁 输出目录: {self.output_dir}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ 生成图表时出错: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    print("可视化模块已加载")
    print(f"输出目录: ../output/figures/")

