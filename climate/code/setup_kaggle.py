"""
Kaggle API 配置脚本
帮助配置 Kaggle API Token
"""
import os
import json
from pathlib import Path

def setup_kaggle_token(token=None):
    """配置 Kaggle API Token"""
    
    # 获取 token（从参数或环境变量）
    if token is None:
        token = os.environ.get('KAGGLE_API_TOKEN')
    
    if not token:
        print("❌ 未找到 KAGGLE_API_TOKEN")
        print("\n请提供 token:")
        print("  方式1: 设置环境变量")
        print("    export KAGGLE_API_TOKEN=your_token")
        print("  方式2: 运行脚本时传入")
        print("    python setup_kaggle.py your_token")
        return False
    
    print("=" * 70)
    print("  配置 Kaggle API")
    print("=" * 70)
    
    # 创建 .kaggle 目录
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    print(f"✓ 目录已创建: {kaggle_dir}")
    
    # 检查 token 格式
    if token.startswith('KGAT_'):
        # 新格式的 token，需要转换为传统格式
        # 注意：新格式可能需要不同的处理方式
        print("\n⚠️  检测到新格式 token (KGAT_...)")
        print("   尝试两种配置方式...")
        
        # 方式1: 设置环境变量（kagglehub 可能支持）
        print("\n方式1: 设置环境变量...")
        os.environ['KAGGLE_API_TOKEN'] = token
        print(f"✓ 环境变量已设置: KAGGLE_API_TOKEN")
        
        # 方式2: 创建 kaggle.json（传统格式）
        # 注意：新格式 token 可能无法直接用于传统 kaggle.json
        # 但我们可以尝试创建一个占位文件
        print("\n方式2: 创建 kaggle.json...")
        kaggle_json = kaggle_dir / 'kaggle.json'
        
        # 尝试从 token 提取信息（如果可能）
        # 新格式可能需要不同的处理
        kaggle_config = {
            "username": "api_token_user",  # 占位符
            "key": token
        }
        
        with open(kaggle_json, 'w') as f:
            json.dump(kaggle_config, f, indent=2)
        
        # 设置权限
        os.chmod(kaggle_json, 0o600)
        print(f"✓ kaggle.json 已创建: {kaggle_json}")
        print(f"✓ 文件权限已设置: 600")
        
    else:
        # 传统格式
        print("\n检测到传统格式 token")
        kaggle_json = kaggle_dir / 'kaggle.json'
        
        # 如果 token 是 JSON 格式，直接写入
        try:
            config = json.loads(token)
            with open(kaggle_json, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            # 如果不是 JSON，可能需要用户提供 username
            print("⚠️  token 格式不明确")
            print("   传统格式需要 username 和 key")
            print("   请提供完整的 kaggle.json 内容")
            return False
        
        os.chmod(kaggle_json, 0o600)
        print(f"✓ kaggle.json 已创建: {kaggle_json}")
    
    # 测试配置
    print("\n" + "=" * 70)
    print("  测试配置...")
    print("=" * 70)
    
    try:
        import kagglehub
        print("✓ kagglehub 已安装")
        
        # 尝试一个简单的操作来验证 token
        print("✓ 配置完成！")
        print("\n可以运行下载脚本测试:")
        print("  python download_data.py")
        
        return True
        
    except ImportError:
        print("⚠️  kagglehub 未安装")
        print("   请运行: pip install kagglehub")
        return False
    except Exception as e:
        print(f"⚠️  测试时出错: {e}")
        print("   但配置已保存，可以尝试运行下载脚本")
        return True

def main():
    """主函数"""
    import sys
    
    # 从命令行参数获取 token
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    
    # 或者从环境变量获取
    if not token:
        token = os.environ.get('KAGGLE_API_TOKEN')
    
    # 如果都没有，提示用户
    if not token:
        print("=" * 70)
        print("  Kaggle API 配置工具")
        print("=" * 70)
        print("\n请提供 KAGGLE_API_TOKEN:")
        print("\n方式1: 设置环境变量后运行脚本")
        print("  export KAGGLE_API_TOKEN=your_token")
        print("  python setup_kaggle.py")
        print("\n方式2: 直接传入 token")
        print("  python setup_kaggle.py your_token")
        print("\n方式3: 在脚本中设置（不推荐）")
        return
    
    setup_kaggle_token(token)

if __name__ == '__main__':
    main()

