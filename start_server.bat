@echo off
chcp 65001 >nul
cls
title 塔罗AI服务器启动工具
color 0A

 echo ==============================================
 echo     塔罗AI服务器启动工具
==============================================

REM 检查.env文件是否存在
if not exist .env (
    echo ❌ 错误: 未找到.env文件
    echo 请确保已复制.env.example为.env并配置API密钥
    pause
    exit /b 1
)

echo ✅ .env文件已找到

REM 检查API密钥是否已配置
for /f "tokens=2 delims==" %%a in ('findstr /i "TAROT_API_KEY" .env') do set "API_KEY=%%a"
if "%API_KEY%"=="" (
    echo ❌ 错误: API密钥未配置
    echo 请编辑.env文件，将TAROT_API_KEY设置为你的实际API密钥
    pause
    exit /b 1
)

if "%API_KEY%"=="your_actual_api_key_here" (
    echo ❌ 错误: API密钥仍为默认占位符
    echo 请编辑.env文件，将TAROT_API_KEY设置为你的实际API密钥
    pause
    exit /b 1
)

echo ✅ API密钥已配置

REM 检查Python环境
 echo 正在检查Python环境...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ 未检测到Python，请确保已安装Python
        pause
        exit /b 1
    ) else (
        set "PY_CMD=python"
    )
) else (
    set "PY_CMD=py"
)

echo ✅ Python已安装 (使用%PY_CMD%命令)

REM 安装依赖
 echo 正在安装依赖...
%PY_CMD% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败，请检查网络连接并重试
    pause
    exit /b 1
)

echo ✅ 依赖已安装

REM 启动服务器
 echo 正在启动服务器...
echo 调试信息: 执行命令: %PY_CMD% server.py

REM 创建一个日志文件来捕获错误
%PY_CMD% server.py > server_start.log 2>&1
if %errorlevel% neq 0 (
    echo ❌ 服务器启动失败!
    echo 请查看server_start.log文件获取详细错误信息
    pause
    exit /b 1
)

REM 如果服务器成功启动，这部分代码通常不会执行到
REM 因为服务器会在前台运行直到被中断

echo ✅ 服务器已成功启动
 echo 请访问 http://localhost:5000 来使用塔罗AI服务
 echo 如需停止服务器，请按 Ctrl+C
pause

exit /b 0
if %errorlevel% neq 0 (
    echo ❌ 服务器启动失败
    echo 错误代码: %errorlevel%
    echo 请检查以下事项:
    echo 1. API密钥是否正确
    echo 2. 网络连接是否正常
    echo 3. 端口5000是否被占用
    pause
    exit /b 1
)

pause