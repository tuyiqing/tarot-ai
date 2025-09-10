# 神秘塔罗占卜网站

## 项目概述
这是一个使用HTML5和CSS开发的塔罗牌占卜网站，集成了SiliconFlow API来提供智能化的塔罗牌解读。网站设计精美，具有丰富的动画效果和响应式布局，为用户提供沉浸式的塔罗牌占卜体验。

## 项目结构
- `index.html`: 网站首页
- `css/style.css`: 主样式表
- `js/main.js`: 主要JavaScript逻辑
- `js/api.js`: SiliconFlow API集成
- `js/api_secure.js`: 安全增强的API客户端
- `images/`: 存放塔罗牌图片和网站素材
- `server.py`: Flask后端服务
- `server_secure.py`: 安全增强的后端服务
- `start_server.bat`: Windows一键启动脚本
- `requirements.txt`: Python依赖列表
- `.env`: 环境变量配置文件（需手动创建）
- `.env.example`: 环境变量配置示例

## 功能说明
1. 多种塔罗牌阵选择（单卡、三卡、凯尔特十字、关系、职业）
2. 交互式抽牌体验（包含洗牌、切牌动画）
3. AI驱动的塔罗牌解读
4. 响应式设计，适配各种设备
5. 本地保存占卜结果
6. 详细的卡牌解释和含义展示
7. 输入验证和安全性保障
8. 速率限制防止滥用

## 塔罗牌阵说明
1. 单卡牌阵：适合快速了解某个具体问题的答案
2. 三卡牌阵：过去、现在、未来的简单解读
3. 凯尔特十字牌阵：全面分析复杂问题的各个方面
4. 关系牌阵：专注于人际关系分析
5. 职业发展牌阵：针对职业和事业发展的专门解读

## 技术实现
- 使用HTML5、CSS3和JavaScript构建前端界面
- 集成DeepSeek AI API进行智能解读
- 使用CSS动画实现洗牌和抽牌特效
- 响应式设计确保在各种设备上的良好体验

## 快速开始

### 前提条件
- 已安装Python 3.8或更高版本
- 已获取SiliconFlow API密钥（格式为sk-开头）

### 方法一：一键启动（Windows）
1. 确保已在`.env`文件中正确配置API密钥
2. 双击`start_server.bat`文件
3. 打开浏览器访问 http://localhost:5000

### 方法二：手动配置

#### 步骤1：创建.env文件
1. 复制`.env.example`文件并重命名为`.env`
2. 用文本编辑器打开`.env`文件
3. 填入您的SiliconFlow API密钥和其他配置：
```
# API配置
TAROT_API_KEY=sk-你的实际API密钥

# 服务器配置
PORT=5000
DEBUG=False
SECRET_KEY=任意随机字符串

# 允许的CORS域名（逗号分隔）
ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
```

#### 步骤2：安装依赖
打开命令行窗口，执行以下命令：
```bash
cd /d "c:\Users\tuyiqing\Desktop\tarot-ai"
pip install -r requirements.txt
```

#### 步骤3：启动服务器
```bash
python server.py
```

## 使用说明
1. 打开网站首页 http://localhost:5000
2. 点击"开始占卜之旅"按钮
3. 选择适合您问题的牌阵类型
4. 输入您想要解答的问题
5. 点击牌堆抽取塔罗牌
6. 查看AI提供的详细解读
7. 可以保存或分享您的占卜结果

## 注意事项
- 首次使用时，请确保您的浏览器已启用JavaScript
- 为获得最佳体验，建议使用最新版本的Chrome、Firefox或Safari浏览器
- 网站需要连接互联网才能获取AI解读
- 塔罗牌解读仅供娱乐和参考，重要决策请依靠您自己的判断
- API密钥请妥善保管，不要泄露给他人

## 常见问题解决

### 问题1：pip命令找不到
**解决**：先安装Python，确保勾选"Add Python to PATH"选项

### 问题2：端口被占用
**解决**：修改.env文件中的PORT值，如改为8080

### 问题3：API密钥无效
**解决**：检查SiliconFlow API密钥格式是否正确（sk-开头）

### 问题4：启动脚本闪退
**解决**：右键点击start_server.bat文件，选择"编辑"查看具体错误信息

## 未来计划
- 添加更多类型的牌阵
- 提供更详细的塔罗牌知识库
- 增加用户账户系统，保存历史占卜记录
- 优化移动端体验
- 添加更多语言支持

## 安全提示
- 请定期检查`.env`文件的访问权限
- 不要将包含API密钥的代码提交到公共仓库
- 如发现安全问题，请参考`SECURITY.md`文件中的应急响应流程

# 智能塔罗牌解读系统

一个结合现代设计和 AI 技术的塔罗牌解读网站。

## 功能特点

- 精美的塔罗牌设计
- AI 驱动的专业解读
- 流畅的动画效果
- 多种牌阵选择
- 响应式设计

## 技术栈

- 前端：HTML5, CSS3, JavaScript
- 后端：Python, Flask
- AI：DeepSeek AI API

## 在线体验

访问 [https://zjj0619.github.io/tarot-ai/](https://zjj0619.github.io/tarot-ai/) 开始您的塔罗之旅。

## 本地开发

1. 克隆仓库
```bash
git clone https://github.com/zjj0619/tarot-ai.git
cd tarot-ai
```

2. 启动后端服务
```bash
python server.py
```

3. 启动前端服务
```bash
python -m http.server 8000
```

4. 访问 http://localhost:8000

## 许可证

MIT License