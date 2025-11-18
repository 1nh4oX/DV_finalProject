# 🗂️ 深圳交通数据获取完整指南

## 📊 数据源概览对比

| 数据源 | 难度 | 时间 | 质量 | 费用 | 推荐度 |
|--------|------|------|------|------|--------|
| 高德开放平台 | ⭐⭐ | 1天 | ⭐⭐⭐⭐⭐ | 免费* | ⭐⭐⭐⭐⭐ |
| 深圳政府平台 | ⭐⭐⭐ | 1-2周 | ⭐⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐ |
| 百度慧眼 | ⭐⭐⭐⭐ | 1-2周 | ⭐⭐⭐⭐⭐ | 收费 | ⭐⭐⭐ |
| 网络爬虫 | ⭐⭐⭐⭐ | 3-5天 | ⭐⭐⭐ | 免费 | ⭐⭐⭐ |
| Kaggle数据集 | ⭐ | 1小时 | ⭐⭐⭐ | 免费 | ⭐⭐⭐⭐ |

*高德免费配额：个人开发者每天5000-30000次

---

## 🌟 方案一：高德地图开放平台（最推荐）

### 优点
✅ 注册简单快速（10分钟）
✅ 数据实时准确
✅ API文档完善
✅ 免费配额充足
✅ 适合学术项目

### 详细步骤

#### 第1步：注册账号
1. 访问：https://lbs.amap.com/
2. 点击右上角"注册/登录"
3. 使用手机号注册（支持微信登录）

#### 第2步：创建应用
1. 登录后进入"控制台"
2. 点击"应用管理" → "我的应用"
3. 点击"创建新应用"
4. 填写：
   - 应用名称：深圳交通分析
   - 应用类型：Web服务

#### 第3步：添加Key
1. 在应用下点击"添加Key"
2. Key名称：traffic_api
3. 服务平台：Web服务
4. 提交并获得Key

#### 第4步：获取数据

**A. 实时路况数据**
```python
import requests

key = '你的API_KEY'
url = 'https://restapi.amap.com/v3/traffic/status/rectangle'

# 深圳市区范围（矩形）
params = {
    'key': key,
    'rectangle': '113.75,22.4;114.62,22.86',  # 深圳市边界
    'extensions': 'all',  # 返回详细信息
    'output': 'json'
}

response = requests.get(url, params=params)
data = response.json()

# 解析数据
if data['status'] == '1':
    roads = data['trafficinfo']['roads']
    for road in roads:
        print(f"道路: {road['name']}")
        print(f"拥堵指数: {road['status']}")  # 0-畅通, 1-缓行, 2-拥堵, 3-严重拥堵
        print(f"速度: {road['speed']} km/h")
```

**B. 路径规划（用于OD分析）**
```python
url = 'https://restapi.amap.com/v3/direction/driving'

params = {
    'key': key,
    'origin': '114.057868,22.543099',  # 起点：市民中心
    'destination': '113.953066,22.542907',  # 终点：科技园
    'extensions': 'all',
    'strategy': 10  # 0-速度优先, 10-不走高速
}

response = requests.get(url, params=params)
route_data = response.json()
```

**C. 地理编码（道路名称→坐标）**
```python
url = 'https://restapi.amap.com/v3/geocode/geo'

params = {
    'key': key,
    'address': '深圳市深南大道',
    'city': '深圳'
}

response = requests.get(url, params=params)
location_data = response.json()
```

#### 第5步：批量采集
```python
import time
import pandas as pd

# 深圳主要道路列表
roads = ['深南大道', '北环大道', '滨河大道', '滨海大道', ...]

data_list = []

for hour in range(24):
    for road in roads:
        # 调用API获取数据
        # ...
        data_list.append({
            'hour': hour,
            'road': road,
            'speed': speed,
            'status': status
        })
        
        time.sleep(0.1)  # 避免超过频率限制

df = pd.DataFrame(data_list)
df.to_csv('shenzhen_traffic_amap.csv', index=False)
```

### 配额说明
- **个人开发者**：
  - 交通态势API：10,000次/天
  - 路径规划API：5,000次/天
  - 地理编码API：30,000次/天

- **企业开发者**（认证后）：
  - 配额可提升至100,000+次/天

### 注意事项
⚠️ 不要频繁请求（建议间隔>0.1秒）
⚠️ 保管好API Key，不要泄露
⚠️ 遵守服务条款，不用于商业用途
⚠️ 学术使用需在论文中标注数据来源

---

## 🏛️ 方案二：深圳市政府数据开放平台

### 访问地址
https://opendata.sz.gov.cn/

### 可获取数据

