"""
辅助工具函数
"""

from datetime import datetime
import re

def format_datetime(dt, format_str='%Y年%m月%d日 %H:%M'):
    """
    格式化日期时间
    
    Args:
        dt: datetime对象
        format_str: 格式字符串
        
    Returns:
        str: 格式化后的日期时间字符串
    """
    if not dt:
        return ''
    return dt.strftime(format_str)

def truncate_text(text, length=100, suffix='...'):
    """
    截断文本
    
    Args:
        text: 要截断的文本
        length: 最大长度
        suffix: 后缀
        
    Returns:
        str: 截断后的文本
    """
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    return text[:length] + suffix

def validate_poetry_data(title, content, author=''):
    """
    验证诗词数据
    
    Args:
        title: 标题
        content: 内容
        author: 作者
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, '标题不能为空'
    
    if not content or not content.strip():
        return False, '内容不能为空'
    
    if len(title.strip()) > 200:
        return False, '标题长度不能超过200个字符'
    
    if len(content.strip()) > 5000:
        return False, '内容长度不能超过5000个字符'
    
    if author and len(author.strip()) > 100:
        return False, '作者名称长度不能超过100个字符'
    
    return True, ''

def clean_text(text):
    """
    清理文本，移除多余的空白字符
    
    Args:
        text: 原始文本
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ''
    
    # 移除首尾空白
    text = text.strip()
    
    # 将多个连续空白字符替换为单个空格
    text = re.sub(r'\s+', ' ', text)
    
    # 将多个连续换行符替换为单个换行符
    text = re.sub(r'\n+', '\n', text)
    
    return text

def extract_keywords(text, max_keywords=5):
    """
    从文本中提取关键词
    
    Args:
        text: 文本内容
        max_keywords: 最大关键词数量
        
    Returns:
        list: 关键词列表
    """
    if not text:
        return []
    
    # 简单的关键词提取（可以后续优化为更复杂的算法）
    # 移除标点符号和数字
    clean_text = re.sub(r'[^\u4e00-\u9fff\w\s]', '', text)
    
    # 按空格和换行分割
    words = re.split(r'[\s\n]+', clean_text)
    
    # 过滤掉长度小于2的词
    words = [word for word in words if len(word) >= 2]
    
    # 统计词频
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    # 按词频排序并返回前N个
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]]
