"""
美化版气候数据可视化 - 参考 Seaborn 官方最佳实践
学习自: https://seaborn.pydata.org/examples/
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from scipy import stats

# MacBook中文字体
MAC_CHINESE_FONTS = ['STHeiti', 'PingFang SC', 'Hiragino Sans GB', 'Arial Unicode MS']

# 设置专业的绘图风格 - 参考 Seaborn 官方
sns.set_theme(style="ticks", context="talk")  # talk 上下文：更大的字体
plt.rcParams['font.sans-serif'] = MAC_CHINESE_FONTS + ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# 专业配色方案
COLORS = {
    'magma': sns.color_palette("magma", n_colors=10),
    'viridis': sns.color_palette("viridis", n_colors=10),
    'mako': sns.color_palette("mako", n_colors=10),
    'rocket': sns.color_palette("rocket", n_colors=10),
}

print(f"✓ 字体: {MAC_CHINESE_FONTS[0]}")
print(f"✓ 风格: Seaborn 官方最佳实践")


class BeautifulClimateVisualizer:
    """美化版气候数据可视化"""
    
    def __init__(self, output_dir='../output/beautiful_figures'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    # ============================================================
    # 第一章：全球变暖趋势
    # ============================================================
    
    def plot_01_temperature_bands(self, df_global):
        """图1: 温度趋势带状图（更专业的展示）"""
        print("\n📊 绘制图1: 全球温度趋势...")
        
        # 数据准备
        df_yearly = df_global.groupby('year').agg({
            'LandAverageTemperature': 'mean',
            'LandAverageTemperatureUncertainty': 'mean'
        }).reset_index().dropna()
        
        # 创建图表 - 合理的尺寸
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 主线 - 使用 mako 深色
        ax.plot(df_yearly['year'], df_yearly['LandAverageTemperature'],
               linewidth=2.5, color=COLORS['mako'][7], label='全球温度', zorder=3)
        
        # 置信带 - 半透明
        ax.fill_between(
            df_yearly['year'],
            df_yearly['LandAverageTemperature'] - df_yearly['LandAverageTemperatureUncertainty'],
            df_yearly['LandAverageTemperature'] + df_yearly['LandAverageTemperatureUncertainty'],
            alpha=0.2, color=COLORS['mako'][7], label='95% 置信区间', zorder=2
        )
        
        # 趋势线（1950后）- 使用 rocket 亮色
        recent = df_yearly[df_yearly['year'] >= 1950]
        z = np.polyfit(recent['year'], recent['LandAverageTemperature'], 1)
        p = np.poly1d(z)
        ax.plot(recent['year'], p(recent['year']), 
               linestyle='--', linewidth=2, color=COLORS['rocket'][7],
               label=f'加速期趋势 ({z[0]:.4f}°C/年)', alpha=0.8, zorder=3)
        
        # 样式设置
        ax.set_xlabel('年份', fontsize=13, weight='medium')
        ax.set_ylabel('温度 (°C)', fontsize=13, weight='medium')
        ax.set_title('全球陆地平均温度长期趋势 (1750-2015)', 
                    fontsize=14, weight='bold', pad=15)
        
        # 图例 - 更紧凑
        ax.legend(loc='upper left', fontsize=10, frameon=True, 
                 framealpha=0.9, edgecolor='gray', facecolor='white')
        
        # 网格 - 更淡
        ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5)
        
        # 去掉上右边框
        sns.despine()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '01_temperature_bands.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 01_temperature_bands.png")
    
    # ============================================================
    # 第二章：国家温度热力图
    # ============================================================
    
    def plot_02_country_heatmap_pro(self, df_country):
        """图2: 专业热力图（参考 seaborn annotated heatmap）"""
        print("\n📊 绘制图2: 国家温度热力图...")
        
        # 选择TOP30变化最大的国家
        key_years = [1850, 1900, 1950, 1980, 2000, 2010]
        
        df_2010 = df_country[df_country['year'] == 2010].copy()
        df_1850 = df_country[df_country['year'] == 1850].copy()
        df_change = df_2010.merge(df_1850, on='Country', suffixes=('_2010', '_1850'))
        df_change['temp_change'] = (df_change['AverageTemperature_2010'] - 
                                    df_change['AverageTemperature_1850'])
        top_countries = df_change.nlargest(25, 'temp_change')['Country'].tolist()
        
        # 准备数据
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
        
        heatmap_df = pd.DataFrame(heatmap_data, index=top_countries, columns=key_years)
        
        # 绘制 - 合理尺寸
        fig, ax = plt.subplots(figsize=(10, 12))
        
        # 使用 rocket 配色，但调整 vmin/vmax 让对比度更明显
        data_min = heatmap_df.min().min()
        data_max = heatmap_df.max().max()
        
        sns.heatmap(heatmap_df, cmap='rocket', annot=False,
                   linewidths=1, linecolor='white', 
                   cbar_kws={'label': '平均温度 (°C)', 'shrink': 0.8},
                   ax=ax, vmin=data_min, vmax=data_max, robust=True)
        
        ax.set_xlabel('年份', fontsize=12, weight='medium')
        ax.set_ylabel('国家', fontsize=12, weight='medium')
        ax.set_title('TOP25升温最快国家的温度演变', 
                    fontsize=14, weight='bold', pad=15)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '02_country_heatmap_pro.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 02_country_heatmap_pro.png")
    
    # ============================================================
    # 第三章：纬度温度分布（小提琴图 - 参考官方）
    # ============================================================
    
    def plot_03_latitude_violin_pro(self, df_city):
        """图3: 专业小提琴图（参考 seaborn grouped violinplots）"""
        print("\n📊 绘制图3: 纬度带温度分布...")
        
        # 数据准备
        df_recent = df_city[df_city['year'] >= df_city['year'].max() - 50].copy()
        
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
        
        # 只选择主要纬度带（避免太挤）
        main_bands = ['60°N', '50°N', '40°N', '30°N', '20°N', '10°N', '0°N', '10°S', '20°S', '30°S']
        df_recent = df_recent[df_recent['latitude_band'].isin(main_bands)]
        
        # 排序
        def parse_lat(lat_str):
            if '°N' in lat_str:
                return float(lat_str.replace('°N', ''))
            elif '°S' in lat_str:
                return -float(lat_str.replace('°S', ''))
            return 0
        
        latitude_order = sorted(df_recent['latitude_band'].unique(), 
                               key=parse_lat, reverse=True)
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制小提琴图 - 使用 viridis 渐变
        sns.violinplot(data=df_recent, x='latitude_band', y='AverageTemperature',
                      order=latitude_order, palette='viridis',
                      inner='quartile', linewidth=1.2, ax=ax, saturation=0.8)
        
        ax.set_xlabel('纬度带', fontsize=12, weight='medium')
        ax.set_ylabel('温度 (°C)', fontsize=12, weight='medium')
        ax.set_title('不同纬度带的温度分布形态', 
                    fontsize=14, weight='bold', pad=15)
        
        # 旋转x轴标签
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        
        # 网格
        ax.yaxis.grid(True, alpha=0.25)
        ax.set_axisbelow(True)
        
        sns.despine()
        plt.tight_layout()
        plt.savefig(self.output_dir / '03_latitude_violin_pro.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 03_latitude_violin_pro.png")
    
    # ============================================================
    # 第四章：CO2与温度（hex jointplot - 参考官方）
    # ============================================================
    
    def plot_04_co2_temp_hexjoint(self, df_co2, df_global):
        """图4: CO2 vs 温度 Hex JointPlot（参考官方示例）"""
        print("\n📊 绘制图4: CO2-温度关系...")
        
        if df_co2 is None or df_co2.empty:
            print("⚠ CO₂数据不可用")
            return
        
        # 数据准备
        df_co2_yearly = df_co2.groupby('year')['co2_emission'].sum().reset_index()
        df_temp_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        df_merged = df_co2_yearly.merge(df_temp_yearly, on='year').dropna()
        
        # 创建 hex jointplot - 参考官方
        g = sns.jointplot(
            x=df_merged['co2_emission'] / 1e6, 
            y=df_merged['LandAverageTemperature'],
            kind="hex",
            color="#4CB391",  # 官方推荐的颜色
            height=8,
            ratio=5,
            marginal_kws=dict(bins=30, fill=True)
        )
        
        # 添加回归线
        z = np.polyfit(df_merged['co2_emission'] / 1e6, 
                      df_merged['LandAverageTemperature'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df_merged['co2_emission'].min() / 1e6, 
                            df_merged['co2_emission'].max() / 1e6, 100)
        g.ax_joint.plot(x_line, p(x_line), 'r-', linewidth=2.5, alpha=0.8,
                       label=f'R² = {np.corrcoef(df_merged["co2_emission"], df_merged["LandAverageTemperature"])[0,1]**2:.3f}')
        
        g.set_axis_labels('全球CO₂排放 (百万吨)', '全球温度 (°C)', 
                         fontsize=12, weight='medium')
        g.fig.suptitle('CO₂排放与温度的因果关系', 
                      fontsize=14, weight='bold', y=1.02)
        
        g.ax_joint.legend(fontsize=10)
        
        plt.savefig(self.output_dir / '04_co2_temp_hexjoint.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 04_co2_temp_hexjoint.png")
    
    # ============================================================
    # 第五章：CO2排放分布（高级组合图 - 参考官方）
    # ============================================================
    
    def plot_05_co2_jointplot_simple(self, df_co2):
        """图5: CO2排放简洁版 JointPlot（更清晰）"""
        print("\n📊 绘制图5: CO2排放分布...")
        
        if df_co2 is None or df_co2.empty:
            print("⚠ CO数据不可用")
            return
        
        # 使用最近年份
        latest_year = df_co2['year'].max()
        df_latest = df_co2[df_co2['year'] == latest_year].copy()
        df_latest = df_latest.dropna(subset=['co2_per_capita', 'co2_emission'])
        df_latest = df_latest[df_latest['co2_per_capita'] > 0]
        df_latest = df_latest[df_latest['co2_emission'] > 0]
        
        # 创建简洁的 JointPlot
        g = sns.jointplot(
            data=df_latest, 
            x='co2_per_capita', 
            y='co2_emission',
            kind="scatter",
            height=9,
            ratio=4,
            color=COLORS['viridis'][6],
            alpha=0.6,
            marginal_kws=dict(bins=25, fill=True, color=COLORS['viridis'][5])
        )
        
        g.set_axis_labels('人均CO排放 (吨/人)', '国家总排放 (吨)', 
                         fontsize=12, weight='medium')
        g.fig.suptitle(f'全球CO排放结构 - 人均vs总量 ({latest_year}年)', 
                      fontsize=14, weight='bold', y=1.01)
        
        plt.savefig(self.output_dir / '05_co2_jointplot_simple.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 05_co2_jointplot_simple.png")
    
    # ============================================================
    # 第六章：条件KDE（参考官方 conditional_kde）
    # ============================================================
    
    def plot_06_co2_time_series_lines(self, df_co2):
        """图6: CO2时间序列折线图（更清晰的展示）"""
        print("\n📊 绘制图6: CO2时间序列...")
        
        if df_co2 is None or df_co2.empty:
            print("⚠ CO数据不可用")
            return
        
        # 准备数据：选择主要排放国
        top_countries = df_co2.groupby('country')['co2_emission'].sum().nlargest(8).index.tolist()
        df_top = df_co2[df_co2['country'].isin(top_countries)].copy()
        
        # 按年份和国家聚合
        df_grouped = df_top.groupby(['year', 'country'])['co2_emission'].sum().reset_index()
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # 使用 viridis 配色
        palette = sns.color_palette("viridis", n_colors=len(top_countries))
        
        for i, country in enumerate(top_countries):
            df_c = df_grouped[df_grouped['country'] == country]
            ax.plot(df_c['year'], df_c['co2_emission'] / 1e6, 
                   linewidth=2.5, label=country, color=palette[i], alpha=0.9)
        
        ax.set_xlabel('年份', fontsize=12, weight='medium')
        ax.set_ylabel('CO排放 (百万吨)', fontsize=12, weight='medium')
        ax.set_title('主要排放国的CO时间序列', 
                    fontsize=14, weight='bold', pad=15)
        
        ax.legend(loc='upper left', fontsize=10, frameon=True, 
                 framealpha=0.9, ncol=2)
        ax.grid(True, alpha=0.25)
        sns.despine()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '06_co2_time_series_lines.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 06_co2_time_series_lines.png")
    
    # ============================================================
    # 第七章：海平面与温度（双Y轴专业版）
    # ============================================================
    
    def plot_07_sealevel_temp_dual(self, df_sea_level, df_global):
        """图7: 海平面-温度双轴图（更专业）"""
        print("\n📊 绘制图7: 海平面与温度关系...")
        
        if df_sea_level is None or df_sea_level.empty:
            print("⚠ 海平面数据不可用")
            return
        
        # 数据准备
        df_temp_yearly = df_global.groupby('year')['LandAverageTemperature'].mean().reset_index()
        df_temp_aligned = df_temp_yearly[df_temp_yearly['year'].isin(df_sea_level['year'])]
        
        # 创建图表
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # 温度轴
        color1 = COLORS['magma'][6]
        ax1.plot(df_temp_aligned['year'], df_temp_aligned['LandAverageTemperature'],
                linewidth=3, color=color1, label='全球温度', marker='o', 
                markersize=3, markevery=2)
        ax1.set_xlabel('年份', fontsize=12, weight='medium')
        ax1.set_ylabel('温度 (°C)', fontsize=12, weight='medium', color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        
        # 海平面轴
        ax2 = ax1.twinx()
        color2 = COLORS['viridis'][7]
        ax2.plot(df_sea_level['year'], df_sea_level['sea_level'],
                linewidth=3, color=color2, label='海平面', marker='s', 
                markersize=3, markevery=2)
        ax2.set_ylabel('海平面高度 (mm)', fontsize=12, weight='medium', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        # 标题
        ax1.set_title('温度与海平面的同步上升', 
                     fontsize=14, weight='bold', pad=15)
        
        # 图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, 
                  loc='upper left', fontsize=10, framealpha=0.9)
        
        ax1.grid(True, alpha=0.25)
        sns.despine(ax=ax1, right=False)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '07_sealevel_temp_dual.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 07_sealevel_temp_dual.png")
    
    # ============================================================
    # 第八章：PairPlot（更专业）
    # ============================================================
    
    def plot_08_pairplot_pro(self, df_global, df_co2, df_sea_level):
        """图8: 专业PairPlot"""
        print("\n📊 绘制图8: 多变量相关矩阵...")
        
        # 数据准备
        df_temp_yearly = df_global.groupby('year').agg({
            'LandAverageTemperature': 'mean'
        }).reset_index()
        
        df_combined = df_temp_yearly.copy()
        
        if df_co2 is not None and not df_co2.empty:
            df_co2_yearly = df_co2.groupby('year')['co2_emission'].sum().reset_index()
            df_combined = df_combined.merge(df_co2_yearly, on='year', how='left')
        
        if df_sea_level is not None and not df_sea_level.empty:
            df_combined = df_combined.merge(df_sea_level[['year', 'sea_level']], 
                                           on='year', how='left')
        
        df_combined = df_combined.dropna()
        df_combined['年代'] = pd.cut(df_combined['year'], 
                                    bins=[1960, 1980, 2000, 2020],
                                    labels=['1960-1980', '1980-2000', '2000-2020'])
        
        # 重命名列（中文）
        df_combined = df_combined.rename(columns={
            'LandAverageTemperature': '温度',
            'co2_emission': 'CO₂排放',
            'sea_level': '海平面'
        })
        
        plot_vars = ['温度', 'CO₂排放', '海平面']
        plot_vars = [v for v in plot_vars if v in df_combined.columns]
        
        if len(plot_vars) < 2:
            print("⚠ 变量不足")
            return
        
        # 绘制 PairPlot - 使用 mako 配色
        g = sns.pairplot(df_combined[plot_vars + ['年代']], hue='年代',
                        palette='mako', diag_kind='kde',
                        plot_kws={'alpha': 0.7, 's': 40, 'edgecolor': 'white', 'linewidth': 0.5},
                        diag_kws={'alpha': 0.7},
                        height=3, aspect=1)
        
        g.fig.suptitle('气候变量相关矩阵', fontsize=14, weight='bold', y=1.01)
        
        plt.savefig(self.output_dir / '08_pairplot_pro.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 保存: 08_pairplot_pro.png")
    
    # ============================================================
    # 主函数
    # ============================================================
    
    def generate_all(self, df_global, df_country, df_city, df_co2=None, df_sea_level=None):
        """生成所有美化图表"""
        print("\n" + "="*80)
        print("🎨 生成美化版可视化（参考 Seaborn 官方最佳实践）")
        print("="*80)
        
        try:
            self.plot_01_temperature_bands(df_global)
            self.plot_02_country_heatmap_pro(df_country)
            self.plot_03_latitude_violin_pro(df_city)
            
            if df_co2 is not None and not df_co2.empty:
                self.plot_04_co2_temp_hexjoint(df_co2, df_global)
                self.plot_05_co2_jointplot_simple(df_co2)
                self.plot_06_co2_time_series_lines(df_co2)
            
            if df_sea_level is not None and not df_sea_level.empty:
                self.plot_07_sealevel_temp_dual(df_sea_level, df_global)
            
            self.plot_08_pairplot_pro(df_global, df_co2, df_sea_level)
            
            print("\n" + "="*80)
            print("✅ 所有美化图表生成完成！")
            print(f"📁 {self.output_dir}")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()

