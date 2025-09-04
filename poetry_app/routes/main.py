"""
主页面路由
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from poetry_app.services.poetry_service import PoetryService

main_bp = Blueprint('main', __name__)
poetry_service = PoetryService()

@main_bp.route('/')
def index():
    """首页 - 显示所有诗词"""
    search_keyword = request.args.get('search', '')
    
    if search_keyword:
        poems = poetry_service.search_poems(search_keyword)
    else:
        poems = poetry_service.get_all_poems()
    
    return render_template('index.html', poems=poems, search_keyword=search_keyword)

@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main_bp.route('/api-status')
def api_status():
    """API状态检查页面"""
    return render_template('api_status.html')
