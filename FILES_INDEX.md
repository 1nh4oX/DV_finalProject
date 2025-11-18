# 📂 项目文件索引

## 📖 文档文件（必读）

### 🌟 核心文档
| 文件名 | 用途 | 优先级 |
|--------|------|--------|
| **README.md** | 项目总览、实验步骤规划 | ⭐⭐⭐⭐⭐ |
| **QUICK_START.md** | 快速开始指南，3步开始 | ⭐⭐⭐⭐⭐ |
| **PROJECT_SUMMARY.md** | 完整项目总结，所有信息汇总 | ⭐⭐⭐⭐⭐ |
| **DATA_SOURCE_GUIDE.md** | 深圳交通数据获取完整指南 | ⭐⭐⭐⭐⭐ |

### 🔧 辅助文档
| 文件名 | 用途 | 优先级 |
|--------|------|--------|
| **INSTALL.md** | 环境安装详细说明 | ⭐⭐⭐⭐ |
| **FILES_INDEX.md** | 本文件，文件索引 | ⭐⭐⭐ |
| **requirements.txt** | Python依赖包列表 | ⭐⭐⭐⭐ |

---

## 💻 代码文件

### 主程序
| 文件名 | 功能 | 代码行数 | 优先级 |
|--------|------|----------|--------|
| **main.py** | 主程序入口，一键运行 | ~50 | ⭐⭐⭐⭐⭐ |

### 核心模块
| 文件路径 | 功能 | 代码行数 | 优先级 |
|----------|------|----------|--------|
| **src/data_generator.py** | 交通数据生成器 | ~350 | ⭐⭐⭐⭐⭐ |
| **src/visualizer.py** | 10种可视化图表生成 | ~700 | ⭐⭐⭐⭐⭐ |
| **src/amap_api_example.py** | 高德API使用示例 | ~400 | ⭐⭐⭐⭐ |

### 其他模块（待创建）
| 文件路径 | 功能 | 状态 |
|----------|------|------|
| src/data_processor.py | 数据预处理和清洗 | 可选 |
| src/data_loader.py | 数据加载工具 | 可选 |

---

## 📊 数据目录

### data/sample/ - 生成的样本数据
运行 `main.py` 后会生成以下9个CSV文件：

| 文件名 | 内容 | 记录数 | 对应图表 |
|--------|------|--------|----------|
| **hourly_traffic.csv** | 每小时交通流量 | ~720 | 图1, 图8 |
| **road_congestion.csv** | 路段拥堵数据 | ~1000+ | 图2 |
| **metro_ridership.csv** | 地铁客流数据 | ~330 | 图3 |
| **od_flow.csv** | OD流动数据 | ~500 | 图4 |
| **top_congested_roads.csv** | TOP10拥堵道路 | 10 | 图5 |
| **travel_mode_share.csv** | 出行方式占比 | 6 | 图6 |
| **weather_traffic.csv** | 天气与交通 | ~90 | 图7 |
| **daily_trips.csv** | 每日出行次数 | ~60 | 图8, 图9 |
| **speed_distribution.csv** | 速度分布 | ~10000 | 图10 |

### data/raw/ - 原始数据（如使用真实API）
放置从高德API等采集的原始数据

### data/processed/ - 处理后的数据
放置清洗和处理后的数据

---

## 🎨 输出文件

### outputs/figures/ - 可视化图表
运行后会生成以下文件：

#### 静态图表（PNG格式，300 DPI）
| 文件名 | 图表类型 | 分辨率 |
|--------|----------|--------|
| **01_peak_hours_line.png** | 高峰时段折线图 | 高清 |
| **02_congestion_heatmap.png** | 拥堵热力图（静态版） | 高清 |
| **03_metro_boxplot.png** | 地铁客流箱线图 | 高清 |
| **04_od_flow_matrix.png** | OD流量矩阵热力图 | 高清 |
| **05_top_congested_roads.png** | TOP10拥堵道路条形图 | 高清 |
| **06_travel_mode_pie.png** | 出行方式饼图 | 高清 |
| **07_weather_vs_congestion.png** | 天气vs拥堵散点图 | 高清 |
| **08_weekday_vs_weekend.png** | 工作日vs周末对比 | 高清 |
| **09_daily_trips_histogram.png** | 出行次数直方图 | 高清 |
| **10_speed_kde.png** | 速度核密度图 | 高清 |

