"""
气候数据自动下载脚本
使用 kagglehub 自动下载所需的气候数据集
"""
import kagglehub
import shutil
import os
from pathlib import Path
import sys
import time
import socket

# 支持从环境变量读取 token
if 'KAGGLE_API_TOKEN' in os.environ:
    token = os.environ['KAGGLE_API_TOKEN']
    # kagglehub 可能支持环境变量，但为了兼容性，也设置到 kaggle.json
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    # 如果 token 以 KGAT_ 开头，是新格式
    if token.startswith('KGAT_'):
        import json
        config = {
            "username": "api_token_user",
            "key": token
        }
        with open(kaggle_json, 'w') as f:
            json.dump(config, f)
        os.chmod(kaggle_json, 0o600)
        print(f"✓ 已从环境变量配置 Kaggle API Token")

# 设置更长的超时时间
socket.setdefaulttimeout(300)  # 5分钟超时

def download_with_retry(dataset_name, max_retries=3, retry_delay=5):
    """
    带重试机制的下载函数
    
    Args:
        dataset_name: 数据集名称
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
    
    Returns:
        下载路径或 None
    """
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"  🔄 第 {attempt + 1} 次重试...")
                time.sleep(retry_delay)
            
            path = kagglehub.dataset_download(dataset_name)
            return path
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️  下载失败: {e}")
                print(f"  等待 {retry_delay} 秒后重试...")
            else:
                raise e
    
    return None

def setup_directories(base_dir='../data/raw'):
    """创建必要的目录结构"""
    base_path = Path(base_dir)
    directories = [
        base_path,
        base_path / 'co2',
        base_path / 'sea_level',
        base_path / 'sea_ice'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ 目录已创建: {directory}")
    
    return base_path

def download_temperature_data(output_dir):
    """下载温度数据"""
    print("\n" + "=" * 70)
    print("📥 下载温度数据...")
    print("=" * 70)
    
    dataset_name = "berkeleyearth/climate-change-earth-surface-temperature-data"
    
    try:
        print(f"正在下载数据集: {dataset_name}")
        print("⏳ 这可能需要几分钟，请耐心等待...")
        path = download_with_retry(dataset_name)
        
        if path is None:
            raise Exception("重试次数已用尽")
        
        print(f"✓ 下载完成！路径: {path}")
        
        # 查找CSV文件并复制到目标目录
        csv_files = list(Path(path).glob("*.csv"))
        
        if csv_files:
            print(f"\n找到 {len(csv_files)} 个CSV文件:")
            for csv_file in csv_files:
                dest_file = output_dir / csv_file.name
                shutil.copy2(csv_file, dest_file)
                print(f"  ✓ {csv_file.name} -> {dest_file}")
        else:
            print("⚠️  未找到CSV文件")
            print(f"   下载路径: {path}")
            print("   请手动检查并复制文件到 data/raw/ 目录")
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print("\n请检查:")
        print("1. 是否已安装 kagglehub: pip install kagglehub")
        print("2. 是否已配置 Kaggle API: https://www.kaggle.com/settings")
        return False

def download_co2_data(output_dir):
    """下载CO2排放数据"""
    print("\n" + "=" * 70)
    print("📥 下载CO2排放数据...")
    print("=" * 70)
    
    dataset_name = "ulrikthygepedersen/co2-emissions-by-country"
    
    try:
        print(f"正在下载数据集: {dataset_name}")
        print("⏳ 这可能需要几分钟，请耐心等待...")
        path = download_with_retry(dataset_name)
        
        if path is None:
            raise Exception("重试次数已用尽")
        
        print(f"✓ 下载完成！路径: {path}")
        
        # 查找CSV文件并复制到目标目录
        csv_files = list(Path(path).glob("*.csv"))
        
        if csv_files:
            print(f"\n找到 {len(csv_files)} 个CSV文件:")
            for csv_file in csv_files:
                # 复制到 co2 子目录
                dest_file = output_dir / 'co2' / csv_file.name
                shutil.copy2(csv_file, dest_file)
                print(f"  ✓ {csv_file.name} -> {dest_file}")
        else:
            print("⚠️  未找到CSV文件")
            print(f"   下载路径: {path}")
            print("   请手动检查并复制文件到 data/raw/co2/ 目录")
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print("\n请检查:")
        print("1. 是否已安装 kagglehub: pip install kagglehub")
        print("2. 是否已配置 Kaggle API: https://www.kaggle.com/settings")
        return False

def download_sea_level_data(output_dir):
    """下载海平面数据"""
    print("\n" + "=" * 70)
    print("📥 下载海平面数据...")
    print("=" * 70)
    
    dataset_name = "kkhandekar/global-sea-level-1993-2021"
    
    try:
        print(f"正在下载数据集: {dataset_name}")
        print("⏳ 这可能需要几分钟，请耐心等待...")
        path = download_with_retry(dataset_name)
        
        if path is None:
            raise Exception("重试次数已用尽")
        
        print(f"✓ 下载完成！路径: {path}")
        
        # 查找CSV文件并复制到目标目录
        csv_files = list(Path(path).glob("*.csv"))
        
        if csv_files:
            print(f"\n找到 {len(csv_files)} 个CSV文件:")
            for csv_file in csv_files:
                # 复制到 sea_level 子目录
                dest_file = output_dir / 'sea_level' / csv_file.name
                shutil.copy2(csv_file, dest_file)
                print(f"  ✓ {csv_file.name} -> {dest_file}")
        else:
            print("⚠️  未找到CSV文件")
            print(f"   下载路径: {path}")
            print("   请手动检查并复制文件到 data/raw/sea_level/ 目录")
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print("\n请检查:")
        print("1. 是否已安装 kagglehub: pip install kagglehub")
        print("2. 是否已配置 Kaggle API: https://www.kaggle.com/settings")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("  气候数据自动下载工具")
    print("  Climate Data Auto-Download Tool")
    print("=" * 70)
    
    # 设置输出目录
    base_dir = Path(__file__).parent.parent / 'data' / 'raw'
    output_dir = setup_directories(base_dir)
    
    print(f"\n📁 数据将保存到: {output_dir.absolute()}")
    
    # 检查 kagglehub 是否安装
    try:
        import kagglehub
    except ImportError:
        print("\n❌ 未安装 kagglehub")
        print("\n请先安装:")
        print("  pip install kagglehub")
        print("\n然后配置 Kaggle API:")
        print("  1. 访问 https://www.kaggle.com/settings")
        print("  2. 创建 API Token")
        print("  3. 将 kaggle.json 放到 ~/.kaggle/ 目录")
        return
    
    # 下载数据
    results = {
        'temperature': False,
        'co2': False,
        'sea_level': False
    }
    
    # 下载温度数据
    results['temperature'] = download_temperature_data(output_dir)
    
    # 下载CO2数据
    results['co2'] = download_co2_data(output_dir)
    
    # 下载海平面数据
    results['sea_level'] = download_sea_level_data(output_dir)
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 下载总结")
    print("=" * 70)
    
    for dataset, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {dataset:15s}: {status}")
    
    print("\n" + "=" * 70)
    
    if all(results.values()):
        print("🎉 所有数据下载完成！")
    else:
        print("⚠️  部分数据下载失败，请检查错误信息")
    
    print("=" * 70)
    print(f"\n📁 数据位置: {output_dir.absolute()}")
    print("\n📝 下一步:")
    print("  运行 python main.py 开始分析")

if __name__ == '__main__':
    main()

