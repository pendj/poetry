"""
AI图像生成服务
"""

import os
import uuid
import mimetypes
import time
import re
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types
from flask import current_app

# 加载.env文件
load_dotenv()

class AIImageService:
    """AI图像生成服务类"""
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.quota_exhausted = False
        self.last_quota_check = 0
        
        # 设置代理环境变量
        self._setup_proxy_environment()
        
        if not self.api_key:
            print("⚠️  警告: GEMINI_API_KEY 环境变量未设置，AI图像生成功能将不可用")
        else:
            print(f"✅ AI服务已初始化，API密钥已设置")
            proxy_info = self._get_proxy_info()
            if proxy_info:
                print(f"🌐 代理配置: {proxy_info}")
    
    def generate_image_from_poetry(self, poetry_content, poetry_title=None, max_retries=3):
        """
        根据诗词内容生成图片
        
        Args:
            poetry_content (str): 诗词内容
            poetry_title (str): 诗词标题
            max_retries (int): 最大重试次数
            
        Returns:
            str: 生成的图片文件名，失败返回None
        """
        if not self.api_key:
            current_app.logger.warning("AI图像生成功能不可用：未设置GEMINI_API_KEY")
            return None
        
        # 检查配额状态
        if self.quota_exhausted:
            current_time = time.time()
            # 如果距离上次检查超过1小时，重置配额状态
            if current_time - self.last_quota_check > 3600:
                self.quota_exhausted = False
                current_app.logger.info("配额状态已重置，尝试重新生成图片")
            else:
                current_app.logger.warning("API配额已用完，请稍后再试或升级API计划")
                return None
        
        for attempt in range(max_retries):
            try:
                result = self._generate_image_attempt(poetry_content, poetry_title)
                if result:
                    return result
                    
            except Exception as e:
                error_msg = str(e)
                current_app.logger.error(f"生成图片时出错 (尝试 {attempt + 1}/{max_retries}): {e}")
                
                # 检查是否是配额限制错误
                if self._is_quota_exceeded(error_msg):
                    if attempt < max_retries - 1:
                        retry_delay = self._get_retry_delay(error_msg)
                        current_app.logger.warning(f"配额限制，等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        current_app.logger.error("配额限制，已达到最大重试次数")
                        return None
                elif "API_KEY" in error_msg:
                    current_app.logger.error("Gemini API密钥无效或未设置")
                    return None
                else:
                    # 其他错误，不重试
                    return None
        
        return None
    
    def _generate_image_attempt(self, poetry_content, poetry_title):
        """单次生成图片尝试"""
        try:
            # 创建客户端，代理通过环境变量自动配置
            client = genai.Client(api_key=self.api_key)
            
            # 构建图片生成提示词
            prompt = self._build_prompt(poetry_content, poetry_title)
            
            model = "gemini-2.5-flash-image-preview"
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            )
            
            # 生成图片 - 参考ai_studio_code的流式处理逻辑
            file_index = 0
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                
                # 处理图片数据
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    
                    current_app.logger.info(f"收到图片数据块 {file_index}")
                    file_index += 1
                    return self._save_image(chunk.candidates[0].content.parts[0].inline_data)
                
                # 处理文本数据（如果有的话）
                elif hasattr(chunk, 'text') and chunk.text:
                    current_app.logger.info(f"收到文本响应: {chunk.text}")
            
            # 如果没有收到任何图片数据
            if file_index == 0:
                current_app.logger.warning("未收到任何图片数据")
                return None
                
        except Exception as e:
            # 重新抛出异常，让上层处理重试逻辑
            raise e
    
    def _build_prompt(self, poetry_content, poetry_title=None):
        """构建图片生成提示词"""
        title_part = f"《{poetry_title}》" if poetry_title else "这首诗词"
        
        prompt = f"""
        请根据以下诗词内容生成一幅美丽的图片：
        
        {title_part}
        {poetry_content}
        
        要求：
        1. 图片风格要符合诗词的意境和情感
        2. 色彩搭配要和谐，体现诗词的氛围
        3. 构图要优美，具有艺术感
        4. 如果是古典诗词，使用传统中国画风格
        5. 如果是现代诗词，使用现代艺术风格
        6. 图片要能传达诗词的核心情感
        """
        
        return prompt.strip()
    
    def _save_image(self, inline_data):
        """保存生成的图片"""
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        data_buffer = inline_data.data
        file_extension = mimetypes.guess_extension(inline_data.mime_type)
        
        if not file_extension:
            file_extension = '.png'
        
        filename = f"{file_id}{file_extension}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # 保存图片
        with open(filepath, "wb") as f:
            f.write(data_buffer)
        
        current_app.logger.info(f"图片已保存: {filename}")
        return filename
    
    def _is_quota_exceeded(self, error_msg):
        """检查是否是配额限制错误"""
        quota_indicators = [
            "429",
            "RESOURCE_EXHAUSTED", 
            "quota",
            "exceeded",
            "rate limit"
        ]
        return any(indicator.lower() in error_msg.lower() for indicator in quota_indicators)
    
    def _get_retry_delay(self, error_msg):
        """从错误信息中提取重试延迟时间"""
        # 尝试从错误信息中提取延迟时间
        retry_delay_match = re.search(r'retryDelay.*?(\d+)s', error_msg)
        if retry_delay_match:
            return int(retry_delay_match.group(1))
        
        # 默认延迟时间
        return 30  # 30秒
    
    def _setup_proxy_environment(self):
        """设置代理环境变量，确保Google GenAI客户端能正确使用代理"""
        # 按优先级顺序检查代理配置
        proxy_url = (
            os.environ.get('HTTP_PROXY') or 
            os.environ.get('HTTPS_PROXY') or 
            os.environ.get('ALL_PROXY') or
            os.environ.get('PROXY_URL')  # 从.env文件读取的自定义代理配置
        )
        
        if proxy_url:
            # 确保代理URL格式正确
            if not proxy_url.startswith(('http://', 'https://', 'socks5://')):
                proxy_url = f'http://{proxy_url}'
            
            # 设置所有必要的代理环境变量
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
            os.environ['ALL_PROXY'] = proxy_url
    
    def _get_proxy_info(self):
        """获取当前代理配置信息"""
        proxy_url = os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY') or os.environ.get('ALL_PROXY')
        return proxy_url
