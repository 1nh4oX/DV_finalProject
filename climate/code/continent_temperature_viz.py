"""
大洲温度变化可视化
- 按大洲分组显示温度异常变化
- 参考风格：堆叠面积图 + 地理背景
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pathlib import Path
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['STHeiti', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 设置 seaborn 主题
sns.set_theme(style='whitegrid', palette='crest')

# 国家到大洲的映射
COUNTRY_TO_CONTINENT = {
    # 欧洲 (Europe)
    'Austria': 'Europe', 'Belgium': 'Europe', 'Bulgaria': 'Europe', 'Croatia': 'Europe',
    'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe',
    'France': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe',
    'Iceland': 'Europe', 'Ireland': 'Europe', 'Italy': 'Europe', 'Latvia': 'Europe',
    'Lithuania': 'Europe', 'Luxembourg': 'Europe', 'Netherlands': 'Europe', 'Norway': 'Europe',
    'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe', 'Slovakia': 'Europe',
    'Slovenia': 'Europe', 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe',
    'United Kingdom': 'Europe', 'Ukraine': 'Europe', 'Belarus': 'Europe', 'Moldova': 'Europe',
    'Serbia': 'Europe', 'Albania': 'Europe', 'Macedonia': 'Europe', 'Montenegro': 'Europe',
    'Bosnia And Herzegovina': 'Europe', 'Kosovo': 'Europe', 'Malta': 'Europe', 'Cyprus': 'Europe',
    'Åland': 'Europe', 'Andorra': 'Europe', 'Monaco': 'Europe', 'San Marino': 'Europe',
    'Liechtenstein': 'Europe', 'Vatican City': 'Europe', 'Faroe Islands': 'Europe',
    'Gibraltar': 'Europe', 'Isle Of Man': 'Europe', 'Jersey': 'Europe', 'Guernsey': 'Europe',
    
    # 亚洲 (Asia)
    'China': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia', 'North Korea': 'Asia',
    'Mongolia': 'Asia', 'Taiwan': 'Asia', 'Hong Kong': 'Asia', 'Macau': 'Asia',
    'India': 'Asia', 'Pakistan': 'Asia', 'Bangladesh': 'Asia', 'Sri Lanka': 'Asia',
    'Nepal': 'Asia', 'Bhutan': 'Asia', 'Afghanistan': 'Asia', 'Myanmar': 'Asia',
    'Thailand': 'Asia', 'Vietnam': 'Asia', 'Cambodia': 'Asia', 'Laos': 'Asia',
    'Malaysia': 'Asia', 'Singapore': 'Asia', 'Indonesia': 'Asia', 'Philippines': 'Asia',
    'Brunei': 'Asia', 'Timor Leste': 'Asia', 'Russia': 'Asia',  # 大部分在亚洲
    'Kazakhstan': 'Asia', 'Uzbekistan': 'Asia', 'Turkmenistan': 'Asia', 'Kyrgyzstan': 'Asia',
    'Tajikistan': 'Asia', 'Iran': 'Asia', 'Iraq': 'Asia', 'Syria': 'Asia',
    'Jordan': 'Asia', 'Lebanon': 'Asia', 'Israel': 'Asia', 'Palestine': 'Asia',
    'Saudi Arabia': 'Asia', 'Yemen': 'Asia', 'Oman': 'Asia', 'United Arab Emirates': 'Asia',
    'Qatar': 'Asia', 'Bahrain': 'Asia', 'Kuwait': 'Asia', 'Turkey': 'Asia',
    'Armenia': 'Asia', 'Azerbaijan': 'Asia', 'Georgia': 'Asia', 'Maldives': 'Asia',
    
    # 北美洲 (North America)
    'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
    'Guatemala': 'North America', 'Cuba': 'North America', 'Haiti': 'North America',
    'Dominican Republic': 'North America', 'Honduras': 'North America', 'Nicaragua': 'North America',
    'El Salvador': 'North America', 'Costa Rica': 'North America', 'Panama': 'North America',
    'Jamaica': 'North America', 'Trinidad And Tobago': 'North America', 'Bahamas': 'North America',
    'Barbados': 'North America', 'Belize': 'North America', 'Puerto Rico': 'North America',
    'Greenland': 'North America', 'Bermuda': 'North America', 'Cayman Islands': 'North America',
    
    # 南美洲 (South America)
    'Brazil': 'South America', 'Argentina': 'South America', 'Colombia': 'South America',
    'Peru': 'South America', 'Venezuela': 'South America', 'Chile': 'South America',
    'Ecuador': 'South America', 'Bolivia': 'South America', 'Paraguay': 'South America',
    'Uruguay': 'South America', 'Guyana': 'South America', 'Suriname': 'South America',
    'French Guiana': 'South America', 'Falkland Islands (Islas Malvinas)': 'South America',
    
    # 非洲 (Africa)
    'Nigeria': 'Africa', 'Ethiopia': 'Africa', 'Egypt': 'Africa', 'Congo (Democratic Republic Of The)': 'Africa',
    'South Africa': 'Africa', 'Tanzania': 'Africa', 'Kenya': 'Africa', 'Uganda': 'Africa',
    'Algeria': 'Africa', 'Sudan': 'Africa', 'Morocco': 'Africa', 'Angola': 'Africa',
    'Mozambique': 'Africa', 'Ghana': 'Africa', 'Madagascar': 'Africa', 'Cameroon': 'Africa',
    'Côte D\'Ivoire': 'Africa', 'Niger': 'Africa', 'Burkina Faso': 'Africa', 'Mali': 'Africa',
    'Malawi': 'Africa', 'Zambia': 'Africa', 'Senegal': 'Africa', 'Chad': 'Africa',
    'Somalia': 'Africa', 'Zimbabwe': 'Africa', 'Guinea': 'Africa', 'Rwanda': 'Africa',
    'Benin': 'Africa', 'Burundi': 'Africa', 'Tunisia': 'Africa', 'Togo': 'Africa',
    'Sierra Leone': 'Africa', 'Libya': 'Africa', 'Congo': 'Africa', 'Liberia': 'Africa',
    'Central African Republic': 'Africa', 'Mauritania': 'Africa', 'Eritrea': 'Africa',
    'Namibia': 'Africa', 'Gambia': 'Africa', 'Botswana': 'Africa', 'Gabon': 'Africa',
    'Lesotho': 'Africa', 'Guinea Bissau': 'Africa', 'Equatorial Guinea': 'Africa',
    'Mauritius': 'Africa', 'Eswatini': 'Africa', 'Swaziland': 'Africa', 'Djibouti': 'Africa',
    'Comoros': 'Africa', 'Cape Verde': 'Africa', 'Sao Tome And Principe': 'Africa',
    'Seychelles': 'Africa', 'Réunion': 'Africa', 'Mayotte': 'Africa', 'Western Sahara': 'Africa',
    
    # 大洋洲 (Oceania)
    'Australia': 'Oceania', 'New Zealand': 'Oceania', 'Papua New Guinea': 'Oceania',
    'Fiji': 'Oceania', 'Solomon Islands': 'Oceania', 'Vanuatu': 'Oceania',
    'New Caledonia': 'Oceania', 'French Polynesia': 'Oceania', 'Samoa': 'Oceania',
    'Guam': 'Oceania', 'Kiribati': 'Oceania', 'Tonga': 'Oceania', 'Micronesia': 'Oceania',
    'Palau': 'Oceania', 'Marshall Islands': 'Oceania', 'Nauru': 'Oceania', 'Tuvalu': 'Oceania',
}

# 大洲配色（混合 flare 和 crest 调色板）
# 按堆叠位置分配：底层冷色，顶层暖色
FLARE_COLORS = sns.color_palette('flare', 6).as_hex()
CREST_COLORS = sns.color_palette('crest', 6).as_hex()

# 从冷到暖的颜色渐变（6个颜色）
# 底层（小值）-> 顶层（大值）
COLD_TO_WARM_COLORS = [
    CREST_COLORS[5],    # 深蓝 #254b7f （最底层）
    CREST_COLORS[3],    # 蓝绿 #287a8c
    CREST_COLORS[0],    # 浅绿 #7dba91
    FLARE_COLORS[0],    # 浅橙 #e98d6b
    FLARE_COLORS[2],    # 玫红 #d14a61
    FLARE_COLORS[4],    # 深紫红 #8f3371 （最顶层）
]

# CONTINENT_COLORS 将在运行时根据数据大小动态分配
CONTINENT_COLORS = {}  # 占位，运行时更新


def load_and_process_data(data_path='../data/raw/GlobalLandTemperaturesByCountry.csv'):
    """加载并处理数据"""
    print("📥 加载国家温度数据...")
    df = pd.read_csv(data_path)
    
    # 转换日期
    df['dt'] = pd.to_datetime(df['dt'])
    df['Year'] = df['dt'].dt.year
    
    # 移除缺失值
    df = df.dropna(subset=['AverageTemperature'])
    
    # 添加大洲列
    df['Continent'] = df['Country'].map(COUNTRY_TO_CONTINENT)
    
    # 移除未映射的国家
    unmapped = df[df['Continent'].isna()]['Country'].unique()
    if len(unmapped) > 0:
        print(f"  ⚠️ 未映射的国家 ({len(unmapped)}): {list(unmapped)[:10]}...")
    
    df = df.dropna(subset=['Continent'])
    
    print(f"  ✓ 数据加载完成：{len(df)} 条记录")
    print(f"  ✓ 时间范围：{df['Year'].min()} - {df['Year'].max()}")
    print(f"  ✓ 大洲数量：{df['Continent'].nunique()}")
    
    return df


def calculate_temperature_anomaly(df, baseline_start=1850, baseline_end=1900):
    """计算相对于基准期的温度异常"""
    print(f"\n🔧 计算温度异常值（基准期：{baseline_start}-{baseline_end}）...")
    
    # 计算每个大洲的年均温度
    yearly_continent = df.groupby(['Year', 'Continent'])['AverageTemperature'].mean().reset_index()
    yearly_continent.columns = ['Year', 'Continent', 'Temperature']
    
    # 计算每个大洲的基准期平均温度
    baseline_temps = yearly_continent[
        (yearly_continent['Year'] >= baseline_start) & 
        (yearly_continent['Year'] <= baseline_end)
    ].groupby('Continent')['Temperature'].mean()
    
    # 计算温度异常
    yearly_continent['Anomaly'] = yearly_continent.apply(
        lambda row: row['Temperature'] - baseline_temps.get(row['Continent'], 0),
        axis=1
    )
    
    print(f"  ✓ 异常值计算完成")
    
    return yearly_continent


def create_continent_visualization(df_anomaly, output_dir='../output/figures'):
    """
    创建大洲温度变化可视化
    风格：深色背景 + 堆叠面积图 + 世界地图图例
    """
    print("\n🎨 生成可视化图表...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 设置深色主题
    plt.style.use('dark_background')
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # 准备数据 - 按大洲的最终异常值排序
    final_anomalies = df_anomaly[df_anomaly['Year'] == df_anomaly['Year'].max()].set_index('Continent')['Anomaly']
    sorted_continents = final_anomalies.sort_values(ascending=False).index.tolist()
    
    # 绘制每个大洲的温度异常曲线（堆叠面积图风格）
    for continent in sorted_continents:
        continent_data = df_anomaly[df_anomaly['Continent'] == continent].sort_values('Year')
        
        # 应用5年滑动平均使曲线更平滑
        continent_data = continent_data.copy()
        continent_data['Anomaly_Smooth'] = continent_data['Anomaly'].rolling(window=5, center=True).mean()
        continent_data = continent_data.dropna()
        
        color = CONTINENT_COLORS.get(continent, '#FFFFFF')
        
        # 绘制填充区域
        ax.fill_between(
            continent_data['Year'], 
            0, 
            continent_data['Anomaly_Smooth'],
            alpha=0.3, 
            color=color,
            linewidth=0
        )
        
        # 绘制主曲线
        ax.plot(
            continent_data['Year'], 
            continent_data['Anomaly_Smooth'],
            color=color, 
            linewidth=2.5, 
            label=continent,
            alpha=0.9
        )
        
        # 在曲线末端添加标签和数值
        if len(continent_data) > 0:
            last_year = continent_data['Year'].iloc[-1]
            last_anomaly = continent_data['Anomaly_Smooth'].iloc[-1]
            
            # 数值标签（带圆角矩形背景）
            ax.annotate(
                f'{last_anomaly:.2f}°C',
                xy=(last_year, last_anomaly),
                xytext=(last_year + 8, last_anomaly),
                fontsize=11,
                fontweight='bold',
                color='white',
                ha='left',
                va='center',
                bbox=dict(
                    boxstyle='round,pad=0.3',
                    facecolor=color,
                    edgecolor='none',
                    alpha=0.9
                )
            )
            
            # 大洲名称标签
            ax.annotate(
                continent,
                xy=(last_year + 8, last_anomaly - 0.15),
                xytext=(last_year + 25, last_anomaly - 0.15),
                fontsize=10,
                color='#cccccc',
                ha='left',
                va='center'
            )
    
    # 设置坐标轴
    year_min = df_anomaly['Year'].min()
    year_max = df_anomaly['Year'].max()
    
    ax.set_xlim(year_min, year_max + 50)  # 右侧留出空间放标签
    ax.set_ylim(-1.5, 2.5)
    
    # 标题
    ax.set_title(
        f'Temperature Anomaly by Continent\n{year_min}-{year_max}',
        fontsize=20,
        fontweight='bold',
        color='white',
        pad=20
    )
    
    # 坐标轴标签
    ax.set_xlabel('Year', fontsize=14, color='#cccccc')
    ax.set_ylabel('Temperature Anomaly (°C)', fontsize=14, color='#cccccc')
    
    # 网格线
    ax.grid(True, linestyle='--', alpha=0.2, color='white')
    ax.axhline(y=0, color='white', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # 刻度样式
    ax.tick_params(colors='#cccccc', labelsize=12)
    
    # 添加基准期标注
    ax.axvspan(1850, 1900, alpha=0.1, color='white', label='Baseline Period (1850-1900)')
    ax.annotate(
        'Baseline\n(1850-1900)',
        xy=(1875, -1.3),
        fontsize=9,
        color='#888888',
        ha='center',
        va='top'
    )
    
    # 添加数据来源
    ax.text(
        0.02, 0.02,
        'Data: Berkeley Earth Surface Temperature Dataset',
        transform=ax.transAxes,
        fontsize=9,
        color='#666666',
        ha='left',
        va='bottom'
    )
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    output_file = output_path / 'continent_temperature_anomaly.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"  ✓ 已保存：{output_file}")
    
    plt.close()
    
    return output_file


def create_stacked_area_version(df_anomaly, output_dir='../output/figures'):
    """
    创建堆叠面积图版本（累积视图）
    """
    print("\n🎨 生成堆叠面积图版本...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 设置深色主题
    plt.style.use('dark_background')
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # 准备数据透视表
    pivot_df = df_anomaly.pivot_table(
        values='Anomaly', 
        index='Year', 
        columns='Continent', 
        aggfunc='mean'
    )
    
    # 应用滑动平均
    pivot_df = pivot_df.rolling(window=5, center=True).mean().dropna()
    
    # 只保留正异常值用于堆叠（将负值设为0）
    pivot_df_positive = pivot_df.clip(lower=0)
    
    # 按最终值排序大洲
    final_values = pivot_df_positive.iloc[-1].sort_values(ascending=True)
    sorted_continents = final_values.index.tolist()
    
    # 准备堆叠数据
    colors = [CONTINENT_COLORS.get(c, '#FFFFFF') for c in sorted_continents]
    
    # 绘制堆叠面积图
    ax.stackplot(
        pivot_df_positive.index,
        [pivot_df_positive[c].values for c in sorted_continents],
        labels=sorted_continents,
        colors=colors,
        alpha=0.8
    )
    
    # 在右侧添加标签
    cumsum = 0
    year_max = pivot_df_positive.index.max()
    for i, continent in enumerate(sorted_continents):
        value = pivot_df_positive[continent].iloc[-1]
        cumsum += value
        label_y = cumsum - value / 2
        
        color = CONTINENT_COLORS.get(continent, '#FFFFFF')
        
        # 数值标签
        ax.annotate(
            f'{value:.2f}',
            xy=(year_max, label_y),
            xytext=(year_max + 5, label_y),
            fontsize=10,
            fontweight='bold',
            color='white',
            ha='left',
            va='center',
            bbox=dict(
                boxstyle='round,pad=0.2',
                facecolor=color,
                edgecolor='none',
                alpha=0.9
            )
        )
        
        # 大洲名称
        ax.annotate(
            continent,
            xy=(year_max + 20, label_y),
            fontsize=9,
            color='#cccccc',
            ha='left',
            va='center'
        )
    
    # 设置坐标轴
    year_min = pivot_df_positive.index.min()
    ax.set_xlim(year_min, year_max + 50)
    
    # 标题
    ax.set_title(
        f'Cumulative Temperature Anomaly by Continent\n{int(year_min)}-{int(year_max)}',
        fontsize=20,
        fontweight='bold',
        color='white',
        pad=20
    )
    
    # 坐标轴标签
    ax.set_xlabel('Year', fontsize=14, color='#cccccc')
    ax.set_ylabel('Temperature Anomaly (°C)', fontsize=14, color='#cccccc')
    
    # 网格线
    ax.grid(True, linestyle='--', alpha=0.2, color='white')
    
    # 刻度样式
    ax.tick_params(colors='#cccccc', labelsize=12)
    
    # 数据来源
    ax.text(
        0.02, 0.02,
        'Data: Berkeley Earth Surface Temperature Dataset',
        transform=ax.transAxes,
        fontsize=9,
        color='#666666',
        ha='left',
        va='bottom'
    )
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    output_file = output_path / 'continent_temperature_stacked.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"  ✓ 已保存：{output_file}")
    
    plt.close()
    
    return output_file


def create_stacked_with_map(df_anomaly, output_dir='../output/figures'):
    """
    创建带世界地图背景的堆叠面积图
    - 左上角内嵌世界地图，各大洲使用对应颜色
    - 主图显示堆叠面积图
    - 使用 seaborn crest 主题 + 白色背景
    """
    print("\n🎨 生成带世界地图背景的堆叠面积图...")
    
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        from cartopy.io import shapereader
    except ImportError:
        print("  ❌ 需要安装 cartopy: pip install cartopy")
        return None
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 使用 seaborn whitegrid 主题
    sns.set_theme(style='whitegrid', palette='crest')
    
    # 创建图形 - 白色背景
    fig, ax_main = plt.subplots(figsize=(16, 10), facecolor='white')
    ax_main.set_facecolor('white')
    
    # ========== 绘制堆叠面积图 ==========
    pivot_df = df_anomaly.pivot_table(
        values='Anomaly', 
        index='Year', 
        columns='Continent', 
        aggfunc='mean'
    )
    pivot_df = pivot_df.rolling(window=5, center=True).mean().dropna()
    pivot_df_positive = pivot_df.clip(lower=0)
    
    # 按数值大小排序（小的在底部，大的在顶部）
    final_values = pivot_df_positive.iloc[-1].sort_values(ascending=True)
    sorted_continents = final_values.index.tolist()
    
    # 根据堆叠位置分配颜色：底层冷色，顶层暖色
    colors = [COLD_TO_WARM_COLORS[i] for i in range(len(sorted_continents))]
    
    ax_main.stackplot(
        pivot_df_positive.index,
        [pivot_df_positive[c].values for c in sorted_continents],
        labels=sorted_continents,
        colors=colors,
        alpha=0.85
    )
    
    # 计算总高度用于标签定位
    cumsum = 0
    year_max = pivot_df_positive.index.max()
    year_min = pivot_df_positive.index.min()
    
    for i, continent in enumerate(sorted_continents):
        value = pivot_df_positive[continent].iloc[-1]
        cumsum += value
        label_y = cumsum - value / 2
        color = COLD_TO_WARM_COLORS[i]  # 根据堆叠位置获取颜色
        
        ax_main.annotate(
            f'{value:.2f}°C',
            xy=(year_max, label_y),
            xytext=(year_max + 3, label_y),
            fontsize=11,
            fontweight='bold',
            color='white',
            ha='left',
            va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, edgecolor='none', alpha=0.95)
        )
        ax_main.annotate(
            continent,
            xy=(year_max + 28, label_y),
            fontsize=10,
            color='#333333',
            ha='left',
            va='center'
        )
    
    # 设置坐标轴范围
    ax_main.set_xlim(year_min, year_max + 60)
    ax_main.set_ylim(0, cumsum * 1.15)
    
    # 标题 - 放在右侧，给地图让位
    ax_main.set_title(
        f'Temperature Anomaly by Continent ({int(year_min)}-{int(year_max)})',
        fontsize=22,
        fontweight='bold',
        color='#1a1a2e',
        pad=15,
        loc='right'
    )
    ax_main.set_xlabel('Year', fontsize=14, color='#333333')
    ax_main.set_ylabel('Temperature Anomaly (°C)', fontsize=14, color='#333333')
    ax_main.grid(True, linestyle='-', alpha=0.3, color='#cccccc')
    ax_main.tick_params(colors='#333333', labelsize=12)
    
    # 数据来源
    ax_main.text(0.01, 0.01, 'Data: Berkeley Earth Surface Temperature Dataset', 
                 transform=ax_main.transAxes, fontsize=8, color='#888888', ha='left', va='bottom')
    
    # ========== 在左上角内嵌世界地图 ==========
    # 构建大洲到颜色的映射（与堆叠图一致）
    continent_color_map = {continent: COLD_TO_WARM_COLORS[i] for i, continent in enumerate(sorted_continents)}
    
    ax_map = fig.add_axes(
        [0.08, 0.55, 0.35, 0.38],
        projection=ccrs.Robinson()
    )
    ax_map.set_facecolor('#f0f8ff')  # 浅蓝色海洋背景
    
    # 设置地图背景
    ax_map.set_global()
    ax_map.patch.set_facecolor('#e8f4f8')
    ax_map.patch.set_alpha(0.95)
    
    # 设置边框
    for spine in ax_map.spines.values():
        spine.set_edgecolor('#cccccc')
        spine.set_linewidth(1)
    
    # 添加海洋背景
    ax_map.add_feature(cfeature.OCEAN, facecolor='#d4e8f0', edgecolor='none')
    
    # 获取国家形状并按大洲着色（使用动态颜色映射）
    try:
        shpfilename = shapereader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
        reader = shapereader.Reader(shpfilename)
        
        for country in reader.records():
            country_name = country.attributes.get('NAME', '')
            continent = COUNTRY_TO_CONTINENT.get(country_name, None)
            
            if continent and continent in continent_color_map:
                color = continent_color_map[continent]
                ax_map.add_geometries(
                    [country.geometry],
                    ccrs.PlateCarree(),
                    facecolor=color,
                    edgecolor='#555555',
                    linewidth=0.2,
                    alpha=0.9
                )
            else:
                # 未分类的国家用浅灰色
                ax_map.add_geometries(
                    [country.geometry],
                    ccrs.PlateCarree(),
                    facecolor='#e0e0e0',
                    edgecolor='#888888',
                    linewidth=0.15,
                    alpha=0.7
                )
    except Exception as e:
        print(f"  ⚠️ 加载国家形状失败: {e}")
        ax_map.add_feature(cfeature.LAND, facecolor='#e0e0e0', edgecolor='#888888')
    
    # 地图标题
    ax_map.set_title('by Region', fontsize=11, color='#333333', pad=3, fontweight='bold')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    output_file = output_path / 'continent_temperature_with_map.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  ✓ 已保存：{output_file}")
    
    plt.close()
    
    return output_file


def main():
    """主函数"""
    print("=" * 70)
    print("  大洲温度变化可视化")
    print("  Continent Temperature Anomaly Visualization")
    print("=" * 70)
    
    # 加载数据
    df = load_and_process_data()
    
    # 计算温度异常
    df_anomaly = calculate_temperature_anomaly(df)
    
    # 生成可视化
    output1 = create_continent_visualization(df_anomaly)
    output2 = create_stacked_area_version(df_anomaly)
    output3 = create_stacked_with_map(df_anomaly)
    
    print("\n" + "=" * 70)
    print("✅ 完成！生成的图表：")
    print(f"  1. {output1}")
    print(f"  2. {output2}")
    if output3:
        print(f"  3. {output3}")
    print("=" * 70)


if __name__ == '__main__':
    main()