#### 1. 公共交通数据
- **公交线路数据**
  - 路径：交通运输 → 公交线路
  - 内容：线路号、站点、首末班时间
  - 格式：CSV/JSON/XML
  - 更新：每月

- **地铁站点数据**
  - 路径：交通运输 → 轨道交通
  - 内容：站点名称、坐标、线路信息
  - 格式：CSV
  - 更新：每季度

#### 2. 道路网络数据
- 道路中心线数据
- 交叉路口数据
- 道路等级分类

#### 3. 交通运行数据（需申请）
- 出租车GPS轨迹
- 公交车GPS轨迹
- 道路流量数据

### 申请流程
1. 注册账号（实名认证）
2. 浏览数据目录
3. 免费数据可直接下载
4. 敏感数据需要申请（填写用途说明）
5. 审核通过后下载（1-2周）

### 使用示例
```python
# 下载后导入
import pandas as pd

# 公交线路数据
bus_routes = pd.read_csv('深圳市公交线路数据.csv', encoding='gbk')

# 地铁站点数据  
metro_stations = pd.read_csv('深圳市地铁站点.csv', encoding='gbk')

# 查看结构
print(bus_routes.head())
print(metro_stations.columns)
```

---

## 🚇 方案三：深圳地铁官网

### 数据来源
http://www.szmc.net/

### 可获取信息
- 线路图和站点信息
- 首末班车时刻表
- 客流统计（部分公开）
- 线网规划

### 获取方法

#### 方法1：官方开放数据
查找官网"数据公开"或"信息公开"栏目

#### 方法2：网页爬取
```python
import requests
from bs4 import BeautifulSoup

url = 'http://www.szmc.net/page/service/service.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 解析线路信息
lines = soup.find_all('div', class_='line-info')
# ...
```

⚠️ 注意：
- 遵守robots.txt协议
- 不要频繁请求
- 仅用于学术研究

---

## 🌤️ 方案四：气象数据

### 中国气象数据网
http://data.cma.cn/

### 获取步骤
1. 注册账号
2. 进入"数据"→"地面观测"→"中国地面气候资料日值数据集"
3. 选择深圳站（站号：59493）
4. 选择时间范围
5. 下载数据（部分收费，历史数据多为免费）

### 数据内容
- 日期
- 平均气温
- 最高/最低气温
- 降雨量
- 风速风向
- 湿度
- ...

---

## 📦 方案五：Kaggle公开数据集

### 推荐数据集

#### 1. Metro Interstate Traffic Volume
- **链接**: https://www.kaggle.com/datasets/anshtanwar/metro-interstate-traffic-volume
- **内容**: 明尼阿波利斯交通流量
- **可用性**: ⭐⭐⭐⭐⭐
- **说明**: 虽然是美国数据，但方法可参考

#### 2. Uber Movement Data
- **链接**: https://www.kaggle.com/datasets/uber/uber-movement-speeds-quarterly
- **内容**: Uber行程数据、速度数据
- **可用性**: ⭐⭐⭐⭐

#### 3. 中国城市交通数据（如有）
- 搜索关键词：
  - "China traffic"
  - "Shenzhen transportation"
  - "Chinese metro ridership"

### 使用方法
```python
# 下载后
import pandas as pd

traffic_data = pd.read_csv('Metro_Interstate_Traffic_Volume.csv')

# 分析时间模式（可参考用于深圳）
traffic_data['hour'] = pd.to_datetime(traffic_data['date_time']).dt.hour
hourly_pattern = traffic_data.groupby('hour')['traffic_volume'].mean()
```

---

## 🕷️ 方案六：网络爬虫

### 可爬取的数据源

#### 1. 交通新闻网站
- 深圳交通局官网新闻
- 深圳特区报交通新闻
- 提取拥堵路段、事件信息

#### 2. 社交媒体
- 微博交通话题
- 深圳交警官方微博
- 实时路况信息

#### 3. 第三方交通App
- 高德地图公开信息
- 百度地图路况
- ⚠️ 注意：不要爬取需要登录的数据

### 爬虫示例
```python
import requests
from bs4 import BeautifulSoup
import time

def crawl_traffic_news():
    url = 'http://www.sz.gov.cn/jtzx/'  # 示例URL
    headers = {
        'User-Agent': 'Mozilla/5.0 ...'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 解析内容
    articles = soup.find_all('div', class_='article')
    
    for article in articles:
        title = article.find('h3').text
        content = article.find('p').text
        # 保存数据
        
    time.sleep(2)  # 礼貌性延迟
```

### 法律与道德
⚠️ **重要提醒**：
- ✅ 遵守网站robots.txt
- ✅ 不要频繁请求（设置延迟）
- ✅ 仅用于学术研究
- ❌ 不要爬取敏感信息
- ❌ 不要用于商业用途
- ❌ 不要绕过验证码和登录

