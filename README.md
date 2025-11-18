# 📊 数据可视化课程期末项目

## 项目概述

本项目包含两个独立的数据分析模块：
1. **Climate** - 全球气候变化数据分析 🌍
2. **Traffic** - 深圳城市交通与出行模式分析 🚗

---

## 📁 项目结构

```
Final/
├── climate/                    # 气候数据分析模块
│   ├── data/                  # 气候数据
│   ├── output/                # 输出文件
│   ├── code/                  # 代码
│   ├── README.md             # 气候模块说明
│   └── KAGGLE_DATASET_RECOMMENDATIONS.md  # Kaggle数据集推荐
│
├── traffic/                   # 交通数据分析模块
│   ├── data/                 # 交通数据
│   ├── output/               # 输出文件
│   ├── code/                 # 代码
│   ├── README.md            # 交通模块说明
│   ├── DATA_SUMMARY.md      # 数据总结
│   ├── DATA_SOURCE_GUIDE.md # 数据源指南
│   └── DATA_AUTHENTICITY_GUIDE.md  # 数据真实性说明
│
├── venv/                     # Python虚拟环境
├── requirements.txt          # 依赖包列表
├── README.md                # 本文件
├── GETTING_STARTED.md       # 快速上手指南 ⭐
├── PROJECT_STRUCTURE.md     # 项目结构说明
└── activate.sh             # 虚拟环境激活脚本
```

---

## 🚀 快速开始

### 1. 环境设置

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果还未安装）
pip install -r requirements.txt
```

### 2. 运行气候数据分析

```bash
# 进入climate目录
cd climate/code

# 运行主程序
python main.py
```

**注意**：首次运行需要先从 Kaggle 下载数据：
- 数据集：Berkeley Earth Climate Change Data
- 链接：https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
- 下载后解压到 `climate/data/raw/` 文件夹

### 3. 运行交通数据分析

```bash
# 进入traffic目录
cd traffic/code

# 运行主程序
python main.py
```

---

## 📊 数据集说明

### Climate 模块

**数据来源**：Kaggle - Berkeley Earth Climate Change Data
- 全球温度数据（1750-2015）
- 城市、国家、州/省温度数据
- 包含经纬度信息

**可视化图表**：
1. 全球温度趋势线图
2. 国家温度对比（TOP20升温最快）
3. 城市温度地理散点图 ⭐
4. 季节性温度热力图
5. 温度分布箱线图

### Traffic 模块

**数据来源**：深圳交通数据（模拟 + 高德API）
- 小时交通流量数据
- 路段拥堵数据
- 地铁客流数据
- OD流量数据
- 出行方式数据

**可视化图表**（11张）：
1. 高峰时段折线图
2. 路段拥堵热力图
3. 地铁客流箱线图
4. OD路径流向图
5. TOP10拥堵道路
6. 出行方式饼图
7. 天气vs拥堵分析
8. 工作日vs周末对比
9. 出行次数直方图
10. 速度分布核密度图
11. 街道流量六边形热力图

---

## 🎨 可视化技术栈

- **基础图表**：Matplotlib, Seaborn
- **交互式图表**：Plotly
- **地理图表**：Folium, Geopandas
- **配色方案**：Viridis, Rocket_r, Coolwarm

---

## 📝 项目文档

### 核心文档（根目录）
- `README.md` - 本文件（项目总说明）
- `GETTING_STARTED.md` - 快速上手指南 ⭐
- `PROJECT_STRUCTURE.md` - 项目结构详解

### Climate 模块文档
- `climate/README.md` - 气候模块详细说明
- `climate/KAGGLE_DATASET_RECOMMENDATIONS.md` - Kaggle数据集推荐

### Traffic 模块文档
- `traffic/README.md` - 交通模块详细说明
- `traffic/DATA_SUMMARY.md` - 交通数据总结
- `traffic/DATA_SOURCE_GUIDE.md` - 交通数据源指南
- `traffic/DATA_AUTHENTICITY_GUIDE.md` - 数据真实性说明

---

## ⚙️ 依赖包

主要依赖包：
- pandas - 数据处理
- numpy - 数值计算
- matplotlib - 基础绘图
- seaborn - 统计可视化
- plotly - 交互式图表
- folium - 地理地图
- geopandas - 地理数据处理

查看完整列表：`requirements.txt`

---

## 🔧 常见问题

### Q1: 字体显示问题
**A**: 项目已自动配置 MacBook 系统字体（STHeiti），如果仍有问题：
```bash
# 清除matplotlib缓存
rm -rf ~/.matplotlib/fontlist-*.json
rm -rf ~/.cache/matplotlib
```

### Q2: 数据文件未找到
**A**: 确保已下载数据并放到正确位置：
- Climate 数据 → `climate/data/raw/`
- Traffic 数据会自动生成到 `traffic/data/sample/`

### Q3: 如何切换数据集？
**A**: 两个模块是独立的，分别在各自目录运行即可。

---

## 📧 更多信息

- 详细使用指南：`GETTING_STARTED.md`
- 项目结构说明：`PROJECT_STRUCTURE.md`
- 各模块说明：`climate/README.md` 和 `traffic/README.md`

---

## 📄 许可

本项目为课程作业项目，仅供学习使用。
