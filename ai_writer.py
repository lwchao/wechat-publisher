"""AI 写作模块"""
import os, json, requests
from typing import Optional, Dict

class AIWriter:
    SUPPORTED_MODELS = {'glm': '智谱 GLM', 'minimax': 'MiniMax', 'qwen': '通义千问'}
    
    def __init__(self, model: str = 'glm'):
        self.model = model
        import yaml
        with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'r') as f:
            self.config = yaml.safe_load(f).get('ai', {})
    
    def _get_api_key(self) -> str:
        model_config = self.config.get(self.model, {})
        return model_config.get('api_key') or os.environ.get(f'{self.model.upper()}_API_KEY')
    
    def _get_base_url(self) -> str:
        return self.config.get(self.model, {}).get('base_url', '')
    
    def generate(self, keyword: str, style: str = '技术文章', length: str = '中等', title: Optional[str] = None) -> str:
        if self.model == 'glm':
            return self._generate_glm(keyword, style, length, title)
        elif self.model == 'minimax':
            return self._generate_minimax(keyword, style, length, title)
        elif self.model == 'qwen':
            return self._generate_qwen(keyword, style, length, title)
        raise ValueError(f"不支持的模型: {self.model}")
    
    def _build_prompt(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        length_map = {'短': '500-800 字', '中等': '1000-1500 字', '长': '2000-3000 字'}
        return f"""请根据以下关键词生成一篇适合微信公众号发布的文章。

关键词: {keyword}
文章标题: {title or '请根据关键词生成'}
文章风格: {style}
文章长度: {length_map.get(length, '中等')}

要求:
1. 文章格式为 Markdown
2. 开头要有吸引人的引言
3. 结构清晰，有多个小标题
4. 内容专业但不晦涩
5. 适合手机阅读
6. 可以添加适度的表情符号增加趣味性

请生成完整的文章内容。"""
    
    def _generate_glm(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        api_key = self._get_api_key()
        base_url = self._get_base_url() or 'https://open.bigmodel.cn/api/paas/v4'
        prompt = self._build_prompt(keyword, style, length, title)
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'glm-4-flash', 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.7}
        resp = requests.post(f'{base_url}/chat/completions', headers=headers, json=data, timeout=120)
        if resp.status_code != 200:
            raise Exception(f"API 调用失败: {resp.text}")
        return resp.json()['choices'][0]['message']['content']
    
    def _generate_minimax(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        api_key = self._get_api_key()
        base_url = self._get_base_url() or 'https://api.minimax.chat/v1'
        prompt = self._build_prompt(keyword, style, length, title)
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'abab6.5s-chat', 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.7}
        resp = requests.post(f'{base_url}/text/chatcompletion_v2', headers=headers, json=data, timeout=120)
        if resp.status_code != 200:
            raise Exception(f"API 调用失败: {resp.text}")
        return resp.json()['choices'][0]['message']['content']
    
    def _generate_qwen(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        api_key = self._get_api_key()
        base_url = self._get_base_url() or 'https://dashscope.aliyuncs.com/api/v1'
        prompt = self._build_prompt(keyword, style, length, title)
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'qwen-turbo', 'input': {'messages': [{'role': 'user', 'content': prompt}]}, 'parameters': {'temperature': 0.7}}
        resp = requests.post(f'{base_url}/services/aigc/text-generation/generation', headers=headers, json=data, timeout=120)
        if resp.status_code != 200:
            raise Exception(f"API 调用失败: {resp.text}")
        return resp.json()['output']['text']
