"""
诗词数据模型
"""

from datetime import datetime
from poetry_app import db

class Poetry(db.Model):
    """诗词模型"""
    __tablename__ = 'poetry'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='诗词标题')
    content = db.Column(db.Text, nullable=False, comment='诗词内容')
    author = db.Column(db.String(100), default='匿名', comment='作者')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    image_path = db.Column(db.String(500), comment='配图路径')
    image_prompt = db.Column(db.Text, comment='图片生成提示词')
    
    def __repr__(self):
        return f'<Poetry {self.title}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'image_path': self.image_path,
            'image_prompt': self.image_prompt
        }
    
    @classmethod
    def get_recent_poems(cls, limit=10):
        """获取最近的诗词"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def search_by_title(cls, keyword):
        """根据标题搜索诗词"""
        return cls.query.filter(cls.title.contains(keyword)).all()
    
    @classmethod
    def search_by_author(cls, author):
        """根据作者搜索诗词"""
        return cls.query.filter(cls.author.contains(author)).all()
