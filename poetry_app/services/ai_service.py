"""
AI图像生成服务
"""

import os
import uuid
import mimetypes
from google import genai
from google.genai import types
from flask import current_app

class AIImageService:
    """AI图像生成服务类"""
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("⚠️  警告: GEMINI_API_KEY 环境变量未设置，AI图像生成功能将不可用")
    
    def generate_image_from_poetry(self, poetry_content, poetry_title=None):
        """
        根据诗词内容生成图片
        
        Args:
            poetry_content (str): 诗词内容
            poetry_title (str): 诗词标题
            
        Returns:
            str: 生成的图片文件名，失败返回None
        """
        if not self.api_key:
            current_app.logger.warning("AI图像生成功能不可用：未设置GEMINI_API_KEY")
            return None
            
        try:
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
                response_modalities=["IMAGE"],
            )
            
            # 生成图片
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
                    
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    
                    return self._save_image(chunk.candidates[0].content.parts[0].inline_data)
                    
        except Exception as e:
            error_msg = str(e)
            current_app.logger.error(f"生成图片时出错: {e}")
            
            # 检查是否是配额限制错误
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                current_app.logger.warning("Gemini API配额已用完，请检查您的API计划")
            elif "API_KEY" in error_msg:
                current_app.logger.warning("Gemini API密钥无效或未设置")
            
            return None
    
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
