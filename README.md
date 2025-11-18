# 深圳城市交通与出行模式分析实验

## 项目概述
本项目旨在分析深圳市的交通出行模式，包括拥堵情况、客流分析、出行方式等多个维度。

## 实验步骤规划

### 第一阶段：数据收集（1-2天）
1. **高德交通大数据开放平台**
   - 注册账号：https://lbs.amap.com/
   - 申请交通态势API
   - 获取深圳市道路拥堵指数、路段速度数据
   
2. **深圳市交通运输局开放数据**
   - 官网：http://www.sz.gov.cn/cn/xxgk/zfxxgj/
   - 深圳市政府数据开放平台：https://opendata.sz.gov.cn/
   - 可获取：地铁客流、公交线路、站点数据

3. **其他数据源**
   - 深圳地铁官网：http://www.szmc.net/
   - 中国气象数据网：http://data.cma.cn/
   - Kaggle相关数据集作为参考

### 第二阶段：数据清洗与预处理（2-3天）
1. 数据去重、缺失值处理
2. 时间格式统一（工作日/周末标注）
3. 地理坐标标准化
4. 数据聚合与统计

### 第三阶段：数据分析与可视化（3-4天）
按照以下顺序完成10种图表：

1. **高峰时段折线图** - 展示一天中不同时段的交通流量变化
2. **路段拥堵热力图** - 在深圳地图上展示各路段拥堵程度
3. **地铁/公交客流箱线图** - 分析不同线路的客流分布特征
4. **城市OD路径流向图** - 展示起点-终点的出行流向
5. **TOP10拥堵道路条形图** - 排名最拥堵的道路
6. **出行方式占比饼图** - 地铁、公交、自驾、骑行等比例
7. **天气vs拥堵散点回归** - 分析天气对交通的影响
8. **工作日vs周末对比图** - 对比不同类型日期的交通特征
9. **日均出行次数直方图** - 展示出行频次分布
10. **速度分布核密度图** - 分析路段速度分布规律

### 第四阶段：撰写分析报告（2-3天）
1. 数据描述性统计
2. 可视化结果解读
3. 结论与建议

## 数据源详细说明

### 推荐数据源（按优先级排序）

#### 🌟 优先级1：深圳市政府数据开放平台
- **网址**: https://opendata.sz.gov.cn/
- **包含内容**:
  - 公共交通线路数据
  - 地铁客流数据
  - 道路交通数据
  - 出租车GPS轨迹（可能需要申请）

#### 🌟 优先级2：高德地图开放平台
- **网址**: https://lbs.amap.com/api/webservice/guide/api/trafficstatus
- **API服务**:
  - 交通态势API（实时路况）
  - 路径规划API（OD分析）
  - 地理编码API
- **注意**: 需要注册账号，个人开发者每天有免费调用额度

#### 🌟 优先级3：开源数据集
- **GitHub**: 搜索 "Shenzhen traffic data" 或 "深圳交通数据"
- **Kaggle**: 搜索 "China traffic" 或使用国际数据集作为方法参考
- **百度地图慧眼**: https://huiyan.baidu.com/ （需要企业认证）

#### 备选数据源
- 滴滴盖亚数据开放平台：https://gaia.didichuxing.com/
- 交通运输部数据开放：https://www.mot.gov.cn/
- OpenStreetMap深圳路网数据：https://www.openstreetmap.org/

### 数据说明
如果官方API受限，本项目将：
1. 使用模拟数据（基于真实数据分布特征）
2. 使用历史公开数据集
3. 使用其他城市数据作为演示（方法论相同）

## 技术栈
- Python 3.8+
- 数据处理：pandas, numpy
- 可视化：matplotlib, seaborn, plotly, folium
- 地图可视化：folium, geopandas
- 统计分析：scipy, statsmodels

## 项目结构
```
Final/
├── README.md                    # 项目说明
├── requirements.txt             # 依赖包
├── data/                        # 数据目录
│   ├── raw/                     # 原始数据
│   ├── processed/               # 处理后的数据
│   └── sample/                  # 示例数据
├── notebooks/                   # Jupyter笔记本
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_visualization.ipynb
├── src/                         # 源代码
│   ├── data_loader.py           # 数据加载
│   ├── data_processor.py        # 数据处理
│   └── visualizer.py            # 可视化函数
├── outputs/                     # 输出结果
│   ├── figures/                 # 图表
│   └── reports/                 # 分析报告
└── essay/                       # 论文部分
    └── traffic_analysis.md
```

## 开始使用
1. 安装依赖：`pip install -r requirements.txt`
2. 运行数据收集脚本
3. 执行可视化笔记本
4. 查看生成的图表和分析结果

