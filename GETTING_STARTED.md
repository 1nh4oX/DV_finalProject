# 🚀 快速上手指南

## 项目概览

本项目包含两个独立的数据可视化模块：
1. **Climate** - 全球气候变化分析 🌍
2. **Traffic** - 深圳交通模式分析 🚗

---

## 📦 第一步：环境准备

### 激活虚拟环境
```bash
cd /Users/haoyin/Documents/大三上/数据可视化/Final
source venv/bin/activate
```

### 验证环境
```bash
python --version  # 应该显示 Python 3.9+
pip list | grep pandas  # 检查是否安装了依赖
```

---

## 🌍 第二步：使用Climate模块

### 2.1 下载数据

**Kaggle数据集**：Berkeley Earth Climate Change Data

**下载步骤**：

1. **访问Kaggle**
   ```
   https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
   ```

2. **登录账号**
   - 如果没有账号，需要先注册
   - 可以用Google账号快速登录

3. **下载数据**
   - 点击页面右上角的 "Download" 按钮
   - 下载 `archive.zip`（约300MB）

4. **解压数据**
   ```bash
   cd climate/data
   # 将下载的archive.zip移动到这里
   unzip archive.zip -d raw/
   ```

5. **验证数据**
   ```bash
   ls -lh climate/data/raw/
   # 应该看到：
   # GlobalTemperatures.csv
   # GlobalLandTemperaturesByCity.csv
   # GlobalLandTemperaturesByCountry.csv
   # GlobalLandTemperaturesByMajorCity.csv
   # GlobalLandTemperaturesByState.csv
   ```

### 2.2 运行Climate分析

```bash
cd climate/code
python main.py
```

**预期输出**：
```
======================================================================
  全球气候变化数据分析系统
  Global Climate Change Data Analysis System
======================================================================

📊 第一步：检查数据集...
----------------------------------------------------------------------
✓ 全球温度              - GlobalTemperatures.csv                      (8.59 MB)
✓ 城市温度（全部）      - GlobalLandTemperaturesByCity.csv           (308.57 MB)
✓ 主要城市温度          - GlobalLandTemperaturesByMajorCity.csv      (23.19 MB)
✓ 国家温度              - GlobalLandTemperaturesByCountry.csv        (23.69 MB)
✓ 州/省温度             - GlobalLandTemperaturesByState.csv          (44.80 MB)

📥 第二步：加载数据...
...
🎨 第四步：生成可视化图表...
...
✅ 所有图表生成完成！
```

### 2.3 查看Climate图表

```bash
# 在Finder中打开
open climate/output/figures/

# 或者用预览打开某个图表
open climate/output/figures/01_global_temperature_trend.png
```

**生成的图表**：
1. `01_global_temperature_trend.png` - 全球温度趋势
2. `02_country_temperature_comparison.png` - 国家温度对比
3. `03_city_temperature_map.html` - 城市温度地图（交互式）⭐
4. `04_seasonal_heatmap.png` - 季节性热力图
5. `05_temperature_distribution.png` - 温度分布

---

## 🚗 第三步：使用Traffic模块

### 3.1 运行Traffic分析

**无需下载数据**，数据会自动生成！

```bash
cd traffic/code
python main.py
```

**预期输出**：
```
======================================================================
  深圳城市交通与出行模式分析系统
  Shenzhen Traffic and Travel Pattern Analysis System
======================================================================

📊 第一步：生成模拟数据...
----------------------------------------------------------------------
✓ hourly_traffic: 720 条记录
✓ road_congestion: 772 条记录
✓ metro_ridership: 330 条记录
...

🎨 第二步：生成可视化图表...
----------------------------------------------------------------------
正在绘制：高峰时段折线图...
✓ 已保存：01_peak_hours_line.png
...
✅ 所有图表生成完成！
```

### 3.2 查看Traffic图表

```bash
# 在Finder中打开
open traffic/output/figures/

# 交互式图表
open traffic/output/figures/11_street_traffic_hexbin_interactive.html
```

