#!/usr/bin/env python3
"""
诗歌创作平台主启动文件
"""

import os
import sys
from poetry_app import create_app, db

# 加载.env文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有python-dotenv，手动加载.env文件
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def main():
    """主函数"""
    print("🎨 诗歌创作平台启动中...")
    
    # 检查环境变量
    if not os.environ.get('GEMINI_API_KEY'):
        print("⚠️  警告: 未设置 GEMINI_API_KEY 环境变量")
        print("   请设置环境变量或创建 .env 文件")
        print("   参考 env_example.txt 文件")
    
    # 创建应用
    app = create_app()
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        print("✅ 数据库初始化完成")
    
    # 启动应用
    print("🚀 应用启动成功!")
    print("📱 访问地址: http://localhost:5000")
    print("🛑 按 Ctrl+C 停止服务")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")

if __name__ == '__main__':
    main()
