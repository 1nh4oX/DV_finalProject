# 🌊 NOAA G02135 海冰数据下载指南

## 📊 数据集信息

**NOAA G02135 - 海冰数据**
- **数据源**: NOAA/NSIDC
- **数据目录**: https://noaadata.apps.nsidc.org/NOAA/G02135/
- **包含内容**:
  - `north/` - 北极海冰数据
  - `south/` - 南极海冰数据
  - `seaice_analysis/` - 海冰分析数据

---

## 📥 下载方法

### 方法1：浏览器手动下载（推荐少量文件）

1. **访问数据目录**
   ```
   https://noaadata.apps.nsidc.org/NOAA/G02135/
   ```

2. **选择区域**
   - 点击 `north/` 下载北极数据
   - 点击 `south/` 下载南极数据
   - 点击 `seaice_analysis/` 下载分析数据

3. **下载文件**
   - 进入子文件夹后，点击所需文件链接下载
   - 文件通常按日期组织（如：`nt_YYYYMMDD_f17_v1.1_n.bin`）

---

### 方法2：命令行批量下载（推荐大量文件）

#### 使用 wget（Linux/Mac）

```bash
# 下载北极海冰数据
cd climate/data/raw/sea_ice/
wget -r -np -nH --cut-dirs=2 -R "index.html*" \
  https://noaadata.apps.nsidc.org/NOAA/G02135/north/

# 下载南极海冰数据
wget -r -np -nH --cut-dirs=2 -R "index.html*" \
  https://noaadata.apps.nsidc.org/NOAA/G02135/south/

# 下载海冰分析数据
wget -r -np -nH --cut-dirs=2 -R "index.html*" \
  https://noaadata.apps.nsidc.org/NOAA/G02135/seaice_analysis/
```

**参数说明**：
- `-r`: 递归下载
- `-np`: 不创建父目录
- `-nH`: 不创建主机目录
- `--cut-dirs=2`: 跳过2层目录结构
- `-R "index.html*"`: 排除索引页面

#### 使用 curl（Mac/Linux）

```bash
# 下载单个文件示例
curl -O https://noaadata.apps.nsidc.org/NOAA/G02135/north/nt_20240101_f17_v1.1_n.bin

# 批量下载（需要先获取文件列表）
```

#### 使用 Python 脚本（推荐）

我已经创建了下载脚本，见下方。

---

## 🐍 Python 下载脚本

### 创建下载脚本

```python
# climate/code/download_sea_ice.py
import os
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse

def download_sea_ice_data(region='north', output_dir='../data/raw/sea_ice'):
    """
    下载NOAA G02135海冰数据
    
    Args:
        region: 'north' (北极) 或 'south' (南极) 或 'seaice_analysis'
        output_dir: 输出目录
    """
    base_url = 'https://noaadata.apps.nsidc.org/NOAA/G02135/'
    region_url = urljoin(base_url, f'{region}/')
    
    output_path = Path(output_dir) / region
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"正在下载 {region} 海冰数据...")
    print(f"输出目录: {output_path}")
    
    # 注意：这需要先获取文件列表
    # 实际使用时，建议使用 wget 或手动下载
    print("⚠️  建议使用 wget 命令批量下载")
    print(f"   命令: wget -r -np -nH --cut-dirs=2 -R 'index.html*' {region_url}")
```

---

## 📁 数据存放位置

下载后，将数据放到以下位置：

```
climate/data/raw/sea_ice/
├── north/          # 北极海冰数据
├── south/          # 南极海冰数据
└── seaice_analysis/ # 海冰分析数据
```

---

## 🔧 数据处理

### 数据格式

NOAA G02135 数据通常是：
- **二进制格式** (`.bin`): 需要特殊工具读取
- **NetCDF格式** (`.nc`): 可用 Python 的 `netCDF4` 或 `xarray` 读取
- **CSV格式**: 可直接用 pandas 读取

### 推荐处理工具

1. **NetCDF 文件**:
   ```python
   import xarray as xr
   ds = xr.open_dataset('sea_ice_file.nc')
   ```

2. **二进制文件**:
   - 需要参考 NOAA 文档了解数据格式
   - 可能需要使用专门的解码工具

---

## 📊 数据使用建议

### 如果数据是二进制格式

1. **查找数据说明文档**
   - 访问 NSIDC 网站获取数据格式说明
   - 查找数据读取工具

2. **使用预处理工具**
   - NOAA 可能提供数据转换工具
   - 或查找第三方转换脚本

### 如果数据是 NetCDF 格式

```python
import xarray as xr
import pandas as pd

# 读取 NetCDF 文件
ds = xr.open_dataset('sea_ice_file.nc')

# 转换为 DataFrame
df = ds.to_dataframe().reset_index()

# 保存为 CSV（便于后续使用）
df.to_csv('sea_ice_data.csv', index=False)
```

---

## 🎯 快速开始

### 最简单的方法（推荐）

1. **使用 wget 下载**:
   ```bash
   cd climate/data/raw/
   mkdir -p sea_ice/north sea_ice/south
   
   # 下载北极数据（示例：最近一年的数据）
   cd sea_ice/north
   wget -r -np -nH --cut-dirs=2 -R "index.html*" \
     https://noaadata.apps.nsidc.org/NOAA/G02135/north/
   ```

2. **检查下载的文件**:
   ```bash
   ls -lh climate/data/raw/sea_ice/north/
   ```

3. **如果文件是二进制格式，查找转换工具或文档**

---

## ⚠️ 注意事项

1. **数据量大**: 完整数据集可能很大（GB级别），建议先下载少量数据测试

2. **数据格式**: 确认数据格式（二进制/NetCDF/CSV），不同格式需要不同的处理方式

3. **网络稳定**: 批量下载时确保网络连接稳定

4. **存储空间**: 确保有足够的磁盘空间

5. **使用许可**: 下载前请查看数据使用许可

---

## 🔗 相关链接

- **NSIDC G02135 数据集页面**: http://nsidc.org/collections/G02135
- **数据目录**: https://noaadata.apps.nsidc.org/NOAA/G02135/
- **文档和工具**: 查看 NSIDC 网站获取数据格式说明和工具

---

## 💡 建议

如果数据格式复杂（二进制），建议：

1. **先下载少量样本文件**测试
2. **查找数据格式文档**或示例代码
3. **考虑使用预处理后的数据**（如果有CSV版本）
4. **或查找Kaggle上已处理好的数据集**

