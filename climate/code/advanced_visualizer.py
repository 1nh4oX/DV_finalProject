"""
高级气候数据可视化模块 - 完全符合论文框架要求
使用 crest 配色主题，参考 Seaborn 官方示例库
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from scipy import stats

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
    'grid.color': '.88',
    'grid.linestyle': '-',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.3,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 1.5,
    'axes.edgecolor': '#2b2b2b',
    'figure.facecolor': 'white',
    'axes.facecolor': '#fafafa',
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
})

# 🎨 核心配色方案：magma 和 viridis（高端配色）
MAGMA_CMAP = sns.color_palette("magma", as_cmap=True)
MAGMA_COLORS = sns.color_palette("magma", n_colors=10)
VIRIDIS_CMAP = sns.color_palette("viridis", as_cmap=True)
VIRIDIS_COLORS = sns.color_palette("viridis", n_colors=10)

# 使用渐变色替代纯红色
ACCENT_COLOR = MAGMA_COLORS[7]  # 深紫红色
TREND_COLOR = MAGMA_COLORS[8]   # 亮橙色

print(f"✓ 字体设置: {MAC_CHINESE_FONTS[0]}")
print(f"✓ 配色主题: magma + viridis")


class AdvancedClimateVisualizer:
    """高级气候数据可视化类"""
    
    def __init__(self, output_dir='../output/advanced_figures'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.magma_cmap = MAGMA_CMAP
        self.magma_colors = MAGMA_COLORS
        self.viridis_cmap = VIRIDIS_CMAP
        self.viridis_colors = VIRIDIS_COLORS
        self.accent_color = ACCENT_COLOR
        self.trend_color = TREND_COLOR
        
    def _ensure_font(self):
        """确保中文字体设置"""
        plt.rcParams['font.sans-serif'] = MAC_CHINESE_FONTS + ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def _beautify_ax(self, ax, title):
        """统一美化坐标轴"""
        ax.set_title(title, fontsize=16, fontweight='bold', color='#1a1a1a', pad=20)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.tick_params(axis='both', which='major', labelsize=11, width=1.2, length=6)
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        
    # ============================================================
    # 第一章：全球变暖是否持续？（长期趋势验证）
    # ============================================================
    
    def plot_01_long_term_trend(self, df_global):
        """图1: 全球温度长期趋势（1750-2015）+ 工业革命前后对比"""
        print("\n📊 第一章：全球变暖是否持续？")
        print("正在绘制：图1 - 全球温度长期趋势线图...")
        self._ensure_font()
        
        # 按年份聚合
        df_yearly = df_global.groupby('year').agg({
            'LandAverageTemperature': 'mean',
            'LandAverageTemperatureUncertainty': 'mean'
        }).reset_index().dropna()
        
        fig, ax = plt.subplots(figsize=(18, 8))
        
        # 分段绘制：工业革命前后
        industrial_year = 1850
        pre_industrial = df_yearly[df_yearly['year'] < industrial_year]
        post_industrial = df_yearly[df_yearly['year'] >= industrial_year]
        
        # 工业革命前：淡色（viridis浅色）
        ax.plot(pre_industrial['year'], pre_industrial['LandAverageTemperature'],
               linewidth=2.5, color=self.viridis_colors[2], label='工业革命前 (<1850)', alpha=0.8)
        
        # 工业革命后：深色（magma深色）
        ax.plot(post_industrial['year'], post_industrial['LandAverageTemperature'],
               linewidth=3.5, color=self.magma_colors[7], label='工业革命后 (≥1850)')
        
        # 置信区间（仅工业革命后）
        ax.fill_between(
            post_industrial['year'],
            post_industrial['LandAverageTemperature'] - post_industrial['LandAverageTemperatureUncertainty'],
            post_industrial['LandAverageTemperature'] + post_industrial['LandAverageTemperatureUncertainty'],
            alpha=0.15, color=self.magma_colors[6], label='95% 置信区间'
        )
        
        # 添加关键转折点标注（使用渐变色）
        recent_100 = df_yearly[df_yearly['year'] >= 1950]
        z = np.polyfit(recent_100['year'], recent_100['LandAverageTemperature'], 1)
        p = np.poly1d(z)
        ax.plot(recent_100['year'], p(recent_100['year']), 
               linestyle='--', linewidth=2.5, color=self.trend_color,
               label=f'加速趋势线 (1950后, 斜率: {z[0]:.4f}°C/年)', alpha=0.9)
        
        # 标注重要年份（使用渐变色）
        ax.axvline(1850, color=self.viridis_colors[5], linestyle=':', linewidth=1.8, alpha=0.6)
        ax.text(1850, df_yearly['LandAverageTemperature'].min(), '工业革命', 
               rotation=90, fontsize=10, va='bottom', ha='right', color=self.viridis_colors[5])
        
        ax.axvline(1950, color=self.magma_colors[8], linestyle=':', linewidth=1.8, alpha=0.6)
        ax.text(1950, df_yearly['LandAverageTemperature'].min(), '加速上升起点', 
               rotation=90, fontsize=10, va='bottom', ha='right', color=self.magma_colors[8])
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('全球陆地平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第一章：全球温度长期趋势验证（1750-2015）')
        ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True, fancybox=True, 
                 framealpha=0.95, edgecolor='gray')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '01_long_term_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：01_long_term_trend.png")
        
    # ============================================================
    # 第二章：变暖是否均匀？（国家/地区差异）
    # ============================================================
    
    def plot_02_country_heatmap_6_periods(self, df_country):
        """图2: 国家温度热力图（6个关键年份对比）"""
        print("\n📊 第二章：变暖是否均匀？")
        print("正在绘制：图2 - 国家温度热力图（6个时间点）...")
        self._ensure_font()
        
        # 6个关键年份
        key_years = [1850, 1900, 1950, 1980, 2000, 2010]
        
        # 选取温度变化最显著的前30个国家
        df_2010 = df_country[df_country['year'] == 2010].copy()
        df_1850 = df_country[df_country['year'] == 1850].copy()
        
        df_change = df_2010.merge(df_1850, on='Country', suffixes=('_2010', '_1850'))
        df_change['temp_change'] = (df_change['AverageTemperature_2010'] - 
                                    df_change['AverageTemperature_1850'])
        top_countries = df_change.nlargest(30, 'temp_change')['Country'].tolist()
        
        # 准备热力图数据
        heatmap_data = []
        for country in top_countries:
            temps = []
            for year in key_years:
                df_filtered = df_country[(df_country['Country'] == country) & 
                                        (df_country['year'] == year)]
                if not df_filtered.empty:
                    temps.append(df_filtered['AverageTemperature'].mean())
                else:
                    temps.append(np.nan)
            heatmap_data.append(temps)
        
        heatmap_df = pd.DataFrame(heatmap_data, 
                                 index=top_countries, 
                                 columns=key_years)
        
        # 绘制热力图（使用 magma 配色）
        fig, ax = plt.subplots(figsize=(14, 18))
        sns.heatmap(heatmap_df, cmap=self.magma_cmap, annot=False, fmt='.1f',
                   linewidths=0.8, linecolor='white', cbar_kws={'label': '平均温度 (°C)'},
                   ax=ax, vmin=heatmap_df.min().min(), vmax=heatmap_df.max().max())
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('国家', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title('第二章：国家温度演变热力图（6个关键时期）\n工业化前→加速变暖期', 
                    fontsize=16, fontweight='bold', color='#1a1a1a', pad=20)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '02_country_heatmap_6_periods.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：02_country_heatmap_6_periods.png")
        
    def plot_03_regional_temperature_lines(self, df_country):
        """图3: 分区域温度均值折线图"""
        print("正在绘制：图3 - 分区域温度均值折线图...")
        self._ensure_font()
        
        # 定义区域（简化版，可根据实际数据调整）
        regions = {
            '北极圈': ['Norway', 'Sweden', 'Finland', 'Iceland', 'Greenland', 'Russia', 'Canada'],
            '欧洲': ['United Kingdom', 'Germany', 'France', 'Spain', 'Italy'],
            '亚洲': ['China', 'India', 'Japan', 'South Korea', 'Thailand'],
            '中东': ['Saudi Arabia', 'Iran', 'Iraq', 'United Arab Emirates', 'Turkey'],
            '非洲': ['Egypt', 'South Africa', 'Nigeria', 'Kenya'],
            '美洲': ['United States', 'Brazil', 'Argentina', 'Mexico']
        }
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # 使用 viridis 和 magma 混合配色
        region_colors = self.viridis_colors[:3] + self.magma_colors[5:8]
        
        for i, (region_name, countries) in enumerate(regions.items()):
            df_region = df_country[df_country['Country'].isin(countries)]
            df_region_yearly = df_region.groupby('year')['AverageTemperature'].mean().reset_index()
            
            ax.plot(df_region_yearly['year'], df_region_yearly['AverageTemperature'],
                   linewidth=3, label=region_name, color=region_colors[i % len(region_colors)],
                   alpha=0.9)
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('区域平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第二章：全球区域温度演变对比（不均衡性验证）')
        ax.legend(loc='best', fontsize=11, frameon=True, shadow=True, fancybox=True, 
                 framealpha=0.95, edgecolor='gray', ncol=2)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '03_regional_temperature_lines.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：03_regional_temperature_lines.png")
        
    # ============================================================
    # 第三章：城市层面发生了什么？（微观气候结构）
    # ============================================================
    
    def plot_04_latitude_violin(self, df_city):
        """图4: 按纬度分组的小提琴图（核心图表）"""
        print("\n📊 第三章：城市层面发生了什么？")
        print("正在绘制：图4 - 纬度带温度分布小提琴图...")
        self._ensure_font()
        
        # 过滤最近50年的数据
        df_recent = df_city[df_city['year'] >= df_city['year'].max() - 50].copy()
        
        # 创建纬度带（每10度一个区间）
        def assign_latitude_band(lat):
            if pd.isna(lat):
                return None
            lat_rounded = int(lat // 10) * 10
            if lat >= 0:
                return f"{lat_rounded}°N"
            else:
                return f"{-lat_rounded}°S"
        
        df_recent['latitude_band'] = df_recent['Latitude_num'].apply(assign_latitude_band)
        df_recent = df_recent.dropna(subset=['latitude_band', 'AverageTemperature'])
        
        # 按纬度排序
        def parse_latitude_for_sort(lat_str):
            """解析纬度字符串用于排序"""
            if '°N' in lat_str:
                return float(lat_str.replace('°N', ''))
            elif '°S' in lat_str:
                return -float(lat_str.replace('°S', ''))
            return 0
        
        latitude_order = sorted(df_recent['latitude_band'].unique(), 
                               key=parse_latitude_for_sort, 
                               reverse=True)
        
        fig, ax = plt.subplots(figsize=(18, 10))
        
        # 绘制小提琴图（使用 viridis 渐变）
        violin_colors = self.viridis_cmap(np.linspace(0.2, 0.9, len(latitude_order)))
        sns.violinplot(data=df_recent, x='latitude_band', y='AverageTemperature',
                      order=latitude_order, palette=violin_colors,
                      inner='box', linewidth=1.5, ax=ax)
        
        ax.set_xlabel('纬度带', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第三章：纬度带温度分布形态差异（小提琴图）\n高纬双峰 vs 低纬稳定')
        ax.tick_params(axis='x', rotation=45)
        
        # 添加注释
        ax.text(0.02, 0.98, '高纬度区：双峰结构（冬夏巨大差异）\n低纬度区：窄高分布（全年温差小）', 
               transform=ax.transAxes, fontsize=11, va='top', ha='left',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '04_latitude_violin.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：04_latitude_violin.png")
        
    def plot_05_city_temperature_boxplot(self, df_city):
        """图5: 城市温度箱线图（展示极端值）"""
        print("正在绘制：图5 - 城市温度箱线图...")
        self._ensure_font()
        
        # 选择前20个数据最丰富的城市
        city_counts = df_city.groupby('City').size().nlargest(20)
        top_cities = city_counts.index.tolist()
        
        df_top_cities = df_city[df_city['City'].isin(top_cities)]
        
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # 绘制箱线图（使用 magma 渐变）
        box_colors = self.magma_cmap(np.linspace(0.2, 0.8, 20))
        sns.boxplot(data=df_top_cities, y='City', x='AverageTemperature',
                   palette=box_colors,
                   linewidth=1.5, ax=ax)
        
        ax.set_xlabel('平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('城市', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第三章：主要城市温度分布与极端值（箱线图）')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '05_city_temperature_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：05_city_temperature_boxplot.png")
        
    # ============================================================
    # 第四章：驱动因素在哪里？（CO₂ 的结构性作用）
    # ============================================================
    
    def plot_06_co2_time_series(self, df_co2):
        """图6: CO₂排放时间序列（展示持续上升）"""
        print("\n📊 第四章：驱动因素在哪里？")
        print("正在绘制：图6 - CO₂排放时间序列...")
        self._ensure_font()
        
        if df_co2 is None or df_co2.empty:
            print("⚠ CO₂数据不可用，跳过")
            return
        
        # 按年份聚合全球总排放
        df_yearly = df_co2.groupby('year')['co2_emission'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # 主折线（使用 magma 深色）
        ax.plot(df_yearly['year'], df_yearly['co2_emission'] / 1e6,
               linewidth=3.5, color=self.magma_colors[7], label='全球总排放')
        
        # 平滑趋势（使用渐变色替代红色）
        from scipy.ndimage import uniform_filter1d
        smoothed = uniform_filter1d(df_yearly['co2_emission'] / 1e6, size=5)
        ax.plot(df_yearly['year'], smoothed, linestyle='--', linewidth=2.5, 
               color=self.trend_color, label='5年平滑趋势', alpha=0.8)
        
        # 填充面积（使用 magma 渐变）
        ax.fill_between(df_yearly['year'], 0, df_yearly['co2_emission'] / 1e6,
                       alpha=0.2, color=self.magma_colors[6])
        
        # 标注关键事件（使用渐变色）
        ax.axvline(1990, color=self.viridis_colors[5], linestyle=':', linewidth=1.8, alpha=0.6)
        ax.text(1990, ax.get_ylim()[1] * 0.9, '《京都议定书》前夕', 
               rotation=90, fontsize=9, va='top', ha='right', color=self.viridis_colors[5])
        
        ax.axvline(2000, color=self.magma_colors[8], linestyle=':', linewidth=1.8, alpha=0.6)
        ax.text(2000, ax.get_ylim()[1] * 0.9, '加速上升期', 
               rotation=90, fontsize=9, va='top', ha='right', color=self.magma_colors[8])
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('全球CO₂总排放 (百万吨)', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第四章：全球CO₂排放量持续上升趋势（1960-2019）')
        ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True, fancybox=True, 
                 framealpha=0.95, edgecolor='gray')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '06_co2_time_series.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：06_co2_time_series.png")
        
    def plot_07_co2_vs_temperature_regression(self, df_co2, df_global):
        """图7: CO₂ vs 温度回归图（因果链证据）"""
        print("正在绘制：图7 - CO₂ vs 温度回归分析图...")
        self._ensure_font()
        
        if df_co2 is None or df_co2.empty:
            print("⚠ CO₂数据不可用，跳过")
            return
        
        # 准备数据：按年份聚合
        df_co2_yearly = df_co2.groupby('year')['co2_emission'].sum().reset_index()
        df_temp_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        
        # 合并
        df_merged = df_co2_yearly.merge(df_temp_yearly, on='year')
        df_merged = df_merged.dropna()
        
        # 归一化年份用于颜色映射
        years_norm = (df_merged['year'] - df_merged['year'].min()) / (df_merged['year'].max() - df_merged['year'].min())
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # 散点图（年份渐变色 - 使用 viridis）
        scatter = ax.scatter(df_merged['co2_emission'] / 1e6, df_merged['LandAverageTemperature'],
                           c=df_merged['year'], cmap=self.viridis_cmap, s=120, alpha=0.8,
                           edgecolors='white', linewidth=2)
        
        # 回归线（使用 magma 亮色替代红色）
        z = np.polyfit(df_merged['co2_emission'] / 1e6, df_merged['LandAverageTemperature'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df_merged['co2_emission'].min() / 1e6, 
                            df_merged['co2_emission'].max() / 1e6, 100)
        ax.plot(x_line, p(x_line), linestyle='--', linewidth=3.5, color=self.trend_color,
               label=f'线性回归 (R² = {np.corrcoef(df_merged["co2_emission"], df_merged["LandAverageTemperature"])[0,1]**2:.3f})')
        
        # 颜色条
        cbar = plt.colorbar(scatter, ax=ax, label='年份')
        cbar.ax.tick_params(labelsize=10)
        
        ax.set_xlabel('全球CO₂总排放 (百万吨)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('全球陆地平均温度 (°C)', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第四章：CO₂ vs 温度的因果链证据（散点回归图）\n点的颜色：时间推进（深→浅）')
        ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True, fancybox=True, 
                 framealpha=0.95, edgecolor='gray')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '07_co2_vs_temperature_regression.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：07_co2_vs_temperature_regression.png")
        
    def plot_08_co2_jointplot(self, df_co2):
        """图8: JointPlot - 人均CO₂ vs 总排放（国家行为差异）"""
        print("正在绘制：图8 - JointPlot（人均CO₂ vs 总排放）...")
        self._ensure_font()
        
        if df_co2 is None or df_co2.empty:
            print("⚠ CO₂数据不可用，跳过")
            return
        
        # 使用最近年份的数据
        latest_year = df_co2['year'].max()
        df_latest = df_co2[df_co2['year'] == latest_year].copy()
        
        # 过滤掉缺失值
        df_latest = df_latest.dropna(subset=['co2_per_capita', 'co2_emission'])
        df_latest = df_latest[df_latest['co2_per_capita'] > 0]
        df_latest = df_latest[df_latest['co2_emission'] > 0]
        
        # 创建 JointPlot
        g = sns.jointplot(data=df_latest, x='co2_per_capita', y='co2_emission',
                         kind='scatter', height=10, ratio=4,
                         marginal_kws=dict(bins=30, fill=True),
                         joint_kws=dict(alpha=0.6, edgecolor='white', linewidth=0.5, s=80))
        
        # 设置颜色（使用 magma）
        g.ax_joint.collections[0].set_facecolor(self.magma_colors[6])
        for patch in g.ax_marg_x.patches:
            patch.set_facecolor(self.magma_colors[6])
        for patch in g.ax_marg_y.patches:
            patch.set_facecolor(self.magma_colors[6])
        
        g.ax_joint.set_xlabel('人均CO₂排放 (吨/人)', fontsize=14, fontweight='bold', color='#333333')
        g.ax_joint.set_ylabel('国家总CO₂排放 (吨)', fontsize=14, fontweight='bold', color='#333333')
        g.fig.suptitle(f'第四章：国家排放结构差异（{latest_year}年）\nJointPlot：人均 vs 总量', 
                      fontsize=16, fontweight='bold', color='#1a1a1a', y=1.02)
        
        plt.savefig(self.output_dir / '08_co2_jointplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：08_co2_jointplot.png")
        
    # ============================================================
    # 第五章：后果是否已经显现？（海平面作为结果指标）
    # ============================================================
    
    def plot_09_sea_level_trend(self, df_sea_level):
        """图9: 海平面变化趋势"""
        print("\n📊 第五章：后果是否已经显现？")
        print("正在绘制：图9 - 海平面变化趋势...")
        self._ensure_font()
        
        if df_sea_level is None or df_sea_level.empty:
            print("⚠ 海平面数据不可用，跳过")
            return
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # 主折线（使用 viridis 深色）
        ax.plot(df_sea_level['year'], df_sea_level['sea_level'],
               linewidth=3.5, color=self.viridis_colors[7], label='海平面高度')
        
        # 填充面积（使用 viridis 渐变）
        ax.fill_between(df_sea_level['year'], 0, df_sea_level['sea_level'],
                       alpha=0.2, color=self.viridis_colors[6])
        
        # 趋势线（使用渐变色）
        z = np.polyfit(df_sea_level['year'], df_sea_level['sea_level'], 1)
        p = np.poly1d(z)
        ax.plot(df_sea_level['year'], p(df_sea_level['year']), 
               linestyle='--', linewidth=2.5, color=self.trend_color,
               label=f'线性趋势 (斜率: {z[0]:.2f} mm/年)', alpha=0.9)
        
        ax.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('海平面高度 (mm)', fontsize=14, fontweight='bold', color='#333333')
        self._beautify_ax(ax, '第五章：全球海平面加速上升趋势（卫星观测数据）')
        ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True, fancybox=True, 
                 framealpha=0.95, edgecolor='gray')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '09_sea_level_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：09_sea_level_trend.png")
        
    def plot_10_sea_level_vs_temperature(self, df_sea_level, df_global):
        """图10: 海平面 vs 温度双轴图（滞后同步）"""
        print("正在绘制：图10 - 海平面 vs 温度双轴图...")
        self._ensure_font()
        
        if df_sea_level is None or df_sea_level.empty:
            print("⚠ 海平面数据不可用，跳过")
            return
        
        # 准备温度数据（与海平面时间段对齐）
        df_temp_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        df_temp_aligned = df_temp_yearly[df_temp_yearly['year'].isin(df_sea_level['year'])]
        
        fig, ax1 = plt.subplots(figsize=(16, 8))
        
        # 温度轴（使用 magma）
        color1 = self.magma_colors[6]
        ax1.plot(df_temp_aligned['year'], df_temp_aligned['LandAverageTemperature'],
                linewidth=3.5, color=color1, label='全球温度')
        ax1.set_xlabel('年份', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('全球陆地平均温度 (°C)', fontsize=14, fontweight='bold', color=color1)
        ax1.tick_params(axis='y', labelcolor=color1, labelsize=11)
        
        # 海平面轴（使用 viridis）
        ax2 = ax1.twinx()
        color2 = self.viridis_colors[7]
        ax2.plot(df_sea_level['year'], df_sea_level['sea_level'],
                linewidth=3.5, color=color2, label='海平面高度')
        ax2.set_ylabel('海平面高度 (mm)', fontsize=14, fontweight='bold', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2, labelsize=11)
        
        # 标题
        ax1.set_title('第五章：温度 × 海平面的同步上升关系（双轴图）', 
                     fontsize=16, fontweight='bold', color='#1a1a1a', pad=20)
        
        # 图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11, 
                  frameon=True, shadow=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '10_sea_level_vs_temperature.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：10_sea_level_vs_temperature.png")
        
    # ============================================================
    # 第六章：综合验证（多变量相关性）
    # ============================================================
    
    def plot_11_pairplot(self, df_global, df_co2, df_sea_level):
        """图11: PairPlot - 多变量相关矩阵（全景证据）"""
        print("\n📊 第六章：综合验证")
        print("正在绘制：图11 - PairPlot多变量相关矩阵...")
        self._ensure_font()
        
        # 准备数据：按年份对齐所有变量
        df_temp_yearly = df_global.groupby('year').agg({
            'LandAverageTemperature': 'mean',
            'LandMaxTemperature': 'mean',
            'LandMinTemperature': 'mean'
        }).reset_index()
        
        # 合并数据
        df_combined = df_temp_yearly.copy()
        
        if df_co2 is not None and not df_co2.empty:
            df_co2_yearly = df_co2.groupby('year')['co2_emission'].sum().reset_index()
            df_combined = df_combined.merge(df_co2_yearly, on='year', how='left')
        
        if df_sea_level is not None and not df_sea_level.empty:
            df_combined = df_combined.merge(df_sea_level[['year', 'sea_level']], on='year', how='left')
        
        # 过滤有效数据
        df_combined = df_combined.dropna()
        
        # 创建年代分类
        df_combined['年代'] = pd.cut(df_combined['year'], 
                                    bins=[1960, 1980, 2000, 2020],
                                    labels=['1960-1980', '1980-2000', '2000-2020'])
        
        # 选择关键变量
        plot_vars = ['LandAverageTemperature', 'co2_emission', 'sea_level']
        plot_vars = [v for v in plot_vars if v in df_combined.columns]
        
        if len(plot_vars) < 2:
            print("⚠ 变量不足，跳过 PairPlot")
            return
        
        # 绘制 PairPlot（使用 magma 配色）
        g = sns.pairplot(df_combined[plot_vars + ['年代']], hue='年代',
                        palette=sns.color_palette("magma", n_colors=3),
                        diag_kind='kde', plot_kws={'alpha': 0.7, 's': 60, 'edgecolor': 'white'},
                        height=3.5, aspect=1.2)
        
        g.fig.suptitle('第六章：气候变量相关矩阵（PairPlot）\n排放—升温—海平面的完整链路', 
                      fontsize=16, fontweight='bold', color='#1a1a1a', y=1.01)
        
        plt.savefig(self.output_dir / '11_pairplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：11_pairplot.png")
        
    # ============================================================
    # 主函数：生成所有可视化
    # ============================================================
    
    def generate_all_visualizations(self, df_global, df_country, df_city, 
                                    df_co2=None, df_sea_level=None):
        """生成所有论文框架要求的可视化"""
        print("\n" + "="*80)
        print("🎨 开始生成符合论文框架的高级可视化")
        print(f"📁 输出目录: {self.output_dir}")
        print(f"🎨 配色主题: crest")
        print("="*80)
        
        try:
            # 第一章：全球变暖是否持续？
            self.plot_01_long_term_trend(df_global)
            
            # 第二章：变暖是否均匀？
            self.plot_02_country_heatmap_6_periods(df_country)
            self.plot_03_regional_temperature_lines(df_country)
            
            # 第三章：城市层面发生了什么？
            self.plot_04_latitude_violin(df_city)
            self.plot_05_city_temperature_boxplot(df_city)
            
            # 第四章：驱动因素在哪里？
            if df_co2 is not None and not df_co2.empty:
                self.plot_06_co2_time_series(df_co2)
                self.plot_07_co2_vs_temperature_regression(df_co2, df_global)
                self.plot_08_co2_jointplot(df_co2)
            
            # 第五章：后果是否已经显现？
            if df_sea_level is not None and not df_sea_level.empty:
                self.plot_09_sea_level_trend(df_sea_level)
                self.plot_10_sea_level_vs_temperature(df_sea_level, df_global)
            
            # 第六章：综合验证
            self.plot_11_pairplot(df_global, df_co2, df_sea_level)
            
            print("\n" + "="*80)
            print("✅ 所有可视化生成完成！")
            print(f"📊 共生成11个高级图表")
            print(f"📁 保存位置: {self.output_dir}")
            print("="*80 + "\n")
            
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()

