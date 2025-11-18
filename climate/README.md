# 🌍 Global Climate Change Data Analysis

## 数据集说明

### Kaggle数据集链接
**Berkeley Earth Climate Change Data**
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

### 数据集包含
1. **GlobalTemperatures.csv** - 全球温度数据（1750-2015）
2. **GlobalLandTemperaturesByCity.csv** - 城市温度数据
3. **GlobalLandTemperaturesByCountry.csv** - 国家温度数据
4. **GlobalLandTemperaturesByState.csv** - 州/省温度数据
5. **GlobalLandTemperaturesByMajorCity.csv** - 主要城市温度数据

---

## 📁 文件结构

```
climate/
├── data/                      # 数据文件夹
│   ├── raw/                  # 原始数据（从Kaggle下载）
│   └── processed/            # 处理后的数据
├── output/                   # 输出文件夹
│   ├── figures/             # 生成的图表
│   └── reports/             # 分析报告
└── code/                     # 代码文件夹
    ├── data_loader.py       # 数据加载
    ├── data_processor.py    # 数据处理
    ├── visualizer.py        # 可视化
    └── main.py              # 主程序
```

---

## 🚀 快速开始

### 1. 下载数据
```bash
# 在Kaggle上下载数据集
# 地址：https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

# 下载后解压到 climate/data/raw/ 文件夹
```

### 2. 安装依赖
```bash
# 已在根目录的 venv 中安装
source ../venv/bin/activate
```

### 3. 运行分析
```bash
cd code
python main.py
```

---

## 📊 可视化图表

### 计划生成的图表：

1. **全球温度趋势线图** 
   - 1750-2015年全球平均温度变化
   - 置信区间显示

2. **地理热力图**
   - 全球温度分布
   - 不同年份对比

3. **国家温度对比**
   - TOP20 升温最快的国家
   - 条形图 + 热力图

4. **季节性分析**
   - 月度温度变化模式
   - 热力图：月份 × 年份

5. **城市温度散点图** ⭐
   - 地理散点图（经纬度）
   - 颜色表示温度
   - 气泡大小表示数据置信度

6. **异常检测**
   - 极端温度事件
   - 时间序列异常点

7. **相关性分析**
   - 不同地区温度相关性
   - 热力图矩阵

8. **动画时间线**
   - 全球温度变化动画
   - 按年份播放

9. **3D表面图**
   - 时间 × 纬度 × 温度
   - 3D可视化

10. **区域对比**
    - 不同大洲温度趋势
    - 多子图对比

---

## 🎨 可视化技术栈

- **基础图表**: Matplotlib, Seaborn
- **交互式图表**: Plotly
- **地理图表**: Folium, Geopandas
- **3D图表**: Plotly 3D
- **动画**: Matplotlib Animation, Plotly

---

## 📈 分析角度

1. **全球变暖趋势**
   - 温度上升速率
   - 加速度分析

2. **地区差异**
   - 极地 vs 赤道
   - 发达国家 vs 发展中国家

3. **极端天气**
   - 热浪事件
   - 异常低温

4. **季节性变化**
   - 四季温度变化
   - 季节偏移

5. **预测未来**
   - 趋势外推
   - 气候模型

---

## 🔧 数据处理

### 数据清洗
- 缺失值处理
- 异常值检测
- 数据标准化

### 特征工程
- 时间特征提取（年、月、季节）
- 地理特征（纬度带、大洲）
- 统计特征（均值、方差、趋势）

---

## 💡 预期结论

1. 全球温度持续上升（特别是最近50年）
2. 北半球升温速度快于南半球
3. 极地地区升温最快
4. 极端天气事件频率增加
5. 城市热岛效应明显

---

## 📝 报告撰写

分析报告将包括：
- 数据概览
- 可视化图表
- 统计分析
- 结论和建议