#### 交互式图表（HTML格式）
| 文件名 | 图表类型 | 特点 |
|--------|----------|------|
| **02_congestion_heatmap.html** | 交互式热力图 | 可缩放、悬停查看 |
| **04_od_flow_sankey.html** | 桑基图 | 可交互、动态展示 |
| **06_travel_mode_interactive.html** | 旭日图 | 交互式占比 |

### outputs/reports/ - 分析报告
存放自动生成的分析报告（可选功能）

---

## 📝 论文相关

### essay/ - 论文和报告
| 文件名 | 内容 | 字数 | 状态 |
|--------|------|------|------|
| **analysis_report_template.md** | 完整分析报告模板 | ~8000字 | ✅ 已完成 |

---

## 📔 Jupyter笔记本（可选）

### notebooks/ - 交互式分析
| 文件名 | 用途 | 状态 |
|--------|------|------|
| 01_data_collection.ipynb | 数据采集流程 | 待创建 |
| 02_data_cleaning.ipynb | 数据清洗过程 | 待创建 |
| 03_visualization.ipynb | 可视化展示 | 待创建 |

**说明**：这些笔记本是可选的，如果您更习惯Jupyter环境，可以创建使用。

---

## 🗂️ 完整目录树

```
Final/
│
├── 📖 文档类
│   ├── README.md                          ⭐⭐⭐⭐⭐
│   ├── QUICK_START.md                     ⭐⭐⭐⭐⭐
│   ├── PROJECT_SUMMARY.md                 ⭐⭐⭐⭐⭐
│   ├── DATA_SOURCE_GUIDE.md              ⭐⭐⭐⭐⭐
│   ├── INSTALL.md                         ⭐⭐⭐⭐
│   ├── FILES_INDEX.md                     (本文件)
│   └── requirements.txt
│
├── 💻 代码类
│   ├── main.py                            ⭐⭐⭐⭐⭐
│   └── src/
│       ├── data_generator.py              ⭐⭐⭐⭐⭐
│       ├── visualizer.py                  ⭐⭐⭐⭐⭐
│       ├── amap_api_example.py            ⭐⭐⭐⭐
│       ├── data_processor.py              (可选)
│       └── data_loader.py                 (可选)
│
├── 📊 数据类
│   └── data/
│       ├── raw/                           (原始数据)
│       ├── processed/                     (处理后)
│       └── sample/                        (生成的数据)
│           ├── hourly_traffic.csv
│           ├── road_congestion.csv
│           ├── metro_ridership.csv
│           ├── od_flow.csv
│           ├── top_congested_roads.csv
│           ├── travel_mode_share.csv
│           ├── weather_traffic.csv
│           ├── daily_trips.csv
│           └── speed_distribution.csv
│
├── 🎨 输出类
│   └── outputs/
│       ├── figures/                       (图表)
│       │   ├── 01_peak_hours_line.png
│       │   ├── 02_congestion_heatmap.png/html
│       │   ├── 03_metro_boxplot.png
│       │   ├── 04_od_flow_*.png/html
│       │   ├── 05_top_congested_roads.png
│       │   ├── 06_travel_mode_*.png/html
│       │   ├── 07_weather_vs_congestion.png
│       │   ├── 08_weekday_vs_weekend.png
│       │   ├── 09_daily_trips_histogram.png
│       │   └── 10_speed_kde.png
│       └── reports/                       (报告)
│
├── 📝 论文类
│   └── essay/
│       └── analysis_report_template.md    ⭐⭐⭐⭐⭐
│
└── 📔 笔记本类 (可选)
    └── notebooks/
        ├── 01_data_collection.ipynb
        ├── 02_data_cleaning.ipynb
        └── 03_visualization.ipynb
```

---

## 🎯 使用流程

### 第一次使用
```
1. 阅读 README.md         (了解项目)
2. 阅读 QUICK_START.md    (快速开始)
3. 按照 INSTALL.md 安装   (环境配置)
4. 运行 main.py           (生成数据和图表)
5. 查看 outputs/figures/  (查看图表)
6. 参考 essay/模板        (撰写论文)
```

### 如需真实数据
```
1. 阅读 DATA_SOURCE_GUIDE.md  (详细指南)
2. 注册高德开放平台
3. 参考 src/amap_api_example.py
4. 采集真实数据
5. 替换或补充模拟数据
```

---

## 📏 文件大小估计

