"""
诗歌创作平台 - Flask应用包
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# 初始化扩展
db = SQLAlchemy()

def create_app(config_class=Config):
    """应用工厂函数"""
    import os
    # 获取项目根目录
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    
    # 确保上传文件夹存在
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 注册蓝图
    from poetry_app.routes.main import main_bp
    from poetry_app.routes.poetry import poetry_bp
    from poetry_app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(poetry_bp, url_prefix='/poetry')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