---

## 🔄 数据整合策略

### 组合方案（推荐）

```
方案A（最快）：
├── 高德API：实时路况、道路拥堵（1天）
├── 政府平台：公交地铁线路（1天）
├── 气象网站：天气数据（1天）
└── 总耗时：1-2天

方案B（最全）：
├── 高德API：实时数据采集（1周持续）
├── 政府平台：申请详细数据（2周）
├── 地铁官网：爬取客流信息（3天）
├── 气象数据：历史数据（1天）
└── 总耗时：2-3周

方案C（应急）：
├── Kaggle：国际数据集参考方法（1小时）
├── 本项目：使用模拟数据（立即）
└── 论文中说明："基于XX数据特征的模拟数据"
```

---

## 📝 论文中如何描述数据来源

### 场景1：使用真实API数据
```
本研究数据来源于高德地图开放平台交通态势API，采集时间为
2024年10月1日至10月31日，每小时采集一次深圳市主要道路的
实时交通状态，包括拥堵指数、平均速度等指标。地铁客流数据
来源于深圳市政府数据开放平台。气象数据来源于中国气象数据网
深圳站（站号59493）。

数据采集说明：
- 时间范围：2024年10月1-31日
- 采样频率：每小时
- 空间范围：深圳市全域主要道路
- 数据量：720条小时记录，覆盖20条主要道路
```

### 场景2：使用模拟数据
```
由于实时交通数据采集需要较长周期的API调用和数据积累，本研究
基于深圳市交通运行的统计特征生成了模拟数据集。模拟数据的生成
依据以下真实数据来源的统计规律：

1. 高德地图《2024年第三季度中国主要城市交通分析报告》中
   深圳市的高峰时段、平均速度等宏观统计特征
2. 深圳市交通运输局发布的《2023年深圳市综合交通运行年度报告》
   中的出行方式占比、日均出行量等数据
3. 深圳地铁官方公布的各线路客流量数据
4. 相关交通研究文献中的参数设定

模拟数据在时间分布、空间特征、统计规律上与真实数据保持一致，
能够有效支持数据可视化方法的展示和交通特征的分析。

局限性说明：模拟数据虽基于真实特征生成，但无法完全替代实际
采集数据，研究结论主要用于方法论展示和一般性规律探讨。
```

### 场景3：使用混合数据
```
本研究采用多源数据融合的方式：

1. 空间数据：深圳市政府数据开放平台的道路网络、公交地铁线路
   （公开数据，可直接下载）
   
2. 时间序列数据：基于高德地图公开发布的《中国主要城市交通
   分析报告》中深圳市的统计特征，生成符合真实分布的时序数据
   
3. 气象数据：中国气象数据网深圳站2024年8-10月的实际观测数据

4. 参考数据：Kaggle公开数据集中的交通模式，用于验证分析方法
   的有效性
```

---

## ✅ 数据采集清单

### 最小可行数据集（1天即可）
- [ ] 深圳市道路列表（20-30条主要道路）
- [ ] 深圳地铁线路和站点（公开信息）
- [ ] 深圳市主要区域列表（9个区）
- [ ] 参考报告：高德Q3交通报告

### 标准数据集（3-5天）
- [ ] 高德API Key申请
- [ ] 采集1周的实时路况数据
- [ ] 下载政府平台公交地铁数据
- [ ] 下载30天气象数据

### 完整数据集（2-3周）
- [ ] 采集1个月的实时数据
- [ ] 申请政府平台GPS轨迹数据
- [ ] 爬取地铁官网客流信息
- [ ] 整合新闻事件数据

---

## 🎯 根据时间选择方案

| 剩余时间 | 推荐方案 | 数据质量 |
|----------|----------|----------|
| < 1天 | 模拟数据 | ⭐⭐⭐ |
| 1-3天 | 高德API + 公开数据 | ⭐⭐⭐⭐ |
| 1-2周 | 持续采集 + 申请数据 | ⭐⭐⭐⭐⭐ |
| > 2周 | 多源数据整合 | ⭐⭐⭐⭐⭐ |

---

## 📞 技术支持

### 高德API问题
- 官方文档：https://lbs.amap.com/api/webservice/summary
- 开发者论坛：https://lbs.amap.com/dev/bbs

### 数据处理问题
- Pandas文档：https://pandas.pydata.org/docs/
- Stack Overflow：搜索相关问题

### 其他帮助
- GitHub Issues：提交问题
- 技术社区：SegmentFault、CSDN

---

希望这份指南能帮助您顺利获取深圳交通数据！

记住：**数据质量比数据数量更重要**。即使是小规模的真实数据，
配合合理的分析方法，也能得出有价值的结论。

Good luck! 🚀

