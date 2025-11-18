"""
高德API Key测试工具
用于验证您的Key类型是否正确
"""

import requests
import json

def test_amap_key(api_key):
    """
    测试高德API Key是否可用
    
    Args:
        api_key: 您的API Key
    """
    print("="*60)
    print("高德API Key测试工具")
    print("="*60)
    print(f"\n正在测试Key: {api_key[:10]}...{api_key[-4:]}")
    print("-"*60)
    
    # 测试1: IP定位API（最简单的测试）
    print("\n【测试1】IP定位API（基础测试）")
    url1 = 'https://restapi.amap.com/v3/ip'
    params1 = {
        'key': api_key,
        'output': 'json'
    }
    
    try:
        response = requests.get(url1, params=params1, timeout=5)
        data1 = response.json()
        
        if data1.get('status') == '1':
            print("✅ 测试通过！Key类型正确（Web服务API）")
            print(f"   返回信息: {data1.get('info')}")
            print(f"   当前位置: {data1.get('province', '未知')} {data1.get('city', '未知')}")
            return True
        else:
            print("❌ 测试失败")
            print(f"   错误代码: {data1.get('infocode')}")
            print(f"   错误信息: {data1.get('info')}")
            
            # 详细错误说明
            error_code = data1.get('infocode')
            if error_code == '10009':
                print("\n   ⚠️  错误原因：Key平台类型不匹配")
                print("   💡 解决方案：")
                print("      1. 登录 https://console.amap.com/dev/key/app")
                print("      2. 在您的应用下点击'添加Key'")
                print("      3. 选择服务平台：'Web服务'（不是'Web端(JS API)'）")
                print("      4. 使用新创建的Web服务Key")
            elif error_code == '10001':
                print("\n   ⚠️  错误原因：Key无效或不存在")
                print("   💡 请检查Key是否正确复制")
            elif error_code == '10003':
                print("\n   ⚠️  错误原因：Key权限不足")
                print("   💡 请检查Key是否开通了相应服务")
            
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False
    
    # 测试2: 交通态势API（如果测试1通过）
    if data1.get('status') == '1':
        print("\n【测试2】交通态势API（功能测试）")
        url2 = 'https://restapi.amap.com/v3/traffic/status/rectangle'
        params2 = {
            'key': api_key,
            'rectangle': '113.75,22.4;114.62,22.86',  # 深圳市范围
            'extensions': 'base',
            'output': 'json'
        }
        
        try:
            response = requests.get(url2, params=params2, timeout=10)
            data2 = response.json()
            
            if data2.get('status') == '1':
                print("✅ 交通API测试通过！")
                roads_count = len(data2.get('trafficinfo', {}).get('roads', []))
                print(f"   获取到 {roads_count} 条道路数据")
                return True
            else:
                print("⚠️  交通API测试失败（可能是配额用完或服务未开通）")
                print(f"   错误: {data2.get('info')}")
                print("   但基础Key测试已通过，可以继续使用其他API")
                return True  # 基础Key可用即可
                
        except Exception as e:
            print(f"⚠️  交通API请求异常: {e}")
            print("   但基础Key测试已通过，可以继续使用")
            return True
    
    return False


def main():
    """主函数"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║           高德API Key测试工具                          ║
    ║                                                        ║
    ║  此工具用于验证您的Key类型是否正确                     ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # 方式1: 从命令行参数获取
    import sys
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        # 方式2: 交互式输入
        print("\n请输入您的高德API Key:")
        print("（可以在高德控制台找到：https://console.amap.com/dev/key/app）")
        api_key = input("Key: ").strip()
    
    if not api_key:
        print("\n❌ 未输入Key，退出")
        return
    
    # 测试Key
    result = test_amap_key(api_key)
    
    print("\n" + "="*60)
    if result:
        print("✅ 测试结果：Key可用！")
        print("\n下一步：")
        print("1. 将Key复制到 src/amap_api_example.py 第19行")
        print("2. 运行 python3 src/amap_api_example.py")
    else:
        print("❌ 测试结果：Key不可用")
        print("\n请按照上面的提示创建正确的Web服务Key")
    print("="*60)


if __name__ == '__main__':
    main()

