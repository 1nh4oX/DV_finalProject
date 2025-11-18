"""
高德地图API数据采集示例
用于获取深圳市真实交通数据

使用前请先：
1. 注册高德开放平台账号：https://lbs.amap.com/
2. 创建应用并获取API Key
3. 将YOUR_API_KEY替换为你的实际Key
"""

import requests
import pandas as pd
import time
from datetime import datetime
import json

class AmapDataCollector:
    """高德地图数据采集器"""
    
    def __init__(self, api_key):
        """
        初始化
        Args:
            api_key: 高德地图API Key
        """
        self.api_key = api_key
        self.base_url = 'https://restapi.amap.com'
        
        # 深圳市主要区域边界（矩形范围）
        self.shenzhen_bounds = {
            'southwest': '113.75,22.4',    # 西南角
            'northeast': '114.62,22.86'    # 东北角
        }
        
        # 深圳主要地点坐标
        self.key_locations = {
            '市民中心': '114.057868,22.543099',
            '深圳北站': '114.029439,22.608900',
            '华强北': '114.089346,22.546119',
            '科技园': '113.953066,22.542907',
            '前海': '113.893000,22.533000',
            '福田口岸': '114.061800,22.517000',
            '罗湖口岸': '114.178000,22.543000',
            '宝安中心': '113.883000,22.554000',
            '龙岗中心城': '114.247000,22.720000',
            '坪山中心': '114.347000,22.700000'
        }
    
    def get_traffic_status(self, rectangle=None):
        """
        获取实时交通路况
        
        Args:
            rectangle: 矩形范围，格式：'左下角经纬度;右上角经纬度'
                      如：'113.75,22.4;114.62,22.86'
        
        Returns:
            dict: 交通状态数据
        """
        url = f'{self.base_url}/v3/traffic/status/rectangle'
        
        if rectangle is None:
            rectangle = f"{self.shenzhen_bounds['southwest']};{self.shenzhen_bounds['northeast']}"
        
        params = {
            'key': self.api_key,
            'rectangle': rectangle,
            'extensions': 'all',  # all-返回道路交通状态, base-返回道路拥堵指数
            'output': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':  # 成功
                print(f"✓ 成功获取交通数据")
                return data
            else:
                print(f"✗ 获取失败: {data.get('info', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"✗ 请求异常: {e}")
            return None
    
    def parse_traffic_data(self, raw_data):
        """
        解析交通数据
        
        Args:
            raw_data: get_traffic_status返回的原始数据
        
        Returns:
            DataFrame: 解析后的数据
        """
        if not raw_data or raw_data['status'] != '1':
            return pd.DataFrame()
        
        roads = raw_data['trafficinfo']['roads']
        
        data_list = []
        for road in roads:
            data_list.append({
                'timestamp': datetime.now(),
                'road_name': road['name'],
                'status': road['status'],  # 0-未知, 1-畅通, 2-缓行, 3-拥堵, 4-严重拥堵
                'direction': road.get('direction', ''),
                'angle': road.get('angle', 0),
                'speed': float(road.get('speed', 0)),  # 平均速度 km/h
                'polyline': road.get('polyline', ''),  # 道路坐标串
            })
        
        df = pd.DataFrame(data_list)
        
        # 状态映射
        status_map = {0: '未知', 1: '畅通', 2: '缓行', 3: '拥堵', 4: '严重拥堵'}
        df['status_text'] = df['status'].map(status_map)
        
        # 拥堵指数 (0-10)
        congestion_map = {0: 0, 1: 2, 2: 5, 3: 7.5, 4: 9.5}
        df['congestion_index'] = df['status'].map(congestion_map)
        
        return df
    
    def get_route_planning(self, origin, destination, strategy=0):
        """
        路径规划（用于OD分析）
        
        Args:
            origin: 起点坐标 "经度,纬度"
            destination: 终点坐标 "经度,纬度"
            strategy: 驾车策略
                     0-速度优先（时间）
                     1-费用优先（不走收费路段的最快道路）
                     2-距离优先
                     3-不走快速路
                     ...
        
        Returns:
            dict: 路径规划结果
        """
        url = f'{self.base_url}/v3/direction/driving'
        
        params = {
            'key': self.api_key,
            'origin': origin,
            'destination': destination,
            'extensions': 'all',
            'strategy': strategy,
            'output': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1':
                print(f"✓ 成功获取路径规划")
                return data
            else:
                print(f"✗ 获取失败: {data.get('info', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"✗ 请求异常: {e}")
            return None
    
    def parse_route_data(self, raw_data):
        """
        解析路径规划数据
        
        Returns:
            dict: 路径信息
        """
        if not raw_data or raw_data['status'] != '1':
            return {}
        
        route = raw_data['route']
        paths = route['paths'][0]  # 取第一条路径
        
        return {
            'origin': route['origin'],
            'destination': route['destination'],
            'distance': int(paths['distance']),  # 米
            'duration': int(paths['duration']),  # 秒
            'traffic_lights': int(paths.get('traffic_lights', 0)),  # 红绿灯数
            'tolls': float(paths.get('tolls', 0)),  # 过路费
            'toll_distance': int(paths.get('toll_distance', 0)),  # 收费路段距离
        }
    
    def geocode(self, address, city='深圳'):
        """
        地理编码：地址 -> 坐标
        
        Args:
            address: 地址名称
            city: 城市名称
        
        Returns:
            str: 坐标 "经度,纬度"
        """
        url = f'{self.base_url}/v3/geocode/geo'
        
        params = {
            'key': self.api_key,
            'address': address,
            'city': city,
            'output': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['status'] == '1' and data['geocodes']:
                location = data['geocodes'][0]['location']
                print(f"✓ {address} -> {location}")
                return location
            else:
                print(f"✗ 地理编码失败: {address}")
                return None
                
        except Exception as e:
            print(f"✗ 请求异常: {e}")
            return None
    
    def collect_hourly_traffic(self, hours=24):
        """
        连续采集多小时的交通数据
        
        Args:
            hours: 采集小时数
        
        Returns:
            DataFrame: 汇总数据
        """
        all_data = []
        
        print(f"开始采集 {hours} 小时的交通数据...")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for i in range(hours):
            print(f"\n--- 第 {i+1}/{hours} 小时 ---")
            
            # 获取交通状态
            raw_data = self.get_traffic_status()
            
            if raw_data:
                df = self.parse_traffic_data(raw_data)
                all_data.append(df)
                print(f"本次采集: {len(df)} 条道路数据")
            
            # 等待1小时（或更短的间隔用于测试）
            if i < hours - 1:
                wait_seconds = 3600  # 1小时
                # 测试时可以改为更短，如：
                # wait_seconds = 300  # 5分钟
                
                print(f"等待 {wait_seconds} 秒...")
                time.sleep(wait_seconds)
        
        # 合并所有数据
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            print(f"\n✓ 采集完成！总共 {len(final_df)} 条记录")
            return final_df
        else:
            print("\n✗ 未采集到数据")
            return pd.DataFrame()
    
    def collect_od_matrix(self, locations=None):
        """
        采集OD矩阵数据
        
        Args:
            locations: 地点字典 {名称: 坐标}
        
        Returns:
            DataFrame: OD数据
        """
        if locations is None:
            locations = self.key_locations
        
        od_data = []
        location_names = list(locations.keys())
        total = len(location_names) * (len(location_names) - 1)
        count = 0
        
        print(f"开始采集 {len(location_names)} 个地点的OD矩阵...")
        print(f"总共需要 {total} 次请求")
        
        for origin_name in location_names:
            for dest_name in location_names:
                if origin_name == dest_name:
                    continue
                
                count += 1
                print(f"\n[{count}/{total}] {origin_name} -> {dest_name}")
                
                # 路径规划
                raw_data = self.get_route_planning(
                    locations[origin_name],
                    locations[dest_name]
                )
                
                if raw_data:
                    route_info = self.parse_route_data(raw_data)
                    route_info['origin_name'] = origin_name
                    route_info['destination_name'] = dest_name
                    route_info['timestamp'] = datetime.now()
                    od_data.append(route_info)
                
                # 避免请求过快
                time.sleep(0.5)
        
        df = pd.DataFrame(od_data)
        print(f"\n✓ OD矩阵采集完成！{len(df)} 条记录")
        return df


def example_usage():
    """使用示例"""
 

    # 1. 初始化（请替换为你的API Key）
    API_KEY = '251dcbe399a442220c89e8b5ce9c1308'  # ⚠️ 替换这里
    
    collector = AmapDataCollector(API_KEY)
    
    print("="*60)
    print("高德地图API数据采集示例")
    print("="*60)
    
    # 2. 获取单次交通状态
    print("\n【示例1】获取实时交通状态")
    print("-"*60)
    raw_traffic = collector.get_traffic_status()
    
    if raw_traffic:
        df_traffic = collector.parse_traffic_data(raw_traffic)
        print("\n数据预览:")
        print(df_traffic.head(10))
        
        # 保存数据
        output_file = '../trafficData/raw/traffic_realtime.csv'
        df_traffic.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ 数据已保存: {output_file}")
    
    # 3. 地理编码
    print("\n【示例2】地理编码")
    print("-"*60)
    location = collector.geocode('深南大道', '深圳')
    
    # 4. 路径规划
    print("\n【示例3】路径规划")
    print("-"*60)
    route = collector.get_route_planning(
        collector.key_locations['市民中心'],
        collector.key_locations['深圳北站']
    )
    
    if route:
        route_info = collector.parse_route_data(route)
        print("\n路径信息:")
        for key, value in route_info.items():
            print(f"  {key}: {value}")
    
    # 5. 采集OD矩阵（可选，耗时较长）
    print("\n【示例4】采集OD矩阵")
    print("-"*60)
    print("⚠️ 这将进行多次API调用，较耗时")
    
    # 取部分地点测试
    test_locations = {
        '市民中心': collector.key_locations['市民中心'],
        '深圳北站': collector.key_locations['深圳北站'],
        '科技园': collector.key_locations['科技园']
    }
    
    df_od = collector.collect_od_matrix(test_locations)
    
    if not df_od.empty:
        print("\nOD数据预览:")
        print(df_od)
        
        output_file = '../trafficData/raw/od_matrix_amap.csv'
        df_od.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ OD数据已保存: {output_file}")
    
    print("\n" + "="*60)
    print("示例完成！")
    print("="*60)


def continuous_collection():
    """
    持续采集示例
    用于长期监测交通状况
    """
    API_KEY = 'YOUR_API_KEY_HERE'  # ⚠️ 替换这里
    
    collector = AmapDataCollector(API_KEY)
    
    # 采集24小时数据
    df = collector.collect_hourly_traffic(hours=24)
    
    if not df.empty:
        # 保存数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'../trafficData/raw/traffic_24h_{timestamp}.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ 数据已保存: {output_file}")
        
        # 简单统计
        print("\n数据统计:")
        print(f"  总记录数: {len(df)}")
        print(f"  唯一道路数: {df['road_name'].nunique()}")
        print(f"  平均速度: {df['speed'].mean():.2f} km/h")
        print(f"  拥堵道路数: {len(df[df['status'] >= 3])}")


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║       高德地图API数据采集工具                          ║
    ║                                                        ║
    ║  使用前请：                                            ║
    ║  1. 注册高德开放平台账号                              ║
    ║  2. 获取API Key                                        ║
    ║  3. 将代码中的 YOUR_API_KEY_HERE 替换为实际Key       ║
    ║                                                        ║
    ║  详细说明请查看: DATA_SOURCE_GUIDE.md                 ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # 运行示例
    example_usage()
    
    # 如需持续采集，取消下面的注释
    # continuous_collection()

