"""
诗词相关路由
"""

from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash, jsonify
from poetry_app.services.poetry_service import PoetryService
from poetry_app import db
import os

poetry_bp = Blueprint('poetry', __name__)
poetry_service = PoetryService()

@poetry_bp.route('/create', methods=['GET', 'POST'])
def create():
    """创建新诗词"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '匿名').strip()
        
        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return render_template('poetry/create.html')
        
        try:
            # 创建诗词
            poetry = poetry_service.create_poetry(title, content, author)
            db.session.add(poetry)
            db.session.commit()
            
            # 检查是否成功生成配图
            if poetry.image_path:
                flash('诗词创建成功！配图已生成。', 'success')
            else:
                flash('诗词创建成功！但配图生成失败，可能是API配额限制。', 'warning')
            
            return redirect(url_for('poetry.view', id=poetry.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建诗词失败: {str(e)}', 'error')
            return render_template('poetry/create.html')
    
    return render_template('poetry/create.html')

@poetry_bp.route('/<int:id>')
def view(id):
    """查看单个诗词"""
    poetry = poetry_service.get_poetry_by_id(id)
    if not poetry:
        flash('诗词不存在', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('poetry/view.html', poetry=poetry)

@poetry_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """编辑诗词"""
    poetry = poetry_service.get_poetry_by_id(id)
    if not poetry:
        flash('诗词不存在', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '匿名').strip()
        
        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return render_template('poetry/edit.html', poetry=poetry)
        
        try:
            # 更新诗词
            if poetry_service.update_poetry(poetry, title, content, author):
                db.session.commit()
                flash('诗词更新成功！', 'success')
                return redirect(url_for('poetry.view', id=poetry.id))
            else:
                flash('更新诗词失败', 'error')
                
        except Exception as e:
            db.session.rollback()
            flash(f'更新诗词失败: {str(e)}', 'error')
    
    return render_template('poetry/edit.html', poetry=poetry)

@poetry_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """删除诗词"""
    poetry = poetry_service.get_poetry_by_id(id)
    if not poetry:
        flash('诗词不存在', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # 删除诗词
        if poetry_service.delete_poetry(poetry):
            db.session.delete(poetry)
            db.session.commit()
            flash('诗词删除成功！', 'success')
        else:
            flash('删除诗词失败', 'error')
            
    except Exception as e:
        db.session.rollback()
        flash(f'删除诗词失败: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@poetry_bp.route('/<int:id>/download')
def download_image(id):
    """下载图片"""
    poetry = poetry_service.get_poetry_by_id(id)
    if not poetry or not poetry.image_path:
        flash('图片不存在', 'error')
        return redirect(url_for('main.index'))
    
    image_path = os.path.join(os.getcwd(), 'static', 'images', poetry.image_path)
    if not os.path.exists(image_path):
        flash('图片文件不存在', 'error')
        return redirect(url_for('main.index'))
    
    return send_file(
        image_path, 
        as_attachment=True, 
        download_name=f"{poetry.title}_配图.jpg",
        mimetype='image/jpeg'
    )

@poetry_bp.route('/<int:id>/regenerate-image', methods=['POST'])
def regenerate_image(id):
    """重新生成图片"""
    poetry = poetry_service.get_poetry_by_id(id)
    if not poetry:
        return jsonify({'error': '诗词不存在'}), 404
    
    try:
        # 重新生成配图
        poetry_service._regenerate_image(poetry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '图片重新生成成功',
            'image_path': poetry.image_path
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'重新生成图片失败: {str(e)}'}), 500
