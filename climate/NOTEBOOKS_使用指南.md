# 气候数据可视化 Jupyter Notebooks 使用指南

## 📚 文件说明

本目录包含四个独立的Jupyter Notebook文件，按主题分类整理了所有气候可视化图表：

### 1. 📈 气候_温度分析.ipynb
**包含图表**: 5个温度相关图表
- 图表1: 全球温度长期趋势线图 (1750-2015)
- 图表2: 国家温度热力图 (TOP25升温最快国家)
- 图表3: 纬度带温度分布（小提琴图）
- 图表4: 全球区域温度演变对比
- 图表5: 主要城市温度箱线图

**数据需求**: 
- `data/raw/GlobalTemperatures.csv`
- `data/raw/GlobalLandTemperaturesByCountry.csv`
- `data/raw/GlobalLandTemperaturesByMajorCity.csv`

### 2. 🏭 气候_CO2排放分析.ipynb
**包含图表**: 4个CO₂排放图表
- 图表1: CO₂排放时间序列
- 图表2: CO₂与温度因果关系（散点回归）
- 图表3: 人均CO₂ vs 总排放（JointPlot）
- 图表4: CO₂与温度关系（Hex Density）

**数据需求**: 
- `data/raw/GlobalTemperatures.csv`
- `data/raw/co2/` （CO₂排放数据）

### 3. 🌊 气候_海平面分析.ipynb
**包含图表**: 2个海平面图表
- 图表1: 海平面上升趋势
- 图表2: 海平面与温度的同步上升（双轴图）

**数据需求**: 
- `data/raw/GlobalTemperatures.csv`
- `data/raw/sea_level/` （海平面数据）

### 4. 🔗 气候_综合分析.ipynb
**包含图表**: 1个综合相关性图表
- 图表1: 多变量相关性矩阵（PairPlot）

**数据需求**: 
- `data/raw/GlobalTemperatures.csv`
- `data/raw/co2/` （CO₂排放数据）
- `data/raw/sea_level/` （海平面数据）

**总计**: 12个精选图表

## 🚀 快速开始

### ✅ Kernel已配置完成

所有notebook已配置好运行环境（kernel名称：**DV Final Project**），可以直接使用。

### 方法一：使用Jupyter Notebook

```bash
# 1. 启动Jupyter Notebook
cd /Users/haoyin/Documents/大三上/数据可视化/Final/climate
jupyter notebook

# 2. 在浏览器中打开想要查看的notebook文件
# 3. Kernel会自动使用"DV Final Project"（项目虚拟环境）
```

### 方法二：使用VS Code

```bash
# 1. 安装VS Code的Jupyter扩展
# 2. 直接在VS Code中打开.ipynb文件
# 3. 右上角选择kernel："DV Final Project"
# 4. 点击"Run All"运行所有单元格
```

### 方法三：使用JupyterLab

```bash
# 1. 启动JupyterLab
cd /Users/haoyin/Documents/大三上/数据可视化/Final/climate
jupyter lab

# 2. 在界面中选择要打开的notebook
# 3. Kernel会自动使用"DV Final Project"
```

## 💡 使用技巧

### 实时修改和查看
1. **修改参数**: 每个图表都是独立的code cell，可以直接修改代码参数
2. **重新运行**: 修改后按 `Shift+Enter` 重新运行当前cell
3. **保存图片**: 每个图表运行后会自动保存到 `output/notebook_figures/` 目录

### 调整图表大小
```python
# 在绘图代码中找到 figsize参数，修改即可
fig, ax = plt.subplots(figsize=(16, 7))  # 修改这两个数字
```

### 修改配色
```python
# 修改颜色变量，可选：
# - MAGMA_COLORS: 紫红橙色系
# - VIRIDIS_COLORS: 蓝绿黄色系
# - MAKO_COLORS: 深蓝绿色系
# - ROCKET_COLORS: 深紫橙色系
```

### 添加新图表
1. 在notebook末尾插入新cell
2. 复制现有图表代码作为模板
3. 修改数据处理和绘图逻辑
4. 添加中文注释说明

## 📊 图表输出

所有图表运行后会自动保存到：
```
climate/output/notebook_figures/
├── 温度_01_全球趋势.png
├── 温度_ 02_国家热力图.png
├── 温度_03_纬度分布.png
├── CO2_01_排放趋势.png
├── CO2_02_温度相关性.png
├── CO2_03_人均vs总量.png
├── 海平面_01_上升趋势.png
└── 海平面_02_与温度关系.png
```

## 🔧 环境要求

```bash
# 必需的Python库
pip install jupyter
pip install matplotlib
pip install seaborn
pip install pandas
pip install numpy
pip install scipy

# 或使用requirements.txt
pip install -r ../requirements.txt
```

## ⚠️ 常见问题

### 1. 中文显示问题
如果遇到中文显示为方块，请检查：
- MacBook系统字体是否正常
- 运行环境设置cell，查看字体设置是否正确

### 2. 数据文件未找到
确保数据文件位于正确路径：
```
climate/data/raw/
├── GlobalTemperatures.csv
├── GlobalLandTemperaturesByCountry.csv
├── GlobalLandTemperaturesByMajorCity.csv
├── co2/ (可选)
└── sea_level/ (可选)
```

### 3. CO₂或海平面数据缺失
- CO₂和海平面数据是可选的
- 如果数据不存在，相关图表会自动跳过
- 不影响温度分析notebook的使用

### 4. 图表显示不完整
```python
# 在cell开头添加：
%matplotlib inline
# 或者使用交互式显示：
%matplotlib widget
```

## 📝 修改建议

### 自定义图表标题
```python
ax.set_title('你的自定义标题', fontsize=15, weight='bold', pad=15)
```

### 调整坐标轴标签
```python
ax.set_xlabel('X轴标签', fontsize=13, weight='bold')
ax.set_ylabel('Y轴标签', fontsize=13, weight='bold')
```

### 更改保存路径
```python
plt.savefig('你的路径/文件名.png', dpi=300, bbox_inches='tight')
```

## 🎯 下一步操作

1. **测试运行**: 打开每个notebook，依次运行所有cells
2. **调整参数**: 根据需要修改图表参数和样式
3. **添加分析**: 在图表下方添加markdown cell写分析说明
4. **导出报告**: 使用 `File > Download as > HTML/PDF` 导出完整报告

## 📞 技术支持

如有问题，请检查：
1. `code/data_loader.py` - 数据加载模块
2. `code/visualizer.py` - 原始可视化代码
3. 项目根目录的 `README.md`

---

**最后更新**: 2025-12-16  
**作者**: 数据可视化课程项目
