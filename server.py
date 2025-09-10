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

# 安全配置 - 从环境变量读取
CORS(app, origins=[
    'http://localhost:3000',
    'http://localhost:5000', 
    'http://127.0.0.1:5000',
    'http://127.0.0.1:3000'
])

# 速率限制
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取API密钥
API_KEY = os.environ.get('TAROT_API_KEY')
if not API_KEY:
    logger.error("⚠️ 警告: TAROT_API_KEY 环境变量未设置")
    API_KEY = 'placeholder_key'  # 临时占位符

# 魔搭社区API端点
API_ENDPOINT = 'https://api.modelscope.cn/api/v1/chat/completions'

# 输入验证函数
def validate_input(data):
    """验证用户输入"""
    if not data or 'prompt' not in data:
        return False, "缺少必要的prompt字段"
    
    prompt = str(data.get('prompt', ''))
    
    # 检查prompt长度
    if len(prompt) > 1000:
        return False, "问题过长，请控制在1000字符以内"
    
    # 检查敏感词汇
    sensitive_words = ['暴力', '自杀', '仇恨', '攻击', 'kill', 'hate', 'bomb']
    prompt_lower = prompt.lower()
    for word in sensitive_words:
        if word in prompt_lower:
            logger.warning(f"检测到敏感词汇: {word}")
            return False, "问题包含不当内容，请重新表述"
    
    # 清理输入
    cleaned_prompt = re.sub(r'[<>"\']', '', prompt).strip()
    if not cleaned_prompt:
        return False, "问题内容不能为空"
    
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
            logger.warning(f"输入验证失败: {result}")
            return jsonify({'error': result}), 400
        
        cleaned_prompt = result
        
        # 检查API密钥是否为占位符
        if API_KEY == 'placeholder_key':
            logger.error("API密钥未配置")
            return jsonify({
                'error': '服务配置错误，请联系管理员'
            }), 500
        
        # 构建请求体
        request_body = {
            "model": "deepseek-ai/DeepSeek-R1-0528",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位经验丰富的塔罗牌解读师，擅长通过塔罗牌为人们提供洞察和指导。请用中文回答，避免涉及政治、暴力等敏感话题，保持回答积极建设性。"
                },
                {
                    "role": "user",
                    "content": cleaned_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1500  # 限制响应长度
        }
        
        # 发送请求到API（带超时）
        response = requests.post(
            API_ENDPOINT,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json=request_body,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"API请求失败: {response.status_code}")
            return jsonify({
                'error': '服务暂时不可用，请稍后再试'
            }), 500
        
        response_data = response.json()
        logger.info(f"成功处理请求")
        return jsonify(response_data)
        
    except requests.Timeout:
        logger.error("API请求超时")
        return jsonify({'error': '请求超时，请检查网络连接'}), 504
    except requests.RequestException as e:
        logger.error(f"网络请求错误: {str(e)}")
        return jsonify({'error': '网络连接错误，请稍后重试'}), 503
    except Exception as e:
        logger.error(f'服务器内部错误: {str(e)}', exc_info=True)
        return jsonify({'error': '服务器内部错误，请稍后再试'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': '请求过于频繁，请稍后再试'}), 429

@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({'error': '请求的接口不存在'}), 404

@app.errorhandler(500)
def internal_error_handler(e):
    logger.error(f'未处理的错误: {str(e)}')
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 生产环境配置
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    if debug_mode:
        logger.warning("⚠️ 警告: 调试模式已开启，仅用于开发环境")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
