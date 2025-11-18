"""
深圳交通数据可视化模块
包含10种精美图表的生成函数
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体 - 修复字体显示问题
import matplotlib
import matplotlib.font_manager as fm
import platform
import os

# 查找可用的中文字体 - MacBook专用优化
def find_chinese_font():
    """查找系统中可用的中文字体（MacBook优化）"""
    # MacBook上肯定有的中文字体（按优先级）
    mac_fonts = [
        'PingFang SC',      # macOS 10.11+ 默认中文字体
        'STHeiti',          # 华文黑体，macOS系统字体
        'Hiragino Sans GB', # 冬青黑体简体中文
        'Arial Unicode MS', # 支持中文的Arial
        'Songti SC',        # 宋体简体
        'Kaiti SC',         # 楷体简体
    ]
    
    # 获取所有可用字体名称
    try:
        available_fonts = set([f.name for f in fm.fontManager.ttflist])
        
        # 精确匹配
        for font in mac_fonts:
            if font in available_fonts:
                print(f"✓ 找到字体: {font}")
                return font
        
        # 模糊匹配（包含关键词）
        for font_name in available_fonts:
            if 'PingFang' in font_name and 'SC' in font_name:
                print(f"✓ 找到字体: {font_name}")
                return font_name
            if 'STHeiti' in font_name:
                print(f"✓ 找到字体: {font_name}")
                return font_name
            if 'Hiragino' in font_name and 'GB' in font_name:
                print(f"✓ 找到字体: {font_name}")
                return font_name
        
        # 如果都没找到，返回第一个包含中文关键词的
        for font_name in available_fonts:
            if any(kw in font_name for kw in ['PingFang', 'STHeiti', 'Hiragino']):
                print(f"✓ 找到字体: {font_name}")
                return font_name
                
    except Exception as e:
        print(f"⚠️  字体查找异常: {e}")
    
    # 最终回退
    print("⚠️  使用默认字体: PingFang SC")
    return 'PingFang SC'

# 设置字体
chinese_font = find_chinese_font()

# 强制设置matplotlib参数 - MacBook优化
plt.rcParams['font.sans-serif'] = [
    chinese_font,
    'PingFang SC',          # macOS默认
    'STHeiti',              # 华文黑体
    'Hiragino Sans GB',     # 冬青黑体
    'Arial Unicode MS',    # Unicode字体
    'Songti SC',            # 宋体
    'SimHei',               # 黑体（兼容）
    'DejaVu Sans'           # 最终回退
]
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'

# MacBook上肯定有的中文字体（按优先级）
MAC_CHINESE_FONTS = ['STHeiti', 'PingFang SC', 'Hiragino Sans GB', 'Arial Unicode MS', 'Songti SC', 'Kaiti SC']

# 直接设置字体 - 使用MacBook系统字体
plt.rcParams['font.sans-serif'] = MAC_CHINESE_FONTS + ['DejaVu Sans']

# 清除matplotlib字体缓存（确保重新加载）
try:
    import matplotlib.font_manager
    # 不重建整个缓存，只更新当前设置
    pass
except:
    pass

print(f"✓ 字体设置: {MAC_CHINESE_FONTS[0]} (MacBook系统字体)")

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


class TrafficVisualizer:
    """交通数据可视化类"""
    
    def __init__(self, data_dir='../trafficData/sample', output_dir='../outputs/figures'):
        self.data_dir = data_dir
        self.output_dir = output_dir
        
        # 深圳市中心坐标
        self.shenzhen_center = [22.5431, 114.0579]
        
        # 创建输出目录
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def _ensure_chinese_font(self):
        """确保中文字体设置生效（在每个绘图函数开始时调用）"""
        # 强制重新设置字体
        plt.rcParams['font.sans-serif'] = MAC_CHINESE_FONTS + ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def load_data(self, filename):
        """加载数据"""
        import os
        filepath = os.path.join(self.data_dir, filename)
        return pd.read_csv(filepath)
    
    def plot_1_peak_hours_line(self):
        """图1: 高峰时段折线图"""
        print("正在绘制：高峰时段折线图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('hourly_traffic.csv')
        
        # 按工作日/周末分组计算平均值
        df_grouped = df.groupby(['hour', 'is_weekend']).agg({
            'traffic_volume': 'mean',
            'avg_speed': 'mean'
        }).reset_index()
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # 子图1：交通流量 - 使用viridis颜色方案
        viridis_colors = sns.color_palette("viridis", 2)
        for is_weekend, label, color in [(False, '工作日', viridis_colors[1]), (True, '周末', viridis_colors[0])]:
            data = df_grouped[df_grouped['is_weekend'] == is_weekend]
            ax1.plot(data['hour'], data['traffic_volume'], 
                    marker='o', linewidth=2.5, markersize=8,
                    label=label, color=color, alpha=0.8)
        
        ax1.set_xlabel('时间（小时）', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('交通流量（车辆数）', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('深圳市24小时交通流量变化', fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax1.legend(fontsize=12, frameon=True, shadow=True, fancybox=True, framealpha=0.95, 
                  edgecolor='gray', facecolor='white')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.set_xticks(range(0, 24, 2))
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_linewidth(1.5)
        ax1.spines['bottom'].set_linewidth(1.5)
        
        # 标注早晚高峰
        ax1.axvspan(7, 9, alpha=0.2, color='red', label='早高峰')
        ax1.axvspan(17, 19, alpha=0.2, color='orange', label='晚高峰')
        
        # 子图2：平均速度 - 使用viridis颜色方案
        viridis_colors = sns.color_palette("viridis", 2)
        for is_weekend, label, color in [(False, '工作日', viridis_colors[1]), (True, '周末', viridis_colors[0])]:
            data = df_grouped[df_grouped['is_weekend'] == is_weekend]
            ax2.plot(data['hour'], data['avg_speed'],
                    marker='s', linewidth=2.5, markersize=8,
                    label=label, color=color, alpha=0.8)
        
        ax2.set_xlabel('时间（小时）', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('平均速度（km/h）', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('深圳市24小时道路平均速度', fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax2.legend(fontsize=12, frameon=True, shadow=True, fancybox=True, framealpha=0.95,
                  edgecolor='gray', facecolor='white')
        ax2.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.set_xticks(range(0, 24, 2))
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_linewidth(1.5)
        ax2.spines['bottom'].set_linewidth(1.5)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/01_peak_hours_line.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：01_peak_hours_line.png")
    
    def plot_2_congestion_heatmap(self):
        """图2: 路段拥堵热力图"""
        print("正在绘制：路段拥堵热力图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('road_congestion.csv')
        
        # 筛选晚高峰数据
        df_evening = df[df['time_period'] == 'evening_peak']
        
        # 创建深圳地图
        m = folium.Map(
            location=self.shenzhen_center,
            zoom_start=11,
            tiles='OpenStreetMap'
        )
        
        # 准备热力图数据
        heat_data = [[row['latitude'], row['longitude'], row['congestion_index']] 
                     for idx, row in df_evening.iterrows()]
        
        # 添加热力图层
        HeatMap(
            heat_data,
            min_opacity=0.3,
            max_opacity=0.9,
            radius=15,
            blur=20,
            gradient={0.0: 'green', 0.5: 'yellow', 0.7: 'orange', 1.0: 'red'}
        ).add_to(m)
        
        # 保存地图
        m.save(f'{self.output_dir}/02_congestion_heatmap.html')
        
        # 额外创建一个matplotlib版本的热力图
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # 创建网格
        x = df_evening['longitude'].values
        y = df_evening['latitude'].values
        z = df_evening['congestion_index'].values
        
        scatter = ax.scatter(x, y, c=z, s=100, cmap=ROCKET_R_CMAP, 
                           alpha=0.7, edgecolors='white', linewidth=0.3)
        
        ax.set_xlabel('经度', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('纬度', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title('深圳市晚高峰路段拥堵热力图', fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
        cbar.set_label('拥堵指数', fontsize=13, fontweight='bold', color='#333333')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/02_congestion_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：02_congestion_heatmap.html 和 .png")
    
    def plot_3_metro_boxplot(self):
        """图3: 地铁客流箱线图"""
        print("正在绘制：地铁客流箱线图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('metro_ridership.csv')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # 子图1：各线路日客流箱线图 - 使用viridis颜色方案
        viridis_palette = sns.color_palette("viridis", len(df['line'].unique()))
        sns.boxplot(data=df, y='line', x='daily_ridership', 
                   palette=viridis_palette, ax=ax1, orient='h')
        ax1.set_xlabel('日均客流量（人次）', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('地铁线路', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('深圳地铁各线路日客流分布', fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax1.grid(axis='x', alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 子图2：工作日vs周末对比
        df_comparison = df.copy()
        df_comparison['day_type'] = df_comparison['is_weekend'].map({True: '周末', False: '工作日'})
        
        viridis_colors = sns.color_palette("viridis", 2)
        sns.violinplot(data=df_comparison, x='day_type', y='daily_ridership',
                      palette={'工作日': viridis_colors[1], '周末': viridis_colors[0]},
                      ax=ax2, inner='box')
        ax2.set_xlabel('日期类型', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('日均客流量（人次）', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_title('工作日vs周末地铁客流对比', fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/03_metro_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：03_metro_boxplot.png")
    
    def plot_4_od_flow(self):
        """图4: 城市OD路径流向图（桑基图）"""
        print("正在绘制：OD路径流向图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('od_flow.csv')
        
        # 聚合数据
        df_agg = df.groupby(['origin', 'destination'])['flow_volume'].sum().reset_index()
        df_agg = df_agg.nlargest(30, 'flow_volume')  # 取前30个主要流向
        
        # 创建桑基图
        all_nodes = list(set(df_agg['origin'].unique()) | set(df_agg['destination'].unique()))
        node_dict = {node: idx for idx, node in enumerate(all_nodes)}
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                       '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739']
            ),
            link=dict(
                source=[node_dict[origin] for origin in df_agg['origin']],
                target=[node_dict[dest] for dest in df_agg['destination']],
                value=df_agg['flow_volume'].tolist(),
                color='rgba(0,0,96,0.2)'
            )
        )])
        
        fig.update_layout(
            title={
                'text': '深圳市主要区域间出行流向（OD分析）',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial'}
            },
            font=dict(size=12, family='Arial'),
            height=600,
            width=1200
        )
        
        fig.write_html(f'{self.output_dir}/04_od_flow_sankey.html')
        
        # 创建和弦图的matplotlib替代版本
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 创建OD矩阵
        districts = df['origin'].unique()
        matrix = pd.crosstab(df['origin'], df['destination'], 
                            values=df['flow_volume'], aggfunc='sum', 
                            dropna=False).fillna(0)
        
        sns.heatmap(matrix, annot=False, fmt='g', cmap=ROCKET_R_CMAP,
                   ax=ax, cbar_kws={'label': '出行量', 'shrink': 0.8}, 
                   linewidths=0.8, linecolor='white', square=False)
        ax.set_title('深圳市区域间出行流量矩阵', fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.set_xlabel('目的地', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('出发地', fontsize=14, fontweight='bold', color='#333333')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/04_od_flow_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：04_od_flow_sankey.html 和 04_od_flow_matrix.png")
    
    def plot_5_top_congested_roads(self):
        """图5: TOP10拥堵道路条形图"""
        print("正在绘制：TOP10拥堵道路条形图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('top_congested_roads.csv')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # 子图1：拥堵指数条形图 - 使用rocket_r颜色方案
        rocket_colors = sns.color_palette("rocket_r", len(df))
        bars1 = ax1.barh(df['road_name'], df['avg_congestion_index'], 
                        color=rocket_colors, edgecolor='white', linewidth=0.8)
        
        ax1.set_xlabel('平均拥堵指数', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_ylabel('道路名称', fontsize=14, fontweight='bold', color='#333333')
        ax1.set_title('深圳市TOP10最拥堵道路', fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax1.grid(axis='x', alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars1, df['avg_congestion_index'])):
            ax1.text(value + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{value:.2f}', va='center', fontweight='bold')
        
        # 子图2：平均延误时间 - 使用rocket_r颜色方案
        rocket_colors = sns.color_palette("rocket_r", len(df))
        bars2 = ax2.barh(df['road_name'], df['avg_delay_minutes'],
                        color=rocket_colors, edgecolor='white', linewidth=0.8)
        
        ax2.set_xlabel('平均延误时间（分钟）', fontsize=14, fontweight='bold', color='#333333')
        ax2.set_ylabel('')
        ax2.set_title('TOP10道路平均延误时间', fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
        ax2.grid(axis='x', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars2, df['avg_delay_minutes'])):
            ax2.text(value + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{value:.1f}分钟', va='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/05_top_congested_roads.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：05_top_congested_roads.png")
    
    def plot_6_travel_mode_pie(self):
        """图6: 出行方式占比饼图"""
        print("正在绘制：出行方式占比饼图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('travel_mode_share.csv')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # 子图1：饼图 - 使用viridis颜色方案
        viridis_colors = sns.color_palette("viridis", len(df))
        colors = viridis_colors
        explode = [0.05 if x == df['percentage'].max() else 0 for x in df['percentage']]
        
        wedges, texts, autotexts = ax1.pie(
            df['percentage'],
            labels=df['travel_mode'],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        ax1.set_title('深圳市居民出行方式占比', fontsize=16, fontweight='bold', pad=25, color='#1a1a1a')
        
        # 子图2：环形图 - 使用viridis颜色方案
        wedges, texts, autotexts = ax2.pie(
            df['percentage'],
            labels=df['travel_mode'],
            autopct='%1.1f%%',
            startangle=90,
            colors=viridis_colors,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=1.5),
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        ax2.set_title('出行方式分布（环形图）', fontsize=16, fontweight='bold', pad=25, color='#1a1a1a')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/06_travel_mode_pie.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 创建plotly交互式版本
        fig = px.sunburst(
            df,
            names='travel_mode',
            values='percentage',
            title='深圳市出行方式占比（交互式）',
            color='percentage',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(
            font=dict(size=14, family='Arial'),
            height=600,
            width=800
        )
        fig.write_html(f'{self.output_dir}/06_travel_mode_interactive.html')
        print("✓ 已保存：06_travel_mode_pie.png 和 06_travel_mode_interactive.html")
    
    def plot_7_weather_vs_congestion(self):
        """图7: 天气vs拥堵散点回归图"""
        print("正在绘制：天气vs拥堵散点回归图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('weather_traffic.csv')
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 子图1：降雨量vs拥堵指数
        weather_colors = {'晴天': '#FFD700', '多云': '#B0C4DE', 
                         '小雨': '#87CEEB', '中雨': '#4682B4', '大雨': '#191970'}
        
        for weather in df['weather'].unique():
            data = df[df['weather'] == weather]
            ax1.scatter(data['rainfall_mm'], data['congestion_index'],
                       label=weather, alpha=0.6, s=80,
                       color=weather_colors.get(weather, 'gray'),
                       edgecolors='black', linewidth=0.5)
        
        # 添加回归线
        x = df['rainfall_mm'].values
        y = df['congestion_index'].values
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        x_line = np.linspace(x.min(), x.max(), 100)
        ax1.plot(x_line, p(x_line), "r--", linewidth=2, label='回归曲线')
        
        ax1.set_xlabel('降雨量（mm）', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_ylabel('拥堵指数', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_title('降雨量与拥堵指数关系', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax1.legend(fontsize=10, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 子图2：温度vs平均速度 - 使用rocket_r颜色方案
        scatter = ax2.scatter(df['temperature'], df['avg_speed'],
                            c=df['congestion_index'], cmap=ROCKET_R_CMAP,
                            s=80, alpha=0.7, edgecolors='white', linewidth=0.3)
        
        # 回归线
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            df['temperature'], df['avg_speed'])
        line = slope * df['temperature'] + intercept
        ax2.plot(df['temperature'], line, 'r--', linewidth=2, 
                label=f'R² = {r_value**2:.3f}')
        
        ax2.set_xlabel('温度（℃）', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_ylabel('平均速度（km/h）', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_title('温度与道路速度关系', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax2.legend(fontsize=10, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        cbar2 = plt.colorbar(scatter, ax=ax2, shrink=0.8)
        cbar2.set_label('拥堵指数', fontsize=12, fontweight='bold', color='#333333')
        
        # 子图3：不同天气类型的拥堵分布 - 使用viridis颜色方案
        df_sorted = df.sort_values('weather')
        viridis_palette = sns.color_palette("viridis", len(df_sorted['weather'].unique()))
        sns.violinplot(data=df_sorted, x='weather', y='congestion_index',
                      palette=viridis_palette, ax=ax3)
        ax3.set_xlabel('天气类型', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_ylabel('拥堵指数', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_title('不同天气条件下的拥堵分布', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax3.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # 子图4：事故数量vs拥堵 - 使用viridis颜色方案
        ax4.scatter(df['accident_count'], df['congestion_index'],
                   c=df['rainfall_mm'], cmap=VIRIDIS_CMAP,
                   s=80, alpha=0.7, edgecolors='white', linewidth=0.3)
        
        slope, intercept, r_value, _, _ = stats.linregress(
            df['accident_count'], df['congestion_index'])
        line = slope * df['accident_count'] + intercept
        ax4.plot(df['accident_count'], line, 'r--', linewidth=2,
                label=f'R² = {r_value**2:.3f}')
        
        ax4.set_xlabel('事故数量', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_ylabel('拥堵指数', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_title('交通事故与拥堵关系', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax4.legend(fontsize=10, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax4.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/07_weather_vs_congestion.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：07_weather_vs_congestion.png")
    
    def plot_8_weekday_vs_weekend(self):
        """图8: 工作日vs周末对比图"""
        print("正在绘制：工作日vs周末对比图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df_traffic = self.load_data('hourly_traffic.csv')
        df_trips = self.load_data('daily_trips.csv')
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 子图1：24小时流量对比
        ax1 = fig.add_subplot(gs[0, :])
        df_avg = df_traffic.groupby(['hour', 'is_weekend'])['traffic_volume'].mean().reset_index()
        
        viridis_colors = sns.color_palette("viridis", 2)
        for is_weekend, label, color in [(False, '工作日', viridis_colors[1]), (True, '周末', viridis_colors[0])]:
            data = df_avg[df_avg['is_weekend'] == is_weekend]
            ax1.fill_between(data['hour'], data['traffic_volume'], 
                           alpha=0.3, color=color)
            ax1.plot(data['hour'], data['traffic_volume'],
                    marker='o', linewidth=2.5, label=label, color=color)
        
        ax1.set_xlabel('时间（小时）', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_ylabel('交通流量', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_title('工作日vs周末：24小时交通流量对比', fontsize=16, fontweight='bold', color='#1a1a1a')
        ax1.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.set_xticks(range(0, 24, 2))
        
        # 子图2：总出行次数对比
        ax2 = fig.add_subplot(gs[1, 0])
        trip_comparison = df_trips.groupby('day_type')['total_trips'].agg(['mean', 'std']).reset_index()
        
        viridis_colors = sns.color_palette("viridis", 2)
        bars = ax2.bar(trip_comparison['day_type'], trip_comparison['mean'],
                      color=[viridis_colors[1], viridis_colors[0]], edgecolor='white', linewidth=1.0,
                      alpha=0.8)
        ax2.errorbar(trip_comparison['day_type'], trip_comparison['mean'],
                    yerr=trip_comparison['std'], fmt='none', 
                    color='black', capsize=10, linewidth=2)
        
        ax2.set_ylabel('日均出行次数', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_title('工作日vs周末：日均出行量对比', fontsize=14, fontweight='bold', color='#1a1a1a')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height/1e6:.1f}M', ha='center', va='bottom',
                    fontweight='bold', fontsize=11)
        
        # 子图3：人均出行次数
        ax3 = fig.add_subplot(gs[1, 1])
        viridis_colors = sns.color_palette("viridis", 2)
        sns.boxplot(data=df_trips, x='day_type', y='trips_per_capita',
                   palette={'工作日': viridis_colors[1], '周末': viridis_colors[0]}, ax=ax3)
        ax3.set_ylabel('人均出行次数', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_xlabel('')
        ax3.set_title('工作日vs周末：人均出行次数分布', fontsize=14, fontweight='bold', color='#1a1a1a')
        ax3.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # 子图4：速度对比
        ax4 = fig.add_subplot(gs[2, 0])
        speed_comparison = df_traffic.groupby(['hour', 'is_weekend'])['avg_speed'].mean().reset_index()
        
        viridis_colors = sns.color_palette("viridis", 2)
        for is_weekend, label, color in [(False, '工作日', viridis_colors[1]), (True, '周末', viridis_colors[0])]:
            data = speed_comparison[speed_comparison['is_weekend'] == is_weekend]
            ax4.plot(data['hour'], data['avg_speed'],
                    marker='s', linewidth=2.5, label=label, color=color)
        
        ax4.set_xlabel('时间（小时）', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_ylabel('平均速度（km/h）', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_title('工作日vs周末：道路平均速度对比', fontsize=14, fontweight='bold', color='#1a1a1a')
        ax4.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax4.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.set_xticks(range(0, 24, 2))
        
        # 子图5：高峰时段对比（雷达图）
        ax5 = fig.add_subplot(gs[2, 1], projection='polar')
        
        hours_peak = [7, 8, 9, 17, 18, 19]
        weekday_vals = [df_traffic[(df_traffic['hour'] == h) & (df_traffic['is_weekend'] == False)]['traffic_volume'].mean() 
                       for h in hours_peak]
        weekend_vals = [df_traffic[(df_traffic['hour'] == h) & (df_traffic['is_weekend'] == True)]['traffic_volume'].mean()
                       for h in hours_peak]
        
        angles = np.linspace(0, 2 * np.pi, len(hours_peak), endpoint=False).tolist()
        weekday_vals += weekday_vals[:1]
        weekend_vals += weekend_vals[:1]
        angles += angles[:1]
        
        viridis_colors = sns.color_palette("viridis", 2)
        ax5.plot(angles, weekday_vals, 'o-', linewidth=2, label='工作日', color=viridis_colors[1])
        ax5.fill(angles, weekday_vals, alpha=0.25, color=viridis_colors[1])
        ax5.plot(angles, weekend_vals, 'o-', linewidth=2, label='周末', color=viridis_colors[0])
        ax5.fill(angles, weekend_vals, alpha=0.25, color=viridis_colors[0])
        
        ax5.set_xticks(angles[:-1])
        ax5.set_xticklabels([f'{h}:00' for h in hours_peak])
        ax5.set_title('高峰时段流量对比（雷达图）', fontsize=14, fontweight='bold', pad=25, color='#1a1a1a')
        ax5.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax5.grid(True)
        
        plt.suptitle('深圳市工作日与周末交通特征全面对比', 
                    fontsize=19, fontweight='bold', y=0.995, color='#1a1a1a')
        
        plt.savefig(f'{self.output_dir}/08_weekday_vs_weekend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：08_weekday_vs_weekend.png")
    
    def plot_9_daily_trips_histogram(self):
        """图9: 日均出行次数直方图"""
        print("正在绘制：日均出行次数直方图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('daily_trips.csv')
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 子图1：总体分布直方图 - 使用viridis颜色方案
        viridis_colors = sns.color_palette("viridis", 1)
        ax1.hist(df['total_trips'] / 1e6, bins=30, 
                color=viridis_colors[0], edgecolor='white', linewidth=0.8, alpha=0.8)
        ax1.axvline(df['total_trips'].mean() / 1e6, color='red', 
                   linestyle='--', linewidth=2, label=f'均值: {df["total_trips"].mean()/1e6:.2f}M')
        ax1.axvline(df['total_trips'].median() / 1e6, color='orange',
                   linestyle='--', linewidth=2, label=f'中位数: {df["total_trips"].median()/1e6:.2f}M')
        
        ax1.set_xlabel('日均出行次数（百万）', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_ylabel('频次', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_title('深圳市日均出行次数分布', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax1.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # 子图2：工作日vs周末对比直方图 - 使用viridis颜色方案
        weekday_data = df[df['day_type'] == '工作日']['total_trips'] / 1e6
        weekend_data = df[df['day_type'] == '周末']['total_trips'] / 1e6
        
        viridis_colors = sns.color_palette("viridis", 2)
        ax2.hist([weekday_data, weekend_data], bins=20, 
                label=['工作日', '周末'],
                color=[viridis_colors[1], viridis_colors[0]], 
                edgecolor='white', linewidth=0.8, alpha=0.7)
        
        ax2.set_xlabel('日均出行次数（百万）', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_ylabel('频次', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_title('工作日vs周末出行次数分布对比', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax2.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # 子图3：累积分布
        sorted_trips = np.sort(df['total_trips'] / 1e6)
        cumulative = np.arange(1, len(sorted_trips) + 1) / len(sorted_trips)
        
        viridis_colors = sns.color_palette("viridis", 1)
        ax3.plot(sorted_trips, cumulative, linewidth=2.5, color=viridis_colors[0])
        ax3.fill_between(sorted_trips, cumulative, alpha=0.3, color=viridis_colors[0])
        ax3.axhline(0.5, color='red', linestyle='--', linewidth=2, label='50%分位数')
        ax3.axhline(0.9, color='orange', linestyle='--', linewidth=2, label='90%分位数')
        ax3.set_xlabel('日均出行次数（百万）', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_ylabel('累积概率', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_title('日均出行次数累积分布函数', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax3.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax3.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # 子图4：人均出行次数分布 - 使用viridis颜色方案
        viridis_colors = sns.color_palette("viridis", 1)
        ax4.hist(df['trips_per_capita'], bins=30,
                color=viridis_colors[0], edgecolor='white', linewidth=0.8, alpha=0.8)
        
        mean_val = df['trips_per_capita'].mean()
        ax4.axvline(mean_val, color='red', linestyle='--', linewidth=2,
                   label=f'均值: {mean_val:.2f}次/人')
        
        ax4.set_xlabel('人均出行次数', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_ylabel('频次', fontsize=13, fontweight='bold', color='#333333')
        ax4.set_title('深圳市人均日出行次数分布', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax4.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax4.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/09_daily_trips_histogram.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：09_daily_trips_histogram.png")
    
    def plot_10_speed_kde(self):
        """图10: 速度分布核密度图"""
        print("正在绘制：速度分布核密度图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('speed_distribution.csv')
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 子图1：不同道路类型的速度分布 - 使用viridis颜色方案
        viridis_palette = sns.color_palette("viridis", len(df['road_type'].unique()))
        road_types = df['road_type'].unique()
        for i, road_type in enumerate(road_types):
            data = df[df['road_type'] == road_type]['speed_kmh']
            data.plot.kde(ax=ax1, linewidth=2.5, label=road_type, color=viridis_palette[i])
        
        ax1.set_xlabel('速度（km/h）', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_ylabel('概率密度', fontsize=13, fontweight='bold', color='#333333')
        ax1.set_title('不同道路类型的速度分布（核密度估计）', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax1.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax1.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.set_xlim(0, 130)
        
        # 子图2：不同时段的速度分布 - 使用viridis颜色方案
        viridis_palette = sns.color_palette("viridis", len(df['time_period'].unique()))
        time_periods = df['time_period'].unique()
        for i, time_period in enumerate(time_periods):
            data = df[df['time_period'] == time_period]['speed_kmh']
            data.plot.kde(ax=ax2, linewidth=2.5, label=time_period,
                         color=viridis_palette[i])
        
        ax2.set_xlabel('速度（km/h）', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_ylabel('概率密度', fontsize=13, fontweight='bold', color='#333333')
        ax2.set_title('不同时段的速度分布', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax2.legend(fontsize=11, frameon=True, fancybox=True, framealpha=0.95, edgecolor='gray')
        ax2.grid(True, alpha=0.35, linestyle='--', linewidth=0.8)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.set_xlim(0, 130)
        
        # 子图3：小提琴图 - 使用viridis颜色方案
        viridis_palette = sns.color_palette("viridis", len(df['road_type'].unique()))
        sns.violinplot(data=df, x='road_type', y='speed_kmh',
                      palette=viridis_palette, ax=ax3, inner='box')
        ax3.set_xlabel('道路类型', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_ylabel('速度（km/h）', fontsize=13, fontweight='bold', color='#333333')
        ax3.set_title('各类道路速度分布（小提琴图）', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax3.grid(axis='y', alpha=0.35, linestyle='--', linewidth=0.8)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # 子图4：2D核密度图
        road_type_map = {'高速公路': 3, '主干道': 2, '支路': 1}
        df_plot = df.copy()
        df_plot['road_type_num'] = df_plot['road_type'].map(road_type_map)
        
        from scipy.stats import gaussian_kde
        x = df_plot['speed_kmh'].values
        y = df_plot['road_type_num'].values
        
        # 创建网格
        xx, yy = np.mgrid[0:130:100j, 0.5:3.5:100j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([x, y])
        kernel = gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)
        
        contour = ax4.contourf(xx, yy, f, levels=20, cmap=ROCKET_R_CMAP, alpha=0.85)
        ax4.scatter(x, y, c='black', s=1, alpha=0.1)
        
        ax4.set_xlabel('速度（km/h）', fontsize=12, fontweight='bold')
        ax4.set_ylabel('道路类型', fontsize=12, fontweight='bold')
        ax4.set_yticks([1, 2, 3])
        ax4.set_yticklabels(['支路', '主干道', '高速公路'])
        ax4.set_title('速度-道路类型联合分布（2D核密度）', fontsize=15, fontweight='bold', color='#1a1a1a')
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        cbar4 = plt.colorbar(contour, ax=ax4, shrink=0.8)
        cbar4.set_label('密度', fontsize=12, fontweight='bold', color='#333333')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/10_speed_kde.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：10_speed_kde.png")
    
    def plot_11_street_traffic_hexbin(self):
        """图11: 街道流量六边形热力图（类似参考图）"""
        print("正在绘制：街道流量六边形热力图...")
        self._ensure_chinese_font()  # 确保字体设置
        
        df = self.load_data('road_congestion.csv')
        
        # 筛选晚高峰数据
        df_evening = df[df['time_period'] == 'evening_peak'].copy()
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # 使用六边形网格（hexbin）展示密度
        # 将拥堵指数转换为流量密度（datapoints/m²的概念）
        # 这里用拥堵指数作为密度指标
        hb = ax.hexbin(
            df_evening['longitude'], 
            df_evening['latitude'], 
            C=df_evening['congestion_index'],
            gridsize=30,  # 网格大小
            cmap=ROCKET_R_CMAP,  # 使用rocket_r颜色方案
            mincnt=1,  # 最小计数
            linewidths=0.1,  # 网格线宽度
            edgecolors='white',
            alpha=0.9
        )
        
        # 添加颜色条
        cb = plt.colorbar(hb, ax=ax, shrink=0.8, pad=0.02)
        cb.set_label('拥堵指数 (Congestion Index)', fontsize=13, fontweight='bold', color='#333333')
        
        # 设置坐标轴
        ax.set_xlabel('经度 (Longitude)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylabel('纬度 (Latitude)', fontsize=14, fontweight='bold', color='#333333')
        ax.set_title('深圳市晚高峰街道流量密度热力图\n(六边形网格密度分布)', 
                    fontsize=17, fontweight='bold', pad=25, color='#1a1a1a')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        # 添加网格
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # 设置坐标范围（深圳市区范围）
        ax.set_xlim(df_evening['longitude'].min() - 0.01, 
                   df_evening['longitude'].max() + 0.01)
        ax.set_ylim(df_evening['latitude'].min() - 0.01, 
                   df_evening['latitude'].max() + 0.01)
        
        # 添加比例尺（模拟）
        from matplotlib.patches import Rectangle
        scale_length = 0.05  # 约5km
        scale_x = df_evening['longitude'].min() + 0.01
        scale_y = df_evening['latitude'].min() + 0.01
        ax.add_patch(Rectangle((scale_x, scale_y), scale_length, 0.002, 
                              facecolor='black', edgecolor='black'))
        ax.text(scale_x + scale_length/2, scale_y - 0.005, '5 km', 
               ha='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/11_street_traffic_hexbin.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 已保存：11_street_traffic_hexbin.png")
        
        # 创建交互式版本（使用plotly）
        try:
            import plotly.graph_objects as go
            
            fig_plotly = go.Figure()
            
            # 添加六边形热力图
            fig_plotly.add_trace(go.Histogram2d(
                x=df_evening['longitude'],
                y=df_evening['latitude'],
                z=df_evening['congestion_index'],
                colorscale='Hot',  # 类似rocket_r
                nbinsx=30,
                nbinsy=30,
                colorbar=dict(title="拥堵指数")
            ))
            
            fig_plotly.update_layout(
                title='深圳市晚高峰街道流量密度热力图（交互式）',
                xaxis_title='经度',
                yaxis_title='纬度',
                width=1200,
                height=900,
                font=dict(size=12, family='Arial')
            )
            
            fig_plotly.write_html(f'{self.output_dir}/11_street_traffic_hexbin_interactive.html')
            print("✓ 已保存：11_street_traffic_hexbin_interactive.html")
        except Exception as e:
            print(f"⚠️  交互式图表生成失败: {e}")
    
    def generate_all_visualizations(self):
        """生成所有可视化图表"""
        print("="*60)
        print("开始生成深圳交通数据可视化...")
        print("="*60)
        
        try:
            self.plot_1_peak_hours_line()
            self.plot_2_congestion_heatmap()
            self.plot_3_metro_boxplot()
            self.plot_4_od_flow()
            self.plot_5_top_congested_roads()
            self.plot_6_travel_mode_pie()
            self.plot_7_weather_vs_congestion()
            self.plot_8_weekday_vs_weekend()
            self.plot_9_daily_trips_histogram()
            self.plot_10_speed_kde()
            self.plot_11_street_traffic_hexbin()
            
            print("\n" + "="*60)
            print("✅ 所有图表生成完成！")
            print(f"📁 输出目录: {self.output_dir}")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    visualizer = TrafficVisualizer()
    visualizer.generate_all_visualizations()


if __name__ == '__main__':
    main()