**生成的图表**（11张）：
1. 高峰时段折线图
2. 路段拥堵热力图
3. 地铁客流箱线图
4. OD路径流向图
5. TOP10拥堵道路
6. 出行方式饼图
7. 天气vs拥堵
8. 工作日vs周末对比
9. 出行次数直方图
10. 速度分布核密度图
11. 街道流量六边形热力图 ⭐

---

## 📊 第四步：分析图表

### Climate图表重点

1. **全球温度趋势** → 看温度上升趋势和速率
2. **国家对比** → 找出升温最快的国家
3. **城市地图** → 地理分布和热点区域
4. **季节性** → 月度温度变化模式

### Traffic图表重点

1. **高峰时段** → 早晚高峰特征
2. **拥堵热力图** → 拥堵区域分布
3. **工作日vs周末** → 出行模式差异
4. **六边形热力图** → 街道流量空间分布

---

## 📝 第五步：撰写报告

### 报告结构建议

```
1. 引言
   - 研究背景
   - 研究目的
   - 数据来源

2. 数据说明
   - 数据集描述
   - 数据处理方法
   - 数据质量

3. 可视化展示
   - 图表1 + 分析
   - 图表2 + 分析
   - ...

4. 结论
   - 主要发现
   - 规律总结
   - 建议

5. 参考文献
```

### 报告模板

参考：`essay/analysis_report_template.md`

---

## 🎯 常见问题

### Q1: Kaggle下载慢怎么办？
**A**: 可以尝试：
- 使用VPN
- 换个时间段下载
- 使用Kaggle CLI工具

### Q2: 生成图表后中文显示乱码？
**A**: 项目已配置MacBook字体（STHeiti），如果仍有问题：
```bash
# 清除matplotlib缓存
rm -rf ~/.matplotlib/fontlist-*.json
rm -rf ~/.cache/matplotlib

# 重新运行
python main.py
```

### Q3: 如何只生成某个图表？
**A**: 修改main.py，注释掉不需要的图表：
```python
# 在 visualizer.generate_all_visualizations() 中
# 注释掉不需要的图表函数
```

### Q4: 如何修改图表样式？
**A**: 编辑 `code/visualizer.py`，修改：
- 颜色方案
- 字体大小
- 图表尺寸
- 标题文字

### Q5: 如何导出分析数据？
**A**: 在数据处理后添加导出代码：
```python
# 在 main.py 中添加
df_processed.to_csv('../data/processed/processed_data.csv', index=False)
```

---

## 🔧 高级使用

### 自定义Climate分析

编辑 `climate/code/visualizer.py`，添加新图表：

```python
def plot_custom_analysis(self, df):
    """自定义分析"""
    # 你的代码...
    plt.savefig(self.output_dir / 'custom_plot.png')
```

### 自定义Traffic分析

编辑 `traffic/code/visualizer.py`，修改现有图表或添加新图表。

---

## 📚 参考资料

### 项目文档
- `README.md` - 项目总说明
- `PROJECT_STRUCTURE.md` - 项目结构
- `DATA_SUMMARY.md` - 数据说明
- `KAGGLE_DATASET_RECOMMENDATIONS.md` - 数据集推荐

### 数据集文档
- [Berkeley Earth](http://berkeleyearth.org/data/)
- [Kaggle Dataset Page](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)

### 可视化文档
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Plotly](https://plotly.com/python/)

---

## ✅ 检查清单

完成以下步骤后，你就可以开始分析了：

- [ ] 激活虚拟环境
- [ ] 从Kaggle下载Climate数据
- [ ] 解压数据到 `climate/data/raw/`
- [ ] 运行 Climate 分析
- [ ] 运行 Traffic 分析
- [ ] 查看所有生成的图表
- [ ] 分析图表，记录发现
- [ ] 撰写分析报告

---

**准备好了吗？开始你的数据分析之旅！** 🎉

如有问题，请查看各模块的 README 文件。

