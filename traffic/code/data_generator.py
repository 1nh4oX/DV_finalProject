"""
深圳交通数据生成器
由于真实API需要申请，此脚本生成基于深圳真实交通特征的模拟数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# 设置随机种子以保证可重复性
np.random.seed(42)


class ShenzhenTrafficDataGenerator:
    """深圳交通数据生成器"""
    
    def __init__(self):
        # 深圳主要道路（基于真实道路）
        self.major_roads = [
            "深南大道", "北环大道", "滨河大道", "滨海大道", "沙河西路",
            "科技园路", "南坪快速", "福龙路", "布龙路", "龙岗大道",
            "宝安大道", "新安路", "松白路", "留仙大道", "梅观高速",
            "机荷高速", "盐排高速", "水官高速", "广深高速", "南光高速"
        ]
        
        # 深圳地铁线路
        self.metro_lines = [
            "1号线", "2号线", "3号线", "4号线", "5号线",
            "6号线", "7号线", "8号线", "9号线", "10号线", "11号线"
        ]
        
        # 深圳主要区域（用于OD分析）
        self.districts = [
            "福田区", "罗湖区", "南山区", "宝安区", "龙岗区",
            "龙华区", "盐田区", "坪山区", "光明区"
        ]
        
        # 主要地点坐标（经纬度）
        self.key_locations = {
            "市民中心": (114.0579, 22.5460),
            "深圳北站": (114.0294, 22.6089),
            "华强北": (114.0893, 22.5461),
            "科技园": (113.9530, 22.5429),
            "前海": (113.8930, 22.5330),
            "福田口岸": (114.0618, 22.5170),
            "罗湖口岸": (114.1780, 22.5430),
            "宝安中心": (113.8830, 22.5540),
            "龙岗中心城": (114.2470, 22.7200),
            "坪山中心": (114.3470, 22.7000)
        }
    
    def generate_hourly_traffic(self, days=30):
        """生成每小时交通流量数据（用于高峰时段折线图）"""
        data = []
        start_date = datetime(2024, 11, 1)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5
            
            for hour in range(24):
                # 模拟真实的交通高峰模式
                base_volume = 1000
                
                # 工作日高峰：早上7-9点，晚上17-19点
                if not is_weekend:
                    if 7 <= hour <= 9:
                        volume = base_volume * np.random.uniform(2.5, 3.5)
                    elif 17 <= hour <= 19:
                        volume = base_volume * np.random.uniform(2.8, 4.0)
                    elif 10 <= hour <= 16:
                        volume = base_volume * np.random.uniform(1.5, 2.0)
                    else:
                        volume = base_volume * np.random.uniform(0.3, 0.8)
                else:
                    # 周末流量较平缓，高峰在10-20点
                    if 10 <= hour <= 20:
                        volume = base_volume * np.random.uniform(1.5, 2.5)
                    else:
                        volume = base_volume * np.random.uniform(0.4, 1.0)
                
                # 添加随机波动
                volume *= np.random.uniform(0.9, 1.1)
                
                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'datetime': current_date.replace(hour=hour),
                    'hour': hour,
                    'day_of_week': current_date.strftime('%A'),
                    'is_weekend': is_weekend,
                    'traffic_volume': int(volume),
                    'avg_speed': max(20, 60 - (volume / 50))  # 流量越大，速度越慢
                })
        
        return pd.DataFrame(data)
    
    def generate_road_congestion(self, num_samples=1000):
        """生成路段拥堵数据（用于热力图）"""
        data = []
        
        for road in self.major_roads:
            # 为每条道路生成多个路段
            num_segments = np.random.randint(5, 15)
            
            # 基础坐标（深圳市中心附近）
            base_lat, base_lon = 22.5431, 114.0579
            
            for segment in range(num_segments):
                # 不同时段的拥堵程度
                for time_period in ['morning_peak', 'midday', 'evening_peak', 'night']:
                    if time_period == 'morning_peak':
                        congestion_index = np.random.uniform(6, 10)  # 严重拥堵
                    elif time_period == 'evening_peak':
                        congestion_index = np.random.uniform(7, 10)  # 非常拥堵
                    elif time_period == 'midday':
                        congestion_index = np.random.uniform(4, 7)   # 中度拥堵
                    else:
                        congestion_index = np.random.uniform(1, 4)   # 畅通
                    
                    # 生成路段坐标（在深圳范围内随机分布）
                    lat = base_lat + np.random.uniform(-0.3, 0.3)
                    lon = base_lon + np.random.uniform(-0.3, 0.3)
                    
                    data.append({
                        'road_name': road,
                        'segment_id': f"{road}_{segment}",
                        'latitude': lat,
                        'longitude': lon,
                        'time_period': time_period,
                        'congestion_index': congestion_index,
                        'avg_speed': max(10, 70 - congestion_index * 6),
                        'travel_time_index': congestion_index / 10 * 2  # 相对于畅通时的倍数
                    })
        
        return pd.DataFrame(data)
    
    def generate_metro_ridership(self, days=30):
        """生成地铁客流数据（用于箱线图）"""
        data = []
        start_date = datetime(2024, 11, 1)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5
            
            for line in self.metro_lines:
                # 不同线路的基础客流不同
                if line in ["1号线", "2号线", "3号线", "5号线"]:
                    base_ridership = 500000  # 主要线路
                else:
                    base_ridership = 300000  # 次要线路
                
                # 工作日客流更大
                if is_weekend:
                    ridership = base_ridership * np.random.uniform(0.6, 0.8)
                else:
                    ridership = base_ridership * np.random.uniform(0.9, 1.2)
                
                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'line': line,
                    'is_weekend': is_weekend,
                    'daily_ridership': int(ridership),
                    'peak_hour_ridership': int(ridership * 0.15),  # 高峰小时约占15%
                    'avg_load_factor': np.random.uniform(0.5, 0.95)  # 满载率
                })
        
        return pd.DataFrame(data)
    
    def generate_od_data(self, num_records=500):
        """生成OD（起点-终点）流动数据"""
        data = []
        
        for _ in range(num_records):
            origin = np.random.choice(self.districts)
            destination = np.random.choice([d for d in self.districts if d != origin])
            
            # 某些OD对更常见（如居住区到商业区）
            if (origin in ["龙华区", "龙岗区", "宝安区"]) and (destination in ["福田区", "南山区"]):
                flow_volume = np.random.randint(5000, 15000)
            else:
                flow_volume = np.random.randint(500, 5000)
            
            data.append({
                'origin': origin,
                'destination': destination,
                'flow_volume': flow_volume,
                'avg_travel_time': np.random.uniform(20, 90),  # 分钟
                'main_mode': np.random.choice(['地铁', '公交', '自驾', '混合'], p=[0.4, 0.25, 0.3, 0.05])
            })
        
        return pd.DataFrame(data)
    
    def generate_top_congested_roads(self):
        """生成TOP拥堵道路数据"""
        data = []
        
        # 选择最拥堵的10条道路
        selected_roads = np.random.choice(self.major_roads, 10, replace=False)
        
        for i, road in enumerate(selected_roads):
            data.append({
                'road_name': road,
                'avg_congestion_index': np.random.uniform(7, 10),
                'peak_hours_per_day': np.random.uniform(4, 8),
                'avg_delay_minutes': np.random.uniform(10, 45),
                'rank': i + 1
            })
        
        df = pd.DataFrame(data)
        return df.sort_values('avg_congestion_index', ascending=False)
    
    def generate_travel_mode_share(self):
        """生成出行方式占比数据"""
        modes = {
            '地铁': 28,
            '公交': 22,
            '自驾': 25,
            '出租车/网约车': 12,
            '骑行': 8,
            '步行': 5
        }
        
        # 添加一些随机波动
        data = []
        for mode, percentage in modes.items():
            data.append({
                'travel_mode': mode,
                'percentage': percentage + np.random.uniform(-2, 2),
                'daily_trips': int(percentage * 50000 * np.random.uniform(0.9, 1.1))
            })
        
        return pd.DataFrame(data)
    
    def generate_weather_traffic(self, days=90):
        """生成天气与交通关系数据"""
        data = []
        start_date = datetime(2024, 8, 1)
        
        weather_types = ['晴天', '多云', '小雨', '中雨', '大雨']
        weather_probs = [0.4, 0.3, 0.15, 0.1, 0.05]
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            weather = np.random.choice(weather_types, p=weather_probs)
            
            # 天气对拥堵的影响
            base_congestion = 5.0
            if weather == '晴天':
                congestion = base_congestion * np.random.uniform(0.8, 1.0)
            elif weather == '多云':
                congestion = base_congestion * np.random.uniform(0.9, 1.1)
            elif weather == '小雨':
                congestion = base_congestion * np.random.uniform(1.1, 1.3)
            elif weather == '中雨':
                congestion = base_congestion * np.random.uniform(1.3, 1.6)
            else:  # 大雨
                congestion = base_congestion * np.random.uniform(1.5, 2.0)
            
            # 温度也会影响出行
            temperature = np.random.uniform(18, 35)
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'weather': weather,
                'temperature': temperature,
                'rainfall_mm': 0 if weather == '晴天' else np.random.exponential(20),
                'congestion_index': congestion,
                'avg_speed': max(25, 65 - congestion * 5),
                'accident_count': int(congestion * np.random.uniform(0.5, 1.5))
            })
        
        return pd.DataFrame(data)
    
    def generate_daily_trips_distribution(self, num_days=60):
        """生成每日出行次数分布数据"""
        data = []
        start_date = datetime(2024, 9, 1)
        
        for day in range(num_days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5
            
            # 工作日和周末的出行模式不同
            if is_weekend:
                daily_trips = np.random.normal(8000000, 1000000)  # 周末出行较少
            else:
                daily_trips = np.random.normal(12000000, 1500000)  # 工作日出行更多
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'day_type': '周末' if is_weekend else '工作日',
                'total_trips': max(0, int(daily_trips)),
                'trips_per_capita': max(0, daily_trips / 13000000)  # 深圳常住人口约1300万
            })
        
        return pd.DataFrame(data)
    
    def generate_speed_distribution(self, num_samples=10000):
        """生成道路速度分布数据（用于核密度图）"""
        data = []
        
        # 三种道路类型的速度分布
        road_types = {
            '高速公路': {'mean': 90, 'std': 20, 'count': 0.2},
            '主干道': {'mean': 45, 'std': 15, 'count': 0.5},
            '支路': {'mean': 25, 'std': 10, 'count': 0.3}
        }
        
        for road_type, params in road_types.items():
            num = int(num_samples * params['count'])
            speeds = np.random.normal(params['mean'], params['std'], num)
            speeds = np.clip(speeds, 5, 120)  # 限制在合理范围
            
            for speed in speeds:
                data.append({
                    'road_type': road_type,
                    'speed_kmh': speed,
                    'time_period': np.random.choice(['高峰期', '平峰期', '低峰期'])
                })
        
        return pd.DataFrame(data)
    
    def generate_all_data(self):
        """生成所有数据并保存"""
        print("开始生成深圳交通数据...")
        
        datasets = {
            'hourly_traffic': self.generate_hourly_traffic(),
            'road_congestion': self.generate_road_congestion(),
            'metro_ridership': self.generate_metro_ridership(),
            'od_flow': self.generate_od_data(),
            'top_congested_roads': self.generate_top_congested_roads(),
            'travel_mode_share': self.generate_travel_mode_share(),
            'weather_traffic': self.generate_weather_traffic(),
            'daily_trips': self.generate_daily_trips_distribution(),
            'speed_distribution': self.generate_speed_distribution()
        }
        
        return datasets


def main():
    """主函数：生成并保存所有数据"""
    generator = ShenzhenTrafficDataGenerator()
    datasets = generator.generate_all_data()
    
    # 保存数据
    import os
    data_dir = '../trafficData/sample'
    os.makedirs(data_dir, exist_ok=True)
    
    for name, df in datasets.items():
        filepath = os.path.join(data_dir, f'{name}.csv')
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"✓ 已保存 {name}: {len(df)} 条记录 -> {filepath}")
    
    print("\n数据生成完成！")
    print(f"总共生成了 {len(datasets)} 个数据集")


if __name__ == '__main__':
    main()

