@echo off
chcp 65001 >nul
cls
title 塔罗AI服务器测试工具
color 0A

rem 显示当前环境变量
echo 当前环境变量:
echo ---------------------------
echo %PATH%
echo ---------------------------

echo 检查Python版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python命令
    pause
    exit /b 1
)

py --version
if %errorlevel% neq 0 (
    echo ❌ 未检测到py命令
    echo 但已检测到python命令，将使用python
)

rem 设置PY_CMD变量
set "PY_CMD=python"

echo 检查Python包...
%PY_CMD% -m pip list

echo 检查requirements.txt文件...
if exist requirements.txt (
    echo ✅ requirements.txt文件存在
    type requirements.txt
) else (
    echo ❌ requirements.txt文件不存在
    echo 创建临时requirements.txt文件...
    echo flask==2.3.2 > requirements.txt
    echo flask-limiter==3.3.1 >> requirements.txt
    echo python-dotenv==1.0.0 >> requirements.txt
    echo requests==2.31.0 >> requirements.txt
    echo flask-cors==4.0.0 >> requirements.txt
)

rem 安装依赖
%PY_CMD% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo 依赖安装成功，尝试启动服务器...

echo 检查.env文件...
if exist .env (
    echo ✅ .env文件存在
    echo 环境变量配置:
    type .env
) else (
    echo ❌ .env文件不存在
    pause
    exit /b 1
)

echo 正在启动服务器...
echo 启动命令: %PY_CMD% -m flask run --host=0.0.0.0 --port=5000

rem 尝试用flask命令直接启动
%PY_CMD% -m flask run --host=0.0.0.0 --port=5000 > server_test.log 2>&1
if %errorlevel% neq 0 (
    echo ❌ 使用flask命令启动失败
    echo 尝试使用python server.py命令启动...
    %PY_CMD% server.py > server_test.log 2>&1
    if %errorlevel% neq 0 (
        echo ❌ 服务器启动失败!
        echo 请查看server_test.log文件获取详细错误信息
        type server_test.log
        pause
        exit /b 1
    )
)

echo ✅ 服务器启动成功
pause
exit /b 0