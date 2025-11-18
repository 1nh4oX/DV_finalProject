# 气候数据说明

## 📥 数据下载

### Kaggle 数据集
**Berkeley Earth Climate Change: Earth Surface Temperature Data**

**下载地址**: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

### 下载步骤

1. **登录 Kaggle**
   - 访问 https://www.kaggle.com/
   - 如果没有账号，先注册

2. **下载数据集**
   - 访问数据集页面
   - 点击右上角 "Download" 按钮
   - 下载 ZIP 文件（约 300MB）

3. **解压文件**
   ```bash
   # 解压到 raw 文件夹
   unzip archive.zip -d raw/
   ```

---

## 📊 数据集文件

### 1. GlobalTemperatures.csv
- **内容**: 全球月度平均温度
- **时间跨度**: 1750-2015
- **字段**:
  - dt: 日期
  - LandAverageTemperature: 陆地平均温度
  - LandAverageTemperatureUncertainty: 不确定性
  - LandMaxTemperature: 最高温度
  - LandMinTemperature: 最低温度
  - LandAndOceanAverageTemperature: 陆地和海洋平均温度

### 2. GlobalLandTemperaturesByCity.csv
- **内容**: 城市月度温度
- **记录数**: 8M+
- **字段**:
  - dt: 日期
  - AverageTemperature: 平均温度
  - AverageTemperatureUncertainty: 不确定性
  - City: 城市名称
  - Country: 国家
  - Latitude: 纬度
  - Longitude: 经度

### 3. GlobalLandTemperaturesByCountry.csv
- **内容**: 国家月度温度
- **记录数**: 500K+
- **字段**:
  - dt: 日期
  - AverageTemperature: 平均温度
  - AverageTemperatureUncertainty: 不确定性
  - Country: 国家

### 4. GlobalLandTemperaturesByMajorCity.csv
- **内容**: 主要城市月度温度
- **记录数**: 200K+
- **字段**: 同 GlobalLandTemperaturesByCity.csv

### 5. GlobalLandTemperaturesByState.csv
- **内容**: 州/省月度温度
- **记录数**: 600K+
- **字段**:
  - dt: 日期
  - AverageTemperature: 平均温度
  - AverageTemperatureUncertainty: 不确定性
  - State: 州/省
  - Country: 国家

---

## 📁 数据存放

```
data/
├── raw/                                    # 原始数据
│   ├── GlobalTemperatures.csv
│   ├── GlobalLandTemperaturesByCity.csv
│   ├── GlobalLandTemperaturesByCountry.csv
│   ├── GlobalLandTemperaturesByState.csv
│   └── GlobalLandTemperaturesByMajorCity.csv
└── processed/                              # 处理后的数据
    ├── global_temp_yearly.csv             # 年度数据
    ├── country_temp_recent.csv            # 最近数据
    └── city_temp_with_coords.csv          # 带坐标的城市数据
```

---

## 🔍 数据质量

### 优点
- 时间跨度长（265年）
- 地理覆盖广（全球）
- 数据来源权威（Berkeley Earth）
- 包含不确定性估计

### 注意事项
- 早期数据（1750-1850）不确定性较大
- 部分城市数据有缺失
- 需要处理缺失值和异常值

---

## 🚀 使用建议

### 推荐使用的数据文件：

1. **全球趋势分析** → `GlobalTemperatures.csv`
2. **国家对比** → `GlobalLandTemperaturesByCountry.csv`
3. **城市地理可视化** → `GlobalLandTemperaturesByMajorCity.csv`

### 数据处理建议：

1. 过滤最近100年数据（1915-2015）- 数据质量更好
2. 只使用不确定性 < 2°C 的数据
3. 按年份聚合，减少数据量
4. 使用移动平均平滑数据

---

## 📝 快速开始

```python
import pandas as pd

# 加载全球温度数据
df_global = pd.read_csv('raw/GlobalTemperatures.csv')

# 加载城市数据
df_city = pd.read_csv('raw/GlobalLandTemperaturesByMajorCity.csv')

# 查看数据
print(df_global.head())
print(df_city.head())
```

