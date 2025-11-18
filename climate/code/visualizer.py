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

# 设置绘图风格
sns.set_style("whitegrid", {
    'grid.color': '.85',
    'grid.linestyle': '--',
    'grid.linewidth': 0.6,
    'grid.alpha': 0.4,
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
            color_continuous_scale='RdYlBu_r',
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
        
        sns.heatmap(pivot_data, cmap=COOLWARM_CMAP, ax=ax,
                   cbar_kws={'label': '温度 (°C)'}, linewidths=0.5, linecolor='white')
        
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
    
    def generate_all_visualizations(self, df_global=None, df_country=None, df_city=None):
        """生成所有可视化图表"""
        print("=" * 60)
        print("开始生成气候数据可视化...")
        print("=" * 60)
        
        try:
            if df_global is not None:
                self.plot_global_temperature_trend(df_global)
                self.plot_seasonal_heatmap(df_global)
            
            if df_country is not None:
                self.plot_country_temperature_comparison(df_country)
                self.plot_temperature_distribution(df_country)
            
            if df_city is not None:
                self.plot_city_temperature_map(df_city)
            
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

