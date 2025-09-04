"""
诗词业务逻辑服务
"""

import os
from poetry_app.models.poetry import Poetry
from poetry_app.services.ai_service import AIImageService
from flask import current_app

class PoetryService:
    """诗词服务类"""
    
    def __init__(self):
        self.ai_service = AIImageService()
    
    def create_poetry(self, title, content, author='匿名'):
        """
        创建新诗词
        
        Args:
            title (str): 诗词标题
            content (str): 诗词内容
            author (str): 作者
            
        Returns:
            Poetry: 创建的诗词对象
        """
        # 创建诗词记录
        poetry = Poetry(title=title, content=content, author=author)
        
        # 生成配图
        try:
            image_filename = self.ai_service.generate_image_from_poetry(content, title)
            if image_filename:
                poetry.image_path = image_filename
                poetry.image_prompt = f"根据诗词《{title}》生成"
        except Exception as e:
            current_app.logger.error(f"生成配图失败: {e}")
        
        return poetry
    
    def update_poetry(self, poetry, title, content, author):
        """
        更新诗词
        
        Args:
            poetry (Poetry): 诗词对象
            title (str): 新标题
            content (str): 新内容
            author (str): 新作者
            
        Returns:
            bool: 是否成功更新
        """
        try:
            # 更新基本信息
            poetry.title = title
            poetry.content = content
            poetry.author = author
            
            # 重新生成配图
            self._regenerate_image(poetry)
            
            return True
        except Exception as e:
            current_app.logger.error(f"更新诗词失败: {e}")
            return False
    
    def delete_poetry(self, poetry):
        """
        删除诗词
        
        Args:
            poetry (Poetry): 诗词对象
            
        Returns:
            bool: 是否成功删除
        """
        try:
            # 删除图片文件
            if poetry.image_path:
                self._delete_image_file(poetry.image_path)
            
            return True
        except Exception as e:
            current_app.logger.error(f"删除诗词失败: {e}")
            return False
    
    def _regenerate_image(self, poetry):
        """重新生成配图"""
        try:
            # 删除旧图片
            if poetry.image_path:
                self._delete_image_file(poetry.image_path)
            
            # 生成新图片
            image_filename = self.ai_service.generate_image_from_poetry(
                poetry.content, poetry.title
            )
            if image_filename:
                poetry.image_path = image_filename
                poetry.image_prompt = f"根据诗词《{poetry.title}》重新生成"
        except Exception as e:
            current_app.logger.error(f"重新生成配图失败: {e}")
    
    def _delete_image_file(self, image_path):
        """删除图片文件"""
        if image_path:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
                current_app.logger.info(f"已删除图片文件: {image_path}")
    
    @staticmethod
    def get_poetry_by_id(poetry_id):
        """根据ID获取诗词"""
        return Poetry.query.get(poetry_id)
    
    @staticmethod
    def get_all_poems():
        """获取所有诗词"""
        return Poetry.query.order_by(Poetry.created_at.desc()).all()
    
    @staticmethod
    def search_poems(keyword):
        """搜索诗词"""
        return Poetry.query.filter(
            Poetry.title.contains(keyword) | 
            Poetry.content.contains(keyword) |
            Poetry.author.contains(keyword)
        ).order_by(Poetry.created_at.desc()).all()
