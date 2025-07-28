# 工具类
import uuid
import yaml
import os
import logging
from typing import Dict, Any, List
import requests
from config import TestConfig
import json

class TestUtils:
    """测试工具类"""
    
    @staticmethod
    def generate_request_uuid() -> str:
        """生成请求UUID，格式如: 7937bcfc-c99c-438b-ace7-9dd3f0ebdb3c"""
        return str(uuid.uuid4())
        
    @staticmethod
    def load_test_data(data_file: str) -> Dict[str, Any]:
        """加载测试数据，支持JSON和YAML"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, data_file)
        try:
            if data_file.endswith('.json'):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            return data
        except Exception as e:
            logging.error(f"加载测试数据失败: {e}")
            raise
    
    @staticmethod
    def make_api_request(url: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        """发送API请求"""
        if headers is None:
            headers = TestConfig.get_request_headers()
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=data,
                timeout=TestConfig.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API请求失败: {e}")
            raise
        