"""
数据模型测试
"""

import unittest
from poetry_app import create_app, db
from poetry_app.models.poetry import Poetry

class TestPoetryModel(unittest.TestCase):
    """诗词模型测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """测试后清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_poetry(self):
        """测试创建诗词"""
        poetry = Poetry(
            title='测试诗词',
            content='这是一首测试诗词',
            author='测试作者'
        )
        db.session.add(poetry)
        db.session.commit()
        
        self.assertEqual(poetry.title, '测试诗词')
        self.assertEqual(poetry.content, '这是一首测试诗词')
        self.assertEqual(poetry.author, '测试作者')
        self.assertIsNotNone(poetry.id)
    
    def test_poetry_to_dict(self):
        """测试诗词转字典"""
        poetry = Poetry(
            title='测试诗词',
            content='这是一首测试诗词',
            author='测试作者'
        )
        db.session.add(poetry)
        db.session.commit()
        
        poetry_dict = poetry.to_dict()
        self.assertEqual(poetry_dict['title'], '测试诗词')
        self.assertEqual(poetry_dict['content'], '这是一首测试诗词')
        self.assertEqual(poetry_dict['author'], '测试作者')
        self.assertIsNotNone(poetry_dict['id'])

if __name__ == '__main__':
    unittest.main()