### 文档
- README.md: ~15 KB
- QUICK_START.md: ~12 KB  
- PROJECT_SUMMARY.md: ~30 KB
- DATA_SOURCE_GUIDE.md: ~25 KB
- 其他文档: ~5 KB
- **文档总计**: ~90 KB

### 代码
- main.py: ~2 KB
- data_generator.py: ~15 KB
- visualizer.py: ~30 KB
- amap_api_example.py: ~18 KB
- **代码总计**: ~65 KB

### 数据（生成后）
- 9个CSV文件: ~5-10 MB
- 取决于采样数量

### 图表（生成后）
- 10个PNG图（300 DPI）: ~30-50 MB
- 4个HTML交互图: ~2-5 MB
- **图表总计**: ~40-60 MB

### 项目总大小
- 初始（未运行）: ~0.2 MB
- 运行后: ~50-70 MB

---

## 🔍 文件用途速查

### 想快速开始？
→ 看 **QUICK_START.md**

### 想了解全貌？
→ 看 **PROJECT_SUMMARY.md**

### 想获取真实数据？
→ 看 **DATA_SOURCE_GUIDE.md**

### 想运行程序？
→ 运行 **main.py**

### 想看图表代码？
→ 看 **src/visualizer.py**

### 想修改数据？
→ 看 **src/data_generator.py**

### 想用高德API？
→ 看 **src/amap_api_example.py**

### 想写论文？
→ 看 **essay/analysis_report_template.md**

### 遇到问题？
→ 看 **INSTALL.md** 或 **PROJECT_SUMMARY.md** 的FAQ部分

---

## 📊 代码统计

### 代码量
- Python代码: ~1500行
- 文档: ~8000字
- 注释率: >30%

### 函数数量
- 数据生成函数: 9个
- 可视化函数: 10个
- API调用函数: 5个
- 工具函数: 若干

### 依赖包
- 核心依赖: 8个
- 可选依赖: 4个

---

## ✅ 文件检查清单

### 运行前检查
- [ ] README.md 存在
- [ ] QUICK_START.md 存在
- [ ] main.py 存在
- [ ] src/data_generator.py 存在
- [ ] src/visualizer.py 存在
- [ ] requirements.txt 存在
- [ ] 目录结构完整

### 运行后检查
- [ ] data/sample/ 下有9个CSV文件
- [ ] outputs/figures/ 下有10个PNG文件
- [ ] 部分HTML交互图生成
- [ ] 无错误信息

### 论文准备检查
- [ ] 所有图表已生成
- [ ] 图表清晰可读
- [ ] 数据来源已说明
- [ ] 分析报告已撰写
- [ ] 参考文献已添加

---

## 🚀 快速命令

### 查看文件列表
```bash
# 查看所有Python文件
find . -name "*.py"

# 查看所有文档
find . -name "*.md"

# 查看生成的数据
ls data/sample/

# 查看生成的图表
ls outputs/figures/
```

### 统计代码行数
```bash
# 统计Python代码行数
find . -name "*.py" | xargs wc -l

# 统计文档字数
find . -name "*.md" | xargs wc -w
```

### 清理生成文件
```bash
# 清理数据文件
rm -rf data/sample/*.csv

# 清理图表文件
rm -rf outputs/figures/*

# 重新生成
python3 main.py
```

---

## 📞 技术支持

### 文件相关问题
- **文件缺失**: 重新下载或生成
- **文件损坏**: 查看错误日志
- **编码问题**: 确保使用UTF-8编码

### 路径问题
- 使用相对路径时，确保从项目根目录运行
- 或使用绝对路径：`/Users/haoyin/Documents/大三上/数据可视化/Final/`

---

## 📝 更新日志

### Version 1.0 (2024-11-18)
- ✅ 完整项目结构
- ✅ 10种可视化图表
- ✅ 数据生成器
- ✅ 详细文档
- ✅ 高德API示例
- ✅ 论文模板

### 后续计划
- [ ] 添加Jupyter笔记本
- [ ] 添加更多数据源示例
- [ ] 添加自动报告生成
- [ ] 添加更多图表类型

---

## 💡 提示

1. **所有文档都很重要**，但如果时间紧，优先看标注⭐⭐⭐⭐⭐的
2. **代码有详细注释**，可以直接阅读学习
3. **遇到问题先看FAQ**，在PROJECT_SUMMARY.md中
4. **所有文件都可修改**，根据需要自定义
5. **记得保存原始文件**，修改前先备份

---

希望这个索引能帮助您快速找到需要的文件！

**祝使用愉快！** 🎉

