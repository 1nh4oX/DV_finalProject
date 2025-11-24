# 🔑 Kaggle API 配置指南

本指南将帮助团队成员配置 Kaggle API，以便使用自动下载脚本获取数据。

---

## 📋 前提条件

1. **Kaggle 账号**
   - 如果没有账号，请先注册：https://www.kaggle.com/
   - 必须登录账号才能使用 API

2. **Python 环境**
   - 已安装 Python 3.7+
   - 已激活项目虚拟环境

---

## 🚀 快速配置步骤

### 方法1：使用配置脚本（推荐）⭐

这是最简单的方法，适合所有团队成员。

#### 步骤1：获取 API Token

1. **登录 Kaggle**
   - 访问：https://www.kaggle.com/
   - 使用你的账号登录

2. **创建 API Token**
   - 访问：https://www.kaggle.com/settings
   - 找到 "API" 部分
   - 点击 **"Create New Token"** 按钮
   - 浏览器会自动下载 `kaggle.json` 文件

3. **查看 Token**
   - 打开下载的 `kaggle.json` 文件
   - 你会看到类似这样的内容：
   ```json
   {
     "username": "your_username",
     "key": "your_api_key_here"
   }
   ```
   - 或者新格式的 token（以 `KGAT_` 开头）

#### 步骤2：配置 Token

**方式A：使用环境变量（推荐）**

```bash
# 设置环境变量（临时，当前终端会话有效）
export KAGGLE_API_TOKEN=your_token_here

# 或者新格式的 token
export KAGGLE_API_TOKEN=KGAT_7c319203a92821e089420a7c022d3a3f
```

**方式B：使用配置脚本**

```bash
# 进入项目目录
cd /path/to/project

# 激活虚拟环境
source venv/bin/activate

# 运行配置脚本
cd climate/code
python setup_kaggle.py

# 或者直接传入 token
python setup_kaggle.py your_token_here
```

**方式C：手动创建配置文件**

```bash
# 创建 .kaggle 目录
mkdir -p ~/.kaggle

# 复制 kaggle.json 到正确位置
cp ~/Downloads/kaggle.json ~/.kaggle/

# 设置正确的权限（重要！）
chmod 600 ~/.kaggle/kaggle.json
```

#### 步骤3：验证配置

```bash
# 测试配置是否成功
cd climate/code
python download_data.py
```

如果看到下载进度，说明配置成功！

---

## 🔧 详细配置说明

### 方法2：传统方式（使用 kaggle.json）

#### 步骤1：下载 kaggle.json

1. 访问 https://www.kaggle.com/settings
2. 点击 "Create New Token"
3. 下载 `kaggle.json` 文件

#### 步骤2：放置配置文件

```bash
# Linux/Mac
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Windows
# 创建目录: C:\Users\YourUsername\.kaggle
# 将 kaggle.json 放到该目录
```

#### 步骤3：验证

```bash
# 安装 kagglehub（如果未安装）
pip install kagglehub

# 测试
python -c "import kagglehub; print('✓ 配置成功')"
```

---

## 📝 环境变量方式（适合 CI/CD）

如果你使用环境变量，可以这样设置：

### Linux/Mac

```bash
# 临时设置（当前终端）
export KAGGLE_API_TOKEN=your_token_here

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export KAGGLE_API_TOKEN=your_token_here' >> ~/.bashrc
source ~/.bashrc
```

### Windows

```cmd
# 临时设置
set KAGGLE_API_TOKEN=your_token_here

# 永久设置（系统环境变量）
# 1. 右键"此电脑" -> 属性
# 2. 高级系统设置 -> 环境变量
# 3. 添加新变量：KAGGLE_API_TOKEN = your_token_here
```

---

## 🎯 使用自动下载脚本

配置完成后，使用自动下载脚本：

```bash
# 进入项目目录
cd /path/to/project

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 运行下载脚本
cd climate/code
python download_data.py
```

脚本会自动下载：
- ✅ 温度数据（Berkeley Earth）
- ✅ CO2 排放数据
- ✅ 海平面数据

---

## ⚠️ 常见问题

### 问题1：`ModuleNotFoundError: No module named 'kagglehub'`

**解决方案**：
```bash
pip install kagglehub
```

### 问题2：`401 - Unauthorized` 或 `403 - Forbidden`

**可能原因**：
- Token 已过期或无效
- Token 权限不足

**解决方案**：
1. 重新创建 API Token
2. 确保账号已登录
3. 检查 token 是否正确配置

### 问题3：`FileNotFoundError: kaggle.json`

**解决方案**：
```bash
# 检查文件是否存在
ls -la ~/.kaggle/kaggle.json

# 如果不存在，重新配置
python climate/code/setup_kaggle.py
```

### 问题4：`Permission denied`

**解决方案**：
```bash
# 设置正确的文件权限
chmod 600 ~/.kaggle/kaggle.json
```

### 问题5：下载速度慢

**解决方案**：
- 检查网络连接
- 使用 VPN（如果在中国大陆）
- 尝试在非高峰时段下载

---

## 🔒 安全提示

### ⚠️ 重要：不要提交 API Token 到 Git

1. **已自动保护**
   - `.gitignore` 已配置忽略所有 token 文件
   - `~/.kaggle/kaggle.json` 不会被提交

2. **如果误提交了 token**
   ```bash
   # 从 Git 历史中删除
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch ~/.kaggle/kaggle.json" \
     --prune-empty --tag-name-filter cat -- --all
   
   # 重新创建 token（如果已泄露）
   ```

3. **最佳实践**
   - 使用环境变量而不是文件
   - 定期更新 token
   - 不要分享 token 给他人

---

## 📚 相关资源

- **Kaggle API 文档**: https://www.kaggle.com/docs/api
- **kagglehub 文档**: https://github.com/Kaggle/kagglehub
- **项目下载脚本**: `climate/code/download_data.py`
- **配置脚本**: `climate/code/setup_kaggle.py`

---

## ✅ 配置检查清单

完成配置后，请确认：

- [ ] Kaggle 账号已登录
- [ ] API Token 已创建
- [ ] Token 已配置（环境变量或 kaggle.json）
- [ ] kagglehub 已安装 (`pip install kagglehub`)
- [ ] 文件权限正确（如果使用 kaggle.json）
- [ ] 测试下载脚本成功运行

---

## 🆘 需要帮助？

如果遇到问题：

1. 查看错误信息
2. 检查上述常见问题
3. 查看 Kaggle API 文档
4. 联系项目维护者

---

**配置完成后，就可以使用 `python download_data.py` 自动下载所有数据了！** 🎉

