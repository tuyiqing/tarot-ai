# 塔罗AI网站安全指南

## 🔐 安全最佳实践

### 1. 环境变量配置

在生产环境部署前，请完成以下配置：

#### 设置环境变量
```bash
# Linux/Mac
export TAROT_API_KEY="your_actual_api_key_here"
export SECRET_KEY="your_very_secret_key_here"
export DEBUG="False"
export PORT="5000"

# Windows
set TAROT_API_KEY=your_actual_api_key_here
set SECRET_KEY=your_very_secret_key_here
set DEBUG=False
set PORT=5000
```

#### 创建 .env 文件
复制 `.env.example` 为 `.env` 并填入实际值：
```bash
cp .env.example .env
# 编辑 .env 文件填入你的配置
```

### 2. 依赖安装

安装安全增强的依赖：
```bash
pip install flask-limiter python-dotenv cryptography
```

### 3. 部署安全检查清单

#### ✅ 部署前检查
- [ ] 已设置 `TAROT_API_KEY` 环境变量
- [ ] 已设置 `SECRET_KEY` 环境变量（至少32位随机字符串）
- [ ] 已禁用调试模式 (`DEBUG=False`)
- [ ] 已配置正确的CORS域名
- [ ] 已启用HTTPS
- [ ] 已设置防火墙规则
- [ ] 已配置日志轮转

#### ✅ 运行安全检查
```bash
# 检查环境变量
echo $TAROT_API_KEY | wc -c  # 应该显示密钥长度

# 检查端口监听
netstat -tlnp | grep :5000

# 检查HTTPS证书
openssl s_client -connect yourdomain.com:443
```

### 4. 监控和日志

#### 日志文件位置
- 应用日志：`app.log`
- 访问日志：Flask默认日志
- 错误日志：系统日志

#### 监控指标
- API响应时间
- 错误率
- 请求频率
- 内存使用率

### 5. 定期安全更新

#### 每月检查
- [ ] 更新所有依赖包
- [ ] 检查API密钥有效性
- [ ] 审查访问日志
- [ ] 测试备份恢复

#### 每季度检查
- [ ] 轮换密钥
- [ ] 安全审计
- [ ] 性能优化
- [ ] 备份策略测试

### 6. 应急响应

#### 发现安全事件时
1. 立即禁用API密钥
2. 检查访问日志
3. 通知相关方
4. 更新密钥和配置
5. 重新部署服务

#### 联系信息
- 技术支持：[你的邮箱]
- 紧急联系：[紧急联系方式]

### 7. 安全测试

#### 自动化测试
```bash
# 运行安全测试
python -m pytest tests/security/

# 漏洞扫描
pip install safety
safety check
```

#### 手动测试
1. 尝试SQL注入：`test'; DROP TABLE users; --`
2. 尝试XSS攻击：`<script>alert('XSS')</script>`
3. 测试速率限制：快速连续发送请求
4. 测试输入验证：超长字符串、特殊字符

### 8. 备份策略

#### 数据备份
- 每日自动备份用户数据
- 每周完整系统备份
- 每月异地备份

#### 密钥管理
- 使用密钥管理服务
- 定期轮换密钥
- 密钥分级管理

### 9. 合规要求

#### 数据保护
- 遵守GDPR/CCPA等隐私法规
- 用户数据加密存储
- 提供数据删除功能

#### 审计要求
- 保留访问日志6个月
- 定期安全审计报告
- 合规性检查清单

---

## 🆘 遇到问题？

### 常见问题解决

#### Q: 启动时报错 "API密钥未配置"
A: 检查环境变量 `TAROT_API_KEY` 是否正确设置

#### Q: 前端显示 "跨域请求被阻止"
A: 检查CORS配置是否包含你的前端域名

#### Q: 请求返回 "429 Too Many Requests"
A: 这是速率限制触发，请降低请求频率

#### Q: 日志文件过大
A: 配置日志轮转：`pip install logrotate`

### 技术支持
如有安全问题，请通过以下方式联系：
- 邮箱：[你的技术支持邮箱]
- 文档：[项目文档链接]
- 社区：[技术支持论坛]