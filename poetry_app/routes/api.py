"""
API接口路由
"""

from flask import Blueprint, jsonify, request
from poetry_app.services.poetry_service import PoetryService
from poetry_app.models.poetry import Poetry

api_bp = Blueprint('api', __name__)
poetry_service = PoetryService()

@api_bp.route('/poems')
def get_poems():
    """获取所有诗词的JSON数据"""
    try:
        poems = poetry_service.get_all_poems()
        return jsonify({
            'success': True,
            'data': [poem.to_dict() for poem in poems],
            'count': len(poems)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/poems/<int:id>')
def get_poem(id):
    """获取单个诗词的JSON数据"""
    try:
        poetry = poetry_service.get_poetry_by_id(id)
        if not poetry:
            return jsonify({
                'success': False,
                'error': '诗词不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': poetry.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/poems/search')
def search_poems():
    """搜索诗词"""
    try:
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({
                'success': False,
                'error': '搜索关键词不能为空'
            }), 400
        
        poems = poetry_service.search_poems(keyword)
        return jsonify({
            'success': True,
            'data': [poem.to_dict() for poem in poems],
            'count': len(poems),
            'keyword': keyword
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/poems/recent')
def get_recent_poems():
    """获取最近的诗词"""
    try:
        limit = request.args.get('limit', 10, type=int)
        poems = Poetry.get_recent_poems(limit)
        
        return jsonify({
            'success': True,
            'data': [poem.to_dict() for poem in poems],
            'count': len(poems)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/stats')
def get_stats():
    """获取统计信息"""
    try:
        total_poems = Poetry.query.count()
        total_authors = Poetry.query.with_entities(Poetry.author).distinct().count()
        poems_with_images = Poetry.query.filter(Poetry.image_path.isnot(None)).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_poems': total_poems,
                'total_authors': total_authors,
                'poems_with_images': poems_with_images,
                'image_coverage': round(poems_with_images / total_poems * 100, 2) if total_poems > 0 else 0
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
