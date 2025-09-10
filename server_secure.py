from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import logging
import os
from datetime import datetime
import re

app = Flask(__name__)

# 安全配置
CORS(app, origins=[
    'http://localhost:3000',
    'http://localhost:5000', 
    'https://tarot-ai.example.com'  # 替换为你的实际域名
])

# 速率限制
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# 配置加载
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-default-secret-key')
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
app.config['PORT'] = int(os.getenv('PORT', 5000))

# 魔搭社区API端点
API_ENDPOINT = "https://api.modelscope.cn/api/v1/chat/completions"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 从环境变量获取API密钥
API_KEY = os.environ.get('TAROT_API_KEY')
if not API_KEY:
    logger.error("TAROT_API_KEY environment variable not set")
    raise ValueError("API密钥未配置")

API_ENDPOINT = 'https://api.siliconflow.cn/v1/chat/completions'

# 输入验证函数
def validate_input(data):
    """验证用户输入"""
    if not data or 'prompt' not in data:
        return False, "缺少必要的prompt字段"
    
    prompt = data['prompt']
    
    # 检查prompt长度
    if len(prompt) > 1000:
        return False, "问题过长，请控制在1000字符以内"
    
    # 检查敏感词汇
    sensitive_words = ['暴力', '自杀', '仇恨', '攻击']
    for word in sensitive_words:
        if word in prompt.lower():
            logger.warning(f"检测到敏感词汇: {word}")
            return False, "问题包含不当内容"
    
    # 清理输入
    cleaned_prompt = re.sub(r'[<>"\']', '', prompt)
    
    return True, cleaned_prompt

@app.route('/api/tarot', methods=['POST'])
@limiter.limit("5 per minute")  # 更严格的速率限制
def get_tarot_reading():
    try:
        data = request.json
        logger.info(f"收到来自 {request.remote_addr} 的请求")
        
        # 验证输入
        is_valid, result = validate_input(data)
        if not is_valid:
            return jsonify({'error': result}), 400
        
        cleaned_prompt = result
        
        # 构建请求体
        request_body = {
            "model": "deepseek-ai/DeepSeek-R1-0528",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位经验丰富的塔罗牌解读师，擅长通过塔罗牌为人们提供洞察和指导。请用中文回答，避免涉及政治、暴力等敏感话题。"
                },
                {
                    "role": "user",
                    "content": cleaned_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1500  # 限制响应长度
        }
        
        # 发送请求到API
        response = requests.post(
            API_ENDPOINT,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json=request_body,
            timeout=30  # 设置超时
        )
        
        if response.status_code != 200:
            logger.error(f"API请求失败: {response.status_code}")
            return jsonify({
                'error': '服务暂时不可用，请稍后再试'
            }), 500
        
        response_data = response.json()
        
        # 记录成功请求
        logger.info(f"成功处理请求，响应长度: {len(str(response_data))}")
        
        return jsonify(response_data)
        
    except requests.Timeout:
        logger.error("API请求超时")
        return jsonify({'error': '请求超时，请稍后再试'}), 504
    except Exception as e:
        logger.error(f'服务器错误: {str(e)}', exc_info=True)
        return jsonify({'error': '服务器内部错误，请稍后再试'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': '请求过于频繁，请稍后再试'}), 429

@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({'error': '请求的接口不存在'}), 404

@app.errorhandler(500)
def internal_error_handler(e):
    logger.error(f'未处理的错误: {str(e)}', exc_info=True)
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 生产环境配置
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        ssl_context='adhoc'  # 启用HTTPS（需要安装pyopenssl）
    )