# 🚨 高危漏洞快速修复指南

## 立即修复步骤（5分钟内完成）

### 1. 设置环境变量
```bash
# Windows命令行
set TAROT_API_KEY=your_actual_api_key_here
set DEBUG=False

# Windows PowerShell
$env:TAROT_API_KEY="your_actual_api_key_here"
$env:DEBUG="False"

# 永久设置（Windows）
setx TAROT_API_KEY "your_actual_api_key_here"
setx DEBUG "False"
```

### 2. 安装安全依赖
```bash
pip install flask-limiter
```

### 3. 启动安全服务器
```bash
python server.py
```

## 验证修复效果

### 测试API密钥保护
```bash
curl -X POST http://localhost:5000/api/tarot \
  -H "Content-Type: application/json" \
  -d '{"prompt":"测试"}'
```

### 测试输入验证
```bash
curl -X POST http://localhost:5000/api/tarot \
  -H "Content-Type: application/json" \
  -d '{"prompt":"<script>alert(1)</script>"}'
```

### 测试速率限制
```bash
# 快速发送多个请求，应该触发429错误
for i in {1..10}; do curl -X POST http://localhost:5000/api/tarot -H "Content-Type: application/json" -d '{"prompt":"测试"}'; done
```

## 常见问题

### Q: 启动时报错 "No module named 'flask_limiter'"
A: 运行：
```bash
pip install flask-limiter
```

### Q: 环境变量设置后不生效
A: Windows需要重启命令行窗口，或运行：
```bash
python -c "import os; print(os.environ.get('TAROT_API_KEY'))"
```

### Q: 前端显示跨域错误
A: 确保使用正确的本地地址：
- http://localhost:5000
- http://127.0.0.1:5000

## 安全验证清单

- [ ] API密钥已从代码中移除
- [ ] 环境变量已正确设置
- [ ] 输入验证正常工作
- [ ] 错误信息不再泄露敏感信息
- [ ] 速率限制已启用
- [ ] 调试模式已关闭

## 下一步：完整安全加固

完成快速修复后，建议：
1. 使用 `server_secure.py` 替换 `server.py`（已包含更多安全特性）
2. 配置HTTPS证书
3. 设置日志监控
4. 定期更新依赖

## 紧急联系

如果遇到问题：
1. 检查控制台错误信息
2. 查看app.log日志文件
3. 确保所有依赖已安装